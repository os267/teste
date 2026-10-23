"""
Genera el Playbook Comercial en HTML con estilos en línea, pensado para subirlo a
Google Drive y convertirlo en Google Docs (las figuras se dibujan con tablas, sin imágenes).

Uso:  python3 playbook/generar_html_docs.py  ->  playbook/salida/Playbook_Comercial_GoogleDocs.html
"""
import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import contenido as C  # noqa: E402

SALIDA = Path(__file__).parent / "salida" / "Playbook_Comercial_GoogleDocs.html"

AZUL, AZUL_P, DORADO, CLARO, TEXTO, GRIS = "#1B365D", "#0F2537", "#C5A059", "#F4F7FA", "#2C3E50", "#7A8794"
VERDE, CREMA = "#4F7A5A", "#FBF3E1"
TIT, CUE = "'Playfair Display',Georgia,serif", "Montserrat,Arial,sans-serif"
e = html.escape
CLASES: dict[str, str] = {}


def cls(estilo: str) -> str:
    """Convierte un estilo en línea en una clase CSS compartida (el HTML pesa mucho menos)."""
    if estilo not in CLASES:
        CLASES[estilo] = f"c{len(CLASES)}"
    return CLASES[estilo]


def span(t, size=10.5, color=TEXTO, bold=False, italic=False, font=CUE):
    est = f"font-family:{font};font-size:{size}pt;color:{color}"
    est += ";font-weight:bold" if bold else ""
    est += ";font-style:italic" if italic else ""
    return f'<span class="{cls(est)}">{e(t)}</span>'


def p(contenido, alinear="left", antes=0, despues=6):
    return f'<p class="{cls(f"margin:{antes}pt 0 {despues}pt 0;text-align:{alinear};line-height:1.25")}">{contenido}</p>'


def tabla(filas, anchos=None):
    """filas: lista de listas de (html, estilo_td)."""
    cols = ""
    if anchos:
        cols = "".join(f'<col width="{a}">' for a in anchos)
    cuerpo = "".join("<tr>" + "".join(f'<td class="{cls("vertical-align:top;padding:6pt 8pt;" + est)}">{h}</td>'
                                      for h, est in fila) + "</tr>" for fila in filas)
    return (f'<table style="border-collapse:collapse;width:100%;margin:4pt 0 10pt 0">{cols}{cuerpo}</table>')


def bg(color):
    return f"background-color:{color};"


def caja(titulo, cuerpo, fondo=CLARO, borde=DORADO, color_t=AZUL, color_c=TEXTO):
    h = ""
    if titulo:
        h += p(span(titulo.upper(), 9, color_t, bold=True), despues=3)
    if isinstance(cuerpo, str):
        h += p(span(cuerpo, 10.5, color_c), despues=0)
    else:
        h += "".join(p(span("■  ", 7.5, borde) + span(it, 10, color_c), despues=2) for it in cuerpo)
    return tabla([[(h, bg(fondo) + f"border-left:4pt solid {borde};padding:8pt 12pt")]])


def tabla_datos(enc, filas, anchos, resaltar=None):
    cab = [(span(x, 9, "#FFFFFF", bold=True), bg(AZUL)) for x in enc]
    cuerpo = []
    for i, f in enumerate(filas):
        fondo = CREMA if resaltar and resaltar(f) else (CLARO if i % 2 else "#FFFFFF")
        cuerpo.append([(span(v, 9.5, AZUL if j == 0 else TEXTO, bold=(j == 0)),
                        bg(fondo) + "border-bottom:1pt solid #D9DEE4") for j, v in enumerate(f)])
    return tabla([cab] + cuerpo, anchos)


def salto():
    return '<p style="page-break-before:always;margin:0"></p>'


def seccion(num, titulo, intro=""):
    h = (f'<h1 style="margin:0 0 4pt 0;border-bottom:2pt solid {DORADO};padding-bottom:4pt">'
         f'{span(num + "  ", 24, DORADO, True, font=TIT)}{span(titulo, 22, AZUL, True, font=TIT)}</h1>')
    if intro:
        h += p(span(intro, 11, GRIS, italic=True), antes=6, despues=10)
    return h


def sub(t):
    return f'<h2 style="margin:12pt 0 4pt 0">{span(t, 14, AZUL, True, font=TIT)}</h2>'


def etiqueta(t):
    return p(span(t.upper(), 8.5, DORADO, bold=True), antes=6, despues=2)


def pie(t):
    return p(span(t, 8.5, GRIS, italic=True), "center", despues=10)


# ---------------------------------------------------------------------------
# figuras como tablas
# ---------------------------------------------------------------------------
def fig_logos():
    celdas = [(p(span("LOGO", 8, GRIS, True), "center", despues=2) + p(span(m, 12, AZUL, True), "center", despues=0),
               f"border:1.5pt dashed {DORADO};padding:14pt")
              for m in ("La Auxiliadora", "Hogar de las Memorias", "Vangrupo")]
    return tabla([celdas], ["33%", "34%", "33%"])


def fig_portafolio():
    colores = [AZUL, VERDE, AZUL, VERDE, DORADO, "#8A8F98"]
    celdas = []
    for pr, col in zip(C.PRODUCTOS, colores):
        h = p(span("PRÓXIMO LANZAMIENTO", 7.5, "#B8860B", True), despues=2) if pr.get("proximo") else ""
        h += p(span(pr["etiqueta"].upper(), 7.5, GRIS), despues=2)
        h += p(span(pr["corto"], 12.5, AZUL_P, True), despues=2)
        h += p(span(pr["precio"], 16, col, True), despues=2)
        h += p(span(pr["pago"], 8.5), despues=0)
        celdas.append((h, bg(CREMA if pr.get("proximo") else CLARO) + f"border-top:4pt solid {col};"
                       "border-left:4pt solid #FFFFFF;border-right:4pt solid #FFFFFF;border-bottom:6pt solid #FFFFFF"))
    return tabla([celdas[:3], celdas[3:]], ["33%", "34%", "33%"]) + pie(
        "Figura 1 · El portafolio en un vistazo. Precios sugeridos, IVA incluido.")


def fig_embudo():
    tonos = ["#1B365D", "#2E4A70", "#425E83", "#567296", "#6A86A9", "#7E9ABC", "#92AECF"]
    filas = []
    for i, (etapa, desc) in enumerate(C.EMBUDO):
        filas.append([(p(span(str(i + 1), 12, AZUL_P, True), "center", despues=0), bg(DORADO) + "border-bottom:2pt solid #FFFFFF"),
                      (p(span(etapa, 11.5, "#FFFFFF", True), despues=0), bg(tonos[i]) + "border-bottom:2pt solid #FFFFFF"),
                      (p(span(desc, 10), despues=0), bg(CLARO if i % 2 == 0 else "#FFFFFF") + "border-bottom:2pt solid #FFFFFF")])
    return tabla(filas, ["7%", "27%", "66%"]) + pie("Figura 2 · Las 7 etapas del embudo de prenecesidad.")


def fig_conversacion():
    cab = [(p(span(f"{i + 1}  ", 13, DORADO, True) + span(paso, 10.5, "#FFFFFF", True), despues=0),
            bg(AZUL) + f"border-right:3pt solid #FFFFFF;border-bottom:3pt solid {DORADO}")
           for i, (paso, _) in enumerate(C.CONVERSACION)]
    cuerpo = [(p(span(desc, 9), despues=0), "") for _, desc in C.CONVERSACION]
    return tabla([cab, cuerpo], ["20%"] * 5) + pie("Figura 3 · Toda conversación sigue cinco pasos.")


def fig_equipos():
    cab = [(p(span(eq, 10.5, "#FFFFFF", True), despues=0), bg(AZUL) + f"border-bottom:3pt solid {DORADO};border-right:4pt solid #FFFFFF")
           for eq, _ in C.EQUIPOS]
    mid = [(p(span(desc, 9.5), despues=0), bg(CLARO) + "border-right:4pt solid #FFFFFF") for _, desc in C.EQUIPOS]
    return tabla([cab, mid], ["33%", "34%", "33%"]) + pie("Figura 4 · " + C.EQUIPOS_NOTA)


def fig_ciclo():
    pasos = [
        ("Inhumación", "Urna biodegradable en el jardín, con placa de identificación."),
        ("3 años", "La familia visita un lugar señalado; la urna se integra a la tierra."),
        ("Placa memorial", "El nombre pasa al monumento del jardín (incluida en el Ecológico y en Mascotas)."),
        ("Ciclo natural", "El espacio se reutiliza: el jardín sigue vivo para otras familias."),
    ]
    cab = [(p(span(str(i + 1), 16, "#FFFFFF", True), "center", despues=0) + p(span(t, 10.5, "#FFFFFF", True), "center", despues=0),
            bg(VERDE) + "border-right:3pt solid #FFFFFF") for i, (t, _) in enumerate(pasos)]
    cuerpo = [(p(span(d, 9), "center", despues=0), bg(CLARO) + "border-right:3pt solid #FFFFFF") for _, d in pasos]
    return tabla([cab, cuerpo], ["25%"] * 4) + pie(
        "Figura 5 · El ciclo de 3 años del Jardín Ecológico y de Mascotas, explicado al cliente.")


def fig_vra():
    celdas = [(p(span(paso[0], 30, AZUL, True, font=TIT), "center", despues=0)
               + p(span(f"{i + 1}. {paso}", 12, AZUL_P, True), "center", despues=2)
               + p(span(desc, 9.5), "center", despues=0),
               bg(CLARO) + f"border-top:4pt solid {DORADO};border-right:4pt solid #FFFFFF")
              for i, (paso, desc) in enumerate(C.METODO_OBJECIONES)]
    return tabla([celdas], ["33%", "34%", "33%"]) + caja("", C.PRINCIPIO_OBJECIONES) + pie(
        "Figura 6 · Método V·R·A: Validar, Reposicionar, Avanzar.")


def fig_comisiones():
    maximo = max(v for _, v in C.COMISIONES_VALORES)
    filas = []
    for nombre, valor in C.COMISIONES_VALORES:
        monto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        filas.append([(p(span(nombre, 10, AZUL_P, True), "right", despues=0), "padding:3pt 8pt"),
                      (p(span("█" * max(1, round(valor / maximo * 26)), 10, AZUL)
                         + span(f"  US$ {monto}", 10, AZUL, True), despues=0), "padding:3pt 8pt")])
    return tabla(filas, ["28%", "72%"]) + pie("Figura 7 · Comisión del mes según cantidad de ventas (ejemplo con Solución Modular).")


# ---------------------------------------------------------------------------
# secciones
# ---------------------------------------------------------------------------
def portada():
    h = fig_logos() + p("", despues=30)
    banda = (p(span(C.CAMPANA.upper(), 10, DORADO, True), despues=8)
             + p(span(C.TITULO, 36, "#FFFFFF", True, font=TIT), despues=4)
             + p(span(C.SUBTITULO, 16, "#E8EDF3", font=TIT), despues=14)
             + p(span(C.MARCAS, 10.5, DORADO, True), despues=0))
    h += tabla([[(banda, bg(AZUL) + f"padding:24pt;border-bottom:5pt solid {DORADO}")]])
    h += p(span(f"\"{C.LEMA}\"", 15, AZUL, italic=True, font=TIT), "center", antes=24, despues=40)
    h += p(span(C.VERSION, 9, GRIS), "center")
    return h + salto()


def como_usar():
    h = sub("Cómo usar este playbook") + p(span(C.COMO_USAR), despues=10)
    h += caja("Pendientes de validación (versión 1.1)", C.PENDIENTES, fondo=CREMA)
    h += sub("Contenido")
    h += tabla([[(p(span(n, 18, DORADO, True, font=TIT), despues=0), "border-bottom:1pt solid #D9DEE4"),
                 (p(span(t, 12, AZUL, True), despues=0), "border-bottom:1pt solid #D9DEE4")] for n, t in C.INDICE],
               ["12%", "88%"])
    return h + salto()


def s01():
    h = seccion("01", "Quiénes somos y lo que vendemos") + p(span(C.QUIENES_SOMOS), despues=10)
    h += fig_portafolio() + sub("¿Por qué ahora?")
    celdas = [(p(span(t, 11.5, AZUL, True), despues=2) + p(span(d, 10), despues=0),
               bg(CLARO) + f"border-top:3pt solid {DORADO};border-right:4pt solid #FFFFFF;border-bottom:4pt solid #FFFFFF")
              for t, d in C.POR_QUE_AHORA]
    h += tabla([celdas[:2], celdas[2:]], ["50%", "50%"]) + sub("Dos momentos de venta")
    h += "".join(p(span(t + ". ", bold=True, color=AZUL) + span(d), despues=5) for t, d in C.MODOS_DE_VENTA)
    h += caja("Regla de oro", C.REGLA_DE_ORO, fondo=AZUL, color_t=DORADO, color_c="#FFFFFF")
    return h + salto()


def s02():
    h = seccion("02", "A quién le vendemos", "Cinco perfiles de cliente. Identifique el perfil en los primeros minutos y adapte el tono.")
    h += tabla_datos(["Perfil", "Quién es", "Qué busca", "Tono", "Producto ideal"], [list(x) for x in C.PERFILES],
                     ["18%", "19%", "23%", "18%", "22%"])
    return h + caja("Filtro de calificación: N · O · A", C.FILTRO_CALIFICACION) + salto()


def s03():
    h = seccion("03", "El proceso de venta", "Un camino claro, del primer contacto a la posventa. Cada etapa tiene un objetivo.")
    h += fig_embudo() + fig_conversacion() + sub(C.EQUIPOS_TITULO) + fig_equipos()
    h += sub("Rituales del equipo") + tabla_datos(["Frecuencia", "Ritual"], [list(r) for r in C.RITUALES], ["20%", "80%"])
    return h + salto()


def ficha(pr):
    prox = pr.get("proximo")
    izq = (p(span(pr["etiqueta"].upper(), 8.5, DORADO, True), despues=2)
           + p(span(pr["nombre"], 17, "#FFFFFF", True, font=TIT), despues=0))
    der = (p(span("PRÓXIMO LANZAMIENTO" if prox else pr.get("etiqueta_precio", "PRECIO SUGERIDO"), 8.5, DORADO, True), "right", despues=2)
           + p(span(pr["precio"], 17, "#FFFFFF", True), "right", despues=0))
    fondo = "#8A8F98" if prox else AZUL
    h = tabla([[(izq, bg(fondo) + f"border-bottom:4pt solid {DORADO};padding:10pt 12pt"),
                (der, bg(fondo) + f"border-bottom:4pt solid {DORADO};padding:10pt 12pt")]], ["66%", "34%"])
    h += p(span(pr["pago"], 9.5, GRIS, italic=True), despues=8)
    h += p(span("Qué es. ", bold=True, color=AZUL) + span(pr["que_es"]), despues=6)
    h += p(span("Para quién. ", bold=True, color=AZUL) + span(pr["para_quien"]), despues=8)
    inc = p(span("QUÉ INCLUYE", 8.5, AZUL, True), despues=3) + "".join(
        p(span("✓  ", 9, VERDE, True) + span(x, 9.5), despues=2) for x in pr["incluye"])
    reg = p(span("REGLAS DEL PRODUCTO", 8.5, AZUL, True), despues=3) + "".join(
        p(span("■  ", 7.5, DORADO) + span(x, 9.5), despues=2) for x in pr["reglas"])
    estilo = bg(CLARO) + f"border-top:3pt solid {DORADO};border-right:4pt solid #FFFFFF"
    h += tabla([[(inc, estilo), (reg, estilo)]], ["50%", "50%"])
    h += etiqueta("Speech sugerido") + caja("", pr["speech"], fondo=CREMA)
    h += etiqueta("Preguntas de descubrimiento") + "".join(
        p(span("?  ", 9, DORADO, True) + span(q, 10), despues=3) for q in pr["preguntas"])
    h += etiqueta("Frase de cierre") + p(span(pr["cierre"], color=AZUL, italic=True))
    h += etiqueta("Objeción típica") + p(span(pr["objecion"], 10))
    return h + caja("Tip del asesor", pr["tip"], borde=VERDE, color_t=VERDE)


def s04():
    h = seccion("04", "Producto por producto: speech y reglas", "Para cada producto: qué es, qué incluye, sus reglas y cómo presentarlo.")
    for i, pr in enumerate(C.PRODUCTOS):
        h += (salto() if i else "") + ficha(pr)
        if pr["corto"] == "Jardín Ecológico":
            h += fig_ciclo()
    h += salto() + sub("Portafolio existente: columbarios (−15% en Finados y noviembre)")
    h += p(span(C.INTRO_EXISTENTES)) + caja("Ubicación definida o a futuro", C.UBICACION_DEFINIDA_FUTURO, fondo=CREMA)
    for i, pr in enumerate(C.PRODUCTOS_EXISTENTES):
        h += (salto() if i else "") + ficha(pr)
    return h + salto()


def s05():
    h = seccion("05", "Manejo de objeciones", "Una objeción no es un \"no\": es una duda que aún no resolvimos.") + fig_vra()
    for i, (obj, val, rep, ava) in enumerate(C.OBJECIONES, start=1):
        filas = [[(p(span(f"{i}.  {obj}", 11, "#FFFFFF", True), despues=0), bg(AZUL)), ("", bg(AZUL))]]
        for letra, nombre, txt in (("V", "Validar", f"\"{val}\""), ("R", "Reposicionar", rep), ("A", "Avanzar", f"\"{ava}\"")):
            filas.append([(p(span(letra + "  ", 12, DORADO, True, font=TIT) + span(nombre, 9, AZUL, True), despues=0),
                           bg(CLARO) + "border-bottom:1pt solid #D9DEE4"),
                          (p(span(txt, 10, italic=(letra != "R")), despues=0), "border-bottom:1pt solid #D9DEE4")])
        h += tabla(filas, ["22%", "78%"])
    return h + salto()


def s06():
    h = seccion("06", "Precios, reglas y condiciones", "Fuente oficial: Ficha Técnica de Cremación vigente. Precios en US$ con IVA incluido.")
    h += tabla_datos(["Producto", "Precio", "Forma de pago", "Mantenimiento", "Plazo / condición"],
                     [list(f) for f in C.TABLA_PRECIOS], ["20%", "15%", "24%", "16%", "25%"],
                     resaltar=lambda f: f[0] == "Jardín Ceremonial")
    h += sub("Portafolio existente: columbarios")
    h += tabla_datos(["Producto", "Precio", "Finados y noviembre (−15%)", "Capacidad", "Incluye"],
                     [list(f) for f in C.TABLA_PRECIOS_EXISTENTES], ["17%", "27%", "24%", "11%", "21%"])
    h += p(span(C.NOTA_EXISTENTES, 9.5, GRIS, italic=True), antes=4)
    h += sub("Reglas comerciales") + tabla_datos(["Tema", "Regla"], [list(r) for r in C.REGLAS_COMERCIALES], ["24%", "76%"])
    return h + caja("El descuento no es la salida", C.DESCUENTO_NO_ES_SALIDA, fondo=CREMA) + salto()


def s07():
    h = seccion("07", "Política de comisiones de los productos de cremación")
    h += caja(C.COMISION_TITULO, C.COMISION_RESUMEN, fondo=CREMA, borde="#B8860B", color_t="#B8860B")
    h += tabla_datos(["Ventas en el mes", "% comisión", "Ejemplo: facturación (Solución Modular)", "Comisión del ejemplo"],
                     [list(f) for f in C.ESCALA_COMISION], ["24%", "18%", "32%", "26%"])
    h += fig_comisiones()
    h += sub("Cuándo se paga y cuándo se descuenta")
    h += tabla_datos(["Producto", "Cuándo se paga", "Estorno"], [list(f) for f in C.COMISIONES], ["30%", "44%", "26%"])
    h += sub("Reglas de comisión") + "".join(p(span("■  ", 7.5, DORADO) + span(r), despues=3) for r in C.REGLAS_COMISION)
    return h + caja("Por qué la comisión está ligada al cobro", C.COMISION_CUIDADO) + salto()


def s08():
    h = seccion("08", "Herramientas de apoyo")
    h += tabla_datos(["Herramienta", "Para qué sirve"], [list(x) for x in C.HERRAMIENTAS], ["30%", "70%"])
    h += sub("Checklist antes de cerrar") + "".join(p(span("☐  ", 12, AZUL) + span(x), despues=4) for x in C.CHECKLIST_CIERRE)
    cierre = (p(span(C.CIERRE_FRASE, 14, "#FFFFFF", italic=True, font=TIT), "center", despues=10)
              + p(span(C.MARCAS, 9.5, DORADO, True), "center", despues=0))
    return h + p("", despues=20) + tabla([[(cierre, bg(AZUL) + f"padding:20pt;border-bottom:5pt solid {DORADO}")]])


def main():
    cuerpo = portada() + como_usar() + s01() + s02() + s03() + s04() + s05() + s06() + s07() + s08()
    doc = (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{e(C.TITULO)} · {e(C.SUBTITULO)}</title>'
           + "<style>" + "".join(f".{c}{{{est}}}" for est, c in CLASES.items()) + "</style>"
           f'</head><body style="font-family:{CUE};color:{TEXTO}">{cuerpo}</body></html>')
    SALIDA.parent.mkdir(exist_ok=True)
    SALIDA.write_text(doc, encoding="utf-8")
    print(f"✔ {SALIDA} ({SALIDA.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
