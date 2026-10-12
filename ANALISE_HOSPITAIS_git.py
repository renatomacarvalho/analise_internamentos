# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "6"
# ///
# DBTITLE 1,LEITURA CSV INTERNACOES
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

# DBTITLE 1,LEITURA CSV MUNICIPIOS

spark.sql("""
CREATE OR REPLACE VIEW workspace.default.municipios AS
SELECT *
FROM read_files(
  '/Volumes/workspace/default/analise_hospitais/RELATORIO_DTB_BRASIL_MUNICIPIO.csv',
  format => 'csv',
  header => true,
  inferSchema => true
)
""")

display(spark.table("workspace.default.municipios").limit(10))

# COMMAND ----------

Tabela de Municipios TOM.csv

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
# MAGIC  order by 1

# COMMAND ----------

# MAGIC %md
# MAGIC Quais top 10 cidades com internações

# COMMAND ----------

# DBTITLE 1,10 cidades com mais internaçõ
# MAGIC %sql
# MAGIC select 
# MAGIC SP_M_HOSP  , m.`Nome_Município`,
# MAGIC count(*) as qtde
# MAGIC  from workspace.default.sppr2501 s
# MAGIC  inner join workspace.default.municipios m on s.SP_M_HOSP = substring(m.`Código Município Completo`,1,6)
# MAGIC  group by all
# MAGIC  order by 3 desc
# MAGIC  limit 10

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     SP_CIDPRI, s.DESCRICAO,sp.*
# MAGIC FROM sppr2501 sp 
# MAGIC inner join cid10_subcategorias s on s.SUBCAT = sp.SP_CIDPRI