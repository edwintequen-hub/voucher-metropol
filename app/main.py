from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.services import (
    obtener_unidades,
    obtener_terminales,
    obtener_tipos_dia,
    obtener_servicios,
    obtener_voucher
)

from app.pdf import generar_pdf

app = FastAPI(title="Voucher Metropol")

BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static"
)


@app.get("/", response_class=HTMLResponse)
def inicio(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "unidades": obtener_unidades(),
            "tipos_dia": obtener_tipos_dia()
        }
    )


@app.get("/terminales/{unidad}")
def terminales(unidad: str):

    return obtener_terminales(unidad)


@app.get("/servicios/{unidad}/{terminal}/{tipo_dia}")
def servicios(
    unidad: str,
    terminal: str,
    tipo_dia: str
):

    return obtener_servicios(
        unidad,
        terminal,
        tipo_dia
    )


@app.get(
    "/voucher/{unidad}/{terminal}/{tipo_dia}/{servicio}/{salida}"
)
def voucher(
    unidad: str,
    terminal: str,
    tipo_dia: str,
    servicio: str,
    salida: str
):

    return obtener_voucher(
        unidad,
        terminal,
        servicio,
        tipo_dia,
        salida
    )


@app.get(
    "/voucher-pdf/{unidad}/{terminal}/{tipo_dia}/{servicio}/{salida}"
)
def voucher_pdf(
    unidad: str,
    terminal: str,
    tipo_dia: str,
    servicio: str,
    salida: str
):

    datos = obtener_voucher(
        unidad,
        terminal,
        servicio,
        tipo_dia,
        salida
    )

    print("TOTAL:", len(datos))

    for x in datos[:10]:
        print(x)

    pdf = generar_pdf(
        datos,
        unidad,
        terminal,
        servicio,
        tipo_dia
    )

    return Response(
    content=pdf,
    media_type="application/pdf",
    headers={
        "Content-Disposition":
        "inline; filename=voucher.pdf"
    }
)