from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

EXCEL_FILE = BASE_DIR / "uploads" / "anexo5.xlsx"
DB_FILE = BASE_DIR / "vouchers.db"

print("Excel:", EXCEL_FILE)
print("Base :", DB_FILE)

df = pd.read_excel(
    EXCEL_FILE,
    sheet_name="Anexo5",
    engine="openpyxl"
)

print("Filas encontradas:", len(df))

conn = sqlite3.connect(str(DB_FILE))

df.to_sql(
    "anexo5",
    conn,
    if_exists="replace",
    index=False
)

conn.commit()

total = conn.execute(
    "SELECT COUNT(*) FROM anexo5"
).fetchone()[0]

print(f"Importación completada: {total:,} registros")

conn.close()