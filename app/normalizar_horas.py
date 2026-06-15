import sqlite3

conn = sqlite3.connect("vouchers.db")

cursor = conn.cursor()

try:
    cursor.execute("""
    ALTER TABLE anexo5
    ADD COLUMN HORA_SALIDA_LIMPIA TEXT
    """)
except:
    pass

try:
    cursor.execute("""
    ALTER TABLE anexo5
    ADD COLUMN HORA_PARADERO_LIMPIA TEXT
    """)
except:
    pass

cursor.execute("""
SELECT
rowid,
[HORARIO DE SALIDA DESDE CABEZAL],
[HORARIO DE PASADA PARADERO]
FROM anexo5
""")

datos = cursor.fetchall()

for fila in datos:

    rowid = fila[0]

    salida = str(fila[1])
    pasada = str(fila[2])

    if " " in salida:
        salida = salida.split(" ")[1]

    if "." in pasada:
        pasada = pasada.split(".")[0]

    cursor.execute("""
    UPDATE anexo5
    SET
    HORA_SALIDA_LIMPIA=?,
    HORA_PARADERO_LIMPIA=?
    WHERE rowid=?
    """, (
        salida,
        pasada,
        rowid
    ))

conn.commit()

print("Horas normalizadas")

conn.close()