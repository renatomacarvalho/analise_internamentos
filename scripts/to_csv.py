import os
import csv
from dbfread import DBF

arquivo_dbf = "SPPR2501.dbf"
arquivo_csv = "SPPR2501.csv"

# Verificar se o arquivo existe
if not os.path.exists(arquivo_dbf):
    raise FileNotFoundError(
        f"Arquivo não encontrado: {arquivo_dbf}"
    )

print("Arquivo encontrado:")
print(arquivo_dbf)

tamanho = os.path.getsize(arquivo_dbf) / (1024 * 1024)
print(f"Tamanho: {tamanho:.2f} MB")
print()

# Abrir DBF sem carregar tudo na memória
dbf = DBF(
    arquivo_dbf,
    encoding="latin1",
    load=False
)

print(f"Quantidade de campos: {len(dbf.field_names)}")
print("Campos:")
print(dbf.field_names)
print()

print("Iniciando conversão DBF -> CSV...")
print("Aguarde...")
print()

contador = 0

with open(
    arquivo_csv,
    "w",
    newline="",
    encoding="utf-8-sig"
) as f:

    writer = csv.writer(f)

    # Cabeçalho
    writer.writerow(dbf.field_names)

    # Registros
    for registro in dbf:

        writer.writerow(
            [
                registro.get(campo)
                for campo in dbf.field_names
            ]
        )

        contador += 1

        if contador % 50000 == 0:
            print(
                f"Registros processados: {contador:,}"
            )

print()
print("=" * 60)
print("CONVERSÃO CONCLUÍDA")
print("=" * 60)

print(f"Registros: {contador:,}")
print(f"Arquivo: {arquivo_csv}")

if os.path.exists(arquivo_csv):

    tamanho_csv = (
        os.path.getsize(arquivo_csv)
        / (1024 * 1024)
    )

    print(
        f"Tamanho CSV: "
        f"{tamanho_csv:.2f} MB"
    )