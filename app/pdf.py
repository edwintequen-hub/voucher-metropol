from io import BytesIO
from pathlib import Path
from collections import defaultdict

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Table,
    TableStyle,
    Image,
    PageBreak
)

BASE_DIR = Path(__file__).resolve().parent.parent
LOGO_PATH = BASE_DIR / "static" / "logo_metropol.png"


def crear_voucher_expedicion(
    expedicion,
    filas,
    unidad,
    terminal,
    servicio,
    tipo_dia,
    styles
):

    contenido = []

    if LOGO_PATH.exists():

        logo = Image(str(LOGO_PATH))
        logo.drawWidth = 50
        logo.drawHeight = 20

        contenido.append([logo])

    contenido.append([
        Paragraph(
            "<b>METROPOL</b>",
            styles["Heading3"]
        )
    ])

    contenido.append([
        Paragraph(
            f"<b>Voucher Expedición {expedicion}</b>",
            styles["BodyText"]
        )
    ])

    contenido.append([
        Paragraph(
            f"Unidad: {unidad}<br/>"
            f"Terminal: {terminal}<br/>"
            f"Servicio: {filas[0]['SERVICIO CLIENTE']}<br/>"
            f"Tipo Día: {tipo_dia}",
            styles["BodyText"]
        )
    ])

    datos = [
    [
        "HORARIO DE SALIDA \nDESDE CABEZAL",
        "CODIGO PARADERO \nUSUARIO",
        "NOMBRE PARADERO",
        "HORARIO DE PASADA \nPARADERO"
    ]
]

    for fila in filas:

        datos.append([
    str(fila["HORARIO DE SALIDA DESDE CABEZAL"])[:5],
    str(fila["CODIGO PARADERO USUARIO"]),
    str(fila["NOMBRE PARADERO"]),
    str(fila["HORARIO DE PASADA PARADERO"])[:5]
])

    tabla = Table(
    datos,
    colWidths=[30, 30, 75, 30]
)

    tabla.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.red),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

    # Encabezados más pequeños
    ("FONTSIZE", (0, 0), (-1, 0), 4),

    # Datos normales
    ("FONTSIZE", (0, 1), (-1, -1), 5),

    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("ALIGN", (0, 0), (-1, -1), "CENTER")
]))

    contenido.append([tabla])

    voucher = Table(
    contenido,
    colWidths=[170]
)

    voucher.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2)
    ]))

    return voucher


def generar_pdf(
    voucher,
    unidad,
    terminal,
    servicio,
    tipo_dia
):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        topMargin=15,
        bottomMargin=15,
        leftMargin=15,
        rightMargin=15
    )

    styles = getSampleStyleSheet()

    expediciones = defaultdict(list)

    for fila in voucher:
        clave = (
            fila["SERVICIO CLIENTE"],
            fila["EXPEDICION"]
        )
        expediciones[clave].append(fila)

    print("EXPEDICIONES ENCONTRADAS:")
    print(list(expediciones.keys()))
    print("TOTAL EXPEDICIONES:", len(expediciones))

    tarjetas = []

    for clave in sorted(expediciones.keys()):
            
            
        servicio_actual, expedicion = clave


        tarjetas.append(
            crear_voucher_expedicion(
                expedicion,
                expediciones[clave],
                unidad,
                terminal,
                servicio_actual,
                tipo_dia,
                styles
            )
        )

    print("TOTAL TARJETAS:", len(tarjetas))

    elementos = []

    for i in range(0, len(tarjetas), 3):

        grupo = tarjetas[i:i + 3]

        while len(grupo) < 3:
            grupo.append("")

            pagina = Table(
        [
            [grupo[0], grupo[1], grupo[2]]
        ],
        colWidths=[180, 180, 180]
    )

        pagina.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP")
        ]))

        elementos.append(pagina)

        if i + 4 < len(tarjetas):
            elementos.append(PageBreak())

    doc.build(elementos)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf