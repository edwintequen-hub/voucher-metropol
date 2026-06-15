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

    cursor.execute("""
        SELECT
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
            [HORARIO DE SALIDA DESDE CABEZAL],
            EXPEDICION
    """, (
        unidad,
        terminal,
        servicio,
        tipo_dia
    ))

    filas = cursor.fetchall()

    conn.close()

    resultado = []

    for fila in filas:

        hora_pasada = str(fila[3] or "")
        hora_salida = str(fila[4] or "")

        # Eliminar fecha si existe
        if " " in hora_pasada:
            hora_pasada = hora_pasada.split(" ")[1]

        if " " in hora_salida:
            hora_salida = hora_salida.split(" ")[1]

        # Eliminar microsegundos
        if "." in hora_pasada:
            hora_pasada = hora_pasada.split(".")[0]

        if "." in hora_salida:
            hora_salida = hora_salida.split(".")[0]

        # Filtrar por hora de salida
        if salida.upper() != "TODO":
            if hora_salida[:5] != salida:
                continue

        resultado.append({
            "EXPEDICION": fila[0],
            "CODIGO PARADERO USUARIO": fila[1],
            "NOMBRE PARADERO": fila[2],
            "HORARIO DE PASADA PARADERO": hora_pasada,
            "HORARIO DE SALIDA DESDE CABEZAL": hora_salida
        })

    return resultado