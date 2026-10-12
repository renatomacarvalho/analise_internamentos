# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "6"
# ///
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

Quais hospitais concentraram mais internações?
Quais doenças/CIDs foram mais frequentes?
Qual foi o custo hospitalar estimado?
Qual foi o tempo médio de permanência?
Quais procedimentos tiveram maior volume?

# COMMAND ----------

# MAGIC %md
# MAGIC Qual a quantidade geral de internações?

# COMMAND ----------

# DBTITLE 1,TOTAL GERAL
# MAGIC %sql
# MAGIC select count(*) as qtde
# MAGIC  from workspace.default.sppr2501

# COMMAND ----------

# MAGIC %md
# MAGIC Quais dias das semana tem mais registro de entrada de internações?

# COMMAND ----------

# MAGIC %sql
# MAGIC select 
# MAGIC
# MAGIC CASE DATE_FORMAT(TO_DATE(CAST(SP_DTINTER AS STRING), 'yyyyMMdd'), 'EEEE')
# MAGIC     WHEN 'Sunday'    THEN '1.Domingo'
# MAGIC     WHEN 'Monday'    THEN '2.Segunda-feira'
# MAGIC     WHEN 'Tuesday'   THEN '3.Terça-feira'
# MAGIC     WHEN 'Wednesday' THEN '4.Quarta-feira'
# MAGIC     WHEN 'Thursday'  THEN '5.Quinta-feira'
# MAGIC     WHEN 'Friday'    THEN '6.Sexta-feira'
# MAGIC     WHEN 'Saturday'  THEN '7.Sábado'
# MAGIC END AS dia_semana,
# MAGIC count(*) as quantidade
# MAGIC  from workspace.default.sppr2501
# MAGIC  group by all

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW aih_permanencia AS
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
# MAGIC   AND SP_DTSAIDA IS NOT NULL;
# MAGIC
# MAGIC SELECT * FROM aih_permanencia LIMIT 20;

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