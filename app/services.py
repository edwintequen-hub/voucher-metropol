from app.database import get_connection


def obtener_unidades():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT UNIDAD
        FROM anexo5
        ORDER BY UNIDAD
    """)

    datos = [x[0] for x in cursor.fetchall()]

    conn.close()

    return datos


def obtener_terminales(unidad):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT TERMINAL
        FROM anexo5
        WHERE UNIDAD = ?
        ORDER BY TERMINAL
    """, (unidad,))

    datos = [x[0] for x in cursor.fetchall()]

    conn.close()

    return datos


def obtener_tipos_dia():

    return [
        "Laboral",
        "Sábado",
        "Domingo"
    ]


def obtener_servicios(
    unidad,
    terminal,
    tipo_dia
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT [SERVICIO CLIENTE]
        FROM anexo5
        WHERE UNIDAD = ?
        AND TERMINAL = ?
        AND [TIPO DIA] = ?
        ORDER BY [SERVICIO CLIENTE]
    """, (
        unidad,
        terminal,
        tipo_dia
    ))

    datos = [x[0] for x in cursor.fetchall()]

    conn.close()

    return datos


def obtener_voucher(
    unidad,
    terminal,
    servicio,
    tipo_dia,
    salida
):

    conn = get_connection()
    cursor = conn.cursor()

    if servicio.upper() == "TODOS":

        cursor.execute("""
            SELECT
                [SERVICIO CLIENTE],
                EXPEDICION,
                [CODIGO PARADERO USUARIO],
                [NOMBRE PARADERO],
                [HORARIO DE PASADA PARADERO],
                [HORARIO DE SALIDA DESDE CABEZAL]
            FROM anexo5
            WHERE UNIDAD = ?
            AND TERMINAL = ?
            AND [TIPO DIA] = ?
            ORDER BY
                [SERVICIO CLIENTE],
                EXPEDICION,
                [HORARIO DE SALIDA DESDE CABEZAL]
        """, (
            unidad,
            terminal,
            tipo_dia
        ))

    else:

        cursor.execute("""
            SELECT
                [SERVICIO CLIENTE],
                EXPEDICION,
                [CODIGO PARADERO USUARIO],
                [NOMBRE PARADERO],
                [HORARIO DE PASADA PARADERO],
                [HORARIO DE SALIDA DESDE CABEZAL]
            FROM anexo5
            WHERE UNIDAD = ?
            AND TERMINAL = ?
            AND [SERVICIO CLIENTE] = ?
            AND [TIPO DIA] = ?
            ORDER BY
                EXPEDICION,
                [HORARIO DE SALIDA DESDE CABEZAL]
        """, (
            unidad,
            terminal,
            servicio,
            tipo_dia
        ))

    filas = cursor.fetchall()

    conn.close()

    print("FILAS SQL:", len(filas))

    resultado = []

    for fila in filas:

        hora_pasada = str(fila[4] or "")
        hora_salida = str(fila[5] or "")

        if " " in hora_pasada:
            hora_pasada = hora_pasada.split(" ")[1]

        if " " in hora_salida:
            hora_salida = hora_salida.split(" ")[1]

        if "." in hora_pasada:
            hora_pasada = hora_pasada.split(".")[0]

        if "." in hora_salida:
            hora_salida = hora_salida.split(".")[0]

        if salida.upper() != "TODO":
            if hora_salida[:5] != salida:
                continue

        resultado.append({
            "SERVICIO CLIENTE": fila[0],
            "EXPEDICION": fila[1],
            "CODIGO PARADERO USUARIO": fila[2],
            "NOMBRE PARADERO": fila[3],
            "HORARIO DE PASADA PARADERO": hora_pasada,
            "HORARIO DE SALIDA DESDE CABEZAL": hora_salida
        })

    print("REGISTROS RESULTADO:", len(resultado))

    return resultado    