import os
import pandas as pd
import datasus_dbc
from dbfread import DBF

# Arquivo original
arquivo_dbc = "SPPR2501.dbc"

# Arquivos intermediários e final
arquivo_dbf = "SPPR2501.dbf"
arquivo_csv = "SPPR2501.csv"

# Verifica se o DBC existe
if not os.path.exists(arquivo_dbc):
    raise FileNotFoundError(
        f"Arquivo não encontrado: {arquivo_dbc}"
    )

print("Arquivo encontrado:")
print(arquivo_dbc)

# DBC -> DBF
print("\nDescompactando DBC para DBF...")

datasus_dbc.decompress(
    arquivo_dbc,
    arquivo_dbf
)

print("DBF criado:", arquivo_dbf)

# DBF -> DataFrame
print("\nLendo DBF...")

dbf = DBF(
    arquivo_dbf,
    encoding="latin1"
)

df = pd.DataFrame(iter(dbf))

print(f"Registros: {len(df):,}")
print(f"Colunas: {len(df.columns)}")

# DataFrame -> CSV
print("\nGerando CSV...")

df.to_csv(
    arquivo_csv,
    index=False,
    encoding="utf-8-sig"
)

print("\nCONCLUÍDO!")
print("Arquivo criado:", arquivo_csv)
print(f"Tamanho: {os.path.getsize(arquivo_csv):,} bytes")

print("\nPrimeiras linhas:")
print(df.head())
