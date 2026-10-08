# Databricks notebook source

SP = dados detalhados de AIH / Produção Hospitalar (SIH/SUS)
PR = Paraná
2501 = competência 01/2025
.dbc = formato compactado utilizado pelo DATASUS.

Sistema de Informações Hospitalares do SUS

# COMMAND ----------

# DBTITLE 1,LEITURA CSV
spark.sql("""
CREATE OR REPLACE VIEW workspace.default.sppr2501 AS
SELECT *
FROM read_files(
  '/Volumes/workspace/default/analise_hospitais/SPPR2501.csv',
  format => 'csv',
  header => true,
  inferSchema => true
)
""")

display(spark.table("workspace.default.sppr2501").limit(10))

# COMMAND ----------

# DBTITLE 1,BASE BRUTA
# MAGIC %sql
# MAGIC select * from workspace.default.sppr2501
# MAGIC limit 10

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(DISTINCT SP_NAIH) AS total_AIH
# MAGIC FROM workspace.default.sppr2501;

# COMMAND ----------

# DBTITLE 1,quais são os principais CIDs das internações
# MAGIC %sql
# MAGIC SELECT
# MAGIC     SP_CIDPRI AS cid_principal,
# MAGIC     COUNT(DISTINCT SP_NAIH) AS quantidade_AIH
# MAGIC FROM workspace.default.sppr2501
# MAGIC WHERE SP_CIDPRI IS NOT NULL
# MAGIC   AND SP_CIDPRI <> ''
# MAGIC GROUP BY SP_CIDPRI
# MAGIC ORDER BY quantidade_AIH DESC
# MAGIC LIMIT 20;

# COMMAND ----------

Quais hospitais concentraram mais internações?
Quais doenças/CIDs foram mais frequentes?
Qual foi o custo hospitalar estimado?
Qual foi o tempo médio de permanência?
Quais procedimentos tiveram maior volume?

# COMMAND ----------

# DBTITLE 1,quantas aih por  mes
# MAGIC %sql
# MAGIC SELECT
# MAGIC     SP_AA AS ano,
# MAGIC     SP_MM AS mes,
# MAGIC     COUNT(DISTINCT SP_NAIH) AS quantidade_AIH
# MAGIC FROM workspace.default.sppr2501
# MAGIC GROUP BY SP_AA, SP_MM
# MAGIC ORDER BY ano, mes;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     SP_DTINTER,
# MAGIC     SP_DTSAIDA
# MAGIC FROM workspace.default.sppr2501
# MAGIC WHERE SP_DTINTER IS NOT NULL
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     SP_NAIH AS AIH,
# MAGIC     TO_DATE(CAST(SP_DTINTER AS STRING), 'yyyyMMdd') AS data_internacao,
# MAGIC     TO_DATE(CAST(SP_DTSAIDA AS STRING), 'yyyyMMdd') AS data_saida,
# MAGIC     DATEDIFF(
# MAGIC         TO_DATE(CAST(SP_DTSAIDA AS STRING), 'yyyyMMdd'),
# MAGIC         TO_DATE(CAST(SP_DTINTER AS STRING), 'yyyyMMdd')
# MAGIC     ) AS dias_permanencia
# MAGIC FROM workspace.default.sppr2501
# MAGIC WHERE SP_DTINTER IS NOT NULL
# MAGIC   AND SP_DTSAIDA IS NOT NULL
# MAGIC LIMIT 20;

# COMMAND ----------

# DBTITLE 1,CRIA VIEW
# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW aih_permanencia AS
# MAGIC
# MAGIC SELECT
# MAGIC     SP_NAIH AS AIH,
# MAGIC     MIN(
# MAGIC         TO_DATE(CAST(SP_DTINTER AS STRING), 'yyyyMMdd')
# MAGIC     ) AS data_internacao,
# MAGIC     MAX(
# MAGIC         TO_DATE(CAST(SP_DTSAIDA AS STRING), 'yyyyMMdd')
# MAGIC     ) AS data_saida,
# MAGIC     DATEDIFF(
# MAGIC         MAX(TO_DATE(CAST(SP_DTSAIDA AS STRING), 'yyyyMMdd')),
# MAGIC         MIN(TO_DATE(CAST(SP_DTINTER AS STRING), 'yyyyMMdd'))
# MAGIC     ) AS dias_permanencia
# MAGIC
# MAGIC FROM workspace.default.sppr2501
# MAGIC
# MAGIC WHERE SP_NAIH IS NOT NULL
# MAGIC   AND SP_DTINTER IS NOT NULL
# MAGIC   AND SP_DTSAIDA IS NOT NULL
# MAGIC
# MAGIC GROUP BY SP_NAIH;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     COUNT(*) AS total_AIH,
# MAGIC     ROUND(AVG(dias_permanencia), 2) AS permanencia_media,
# MAGIC     MIN(dias_permanencia) AS permanencia_minima,
# MAGIC     MAX(dias_permanencia) AS permanencia_maxima
# MAGIC FROM aih_permanencia;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     AIH,
# MAGIC     data_internacao,
# MAGIC     data_saida,
# MAGIC     dias_permanencia
# MAGIC FROM aih_permanencia
# MAGIC ORDER BY dias_permanencia DESC
# MAGIC LIMIT 20;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     COUNT(*) AS AIHs_0_dias
# MAGIC FROM aih_permanencia
# MAGIC WHERE dias_permanencia = 0;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     CASE
# MAGIC         WHEN dias_permanencia = 0 THEN '0 dias'
# MAGIC         WHEN dias_permanencia BETWEEN 1 AND 3 THEN '1-3 dias'
# MAGIC         WHEN dias_permanencia BETWEEN 4 AND 7 THEN '4-7 dias'
# MAGIC         WHEN dias_permanencia BETWEEN 8 AND 15 THEN '8-15 dias'
# MAGIC         WHEN dias_permanencia BETWEEN 16 AND 30 THEN '16-30 dias'
# MAGIC         ELSE '31+ dias'
# MAGIC     END AS faixa_permanencia,
# MAGIC     COUNT(*) AS quantidade_AIH
# MAGIC FROM aih_permanencia
# MAGIC GROUP BY
# MAGIC     CASE
# MAGIC         WHEN dias_permanencia = 0 THEN '0 dias'
# MAGIC         WHEN dias_permanencia BETWEEN 1 AND 3 THEN '1-3 dias'
# MAGIC         WHEN dias_permanencia BETWEEN 4 AND 7 THEN '4-7 dias'
# MAGIC         WHEN dias_permanencia BETWEEN 8 AND 15 THEN '8-15 dias'
# MAGIC         WHEN dias_permanencia BETWEEN 16 AND 30 THEN '16-30 dias'
# MAGIC         ELSE '31+ dias'
# MAGIC     END
# MAGIC ORDER BY quantidade_AIH DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     AIH,
# MAGIC     data_internacao,
# MAGIC     data_saida,
# MAGIC     dias_permanencia
# MAGIC FROM aih_permanencia
# MAGIC WHERE dias_permanencia = 3576;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     SP_NAIH AS AIH,
# MAGIC     SP_DTINTER AS data_internacao,
# MAGIC     SP_DTSAIDA AS data_saida,
# MAGIC     SP_CIDPRI AS CID_principal,
# MAGIC     SP_CNES AS CNES,
# MAGIC     SP_PROCREA AS procedimento,
# MAGIC     SP_VALATO AS valor
# MAGIC FROM workspace.default.sppr2501
# MAGIC WHERE SP_NAIH = '4115104952398';

# COMMAND ----------

spark.sql("""
CREATE OR REPLACE VIEW workspace.default.cid10_subcategorias AS
SELECT *
FROM read_files(
  '/Volumes/workspace/default/analise_hospitais/CID-10-SUBCATEGORIAS.CSV',
  format => 'csv',
  header => true,
  delimiter => ';',
  encoding => 'ISO-8859-1',
  inferSchema => true
)
""")
subcategorias = spark.table("workspace.default.cid10_subcategorias")
subcategorias.createOrReplaceTempView("subcategorias")
display(subcategorias.limit(10))

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     SP_CIDPRI, s.DESCRICAO,sp.*
# MAGIC FROM sppr2501 sp 
# MAGIC inner join cid10_subcategorias s on s.SUBCAT = sp.SP_CIDPRI

# COMMAND ----------

# DBTITLE 1,cid mais frequentes
# MAGIC %sql
# MAGIC SELECT
# MAGIC  COUNT(DISTINCT SP_NAIH) AS quantidade_AIH ,
# MAGIC     SP_CIDPRI AS CID,
# MAGIC     s.DESCRICAO
# MAGIC FROM sppr2501 sp
# MAGIC inner join cid10_subcategorias s on s.SUBCAT = sp.SP_CIDPRI
# MAGIC WHERE SP_CIDPRI IS NOT NULL
# MAGIC GROUP BY
# MAGIC   all
# MAGIC ORDER BY quantidade_AIH DESC;