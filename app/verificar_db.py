from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "vouchers.db"

conn = sqlite3.connect(DB_FILE)

cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM anexo5")

total = cursor.fetchone()[0]

print("Total registros:", total)

cursor.execute("""
SELECT DISTINCT TERMINAL
FROM anexo5
ORDER BY TERMINAL
LIMIT 20
""")

print("\nTerminales:")

for row in cursor.fetchall():
    print("-", row[0])

conn.close()