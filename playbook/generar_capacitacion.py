"""
Genera la presentación de la Capacitación Comercial (16:9, sesión online de 80–90 min) para
importar en Canva, a partir de contenido.py. Es un material interno: sigue el padrón visual de
Mil Advisory (modelo "Crematorios El Salvador": Montserrat, azul marino y amarillo).
No incluye el Jardín Ceremonial (no se presenta en Canva).

Uso:  python3 playbook/generar_capacitacion.py
      ->  playbook/salida/Capacitacion_Comercial_Cremacion_Vangrupo.pptx

Los logos de Mil Advisory (playbook/logos/mil_advisory_*.png) no se versionan: descárguelos del
Drive antes de ejecutar. Si faltan, la presentación se genera sin ellos.
"""
import sys
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu

sys.path.insert(0, str(Path(__file__).parent))
import contenido as C  # noqa: E402
import figuras as F  # noqa: E402
import generar_pptx as G  # noqa: E402
import paleta as P  # noqa: E402

BASE = Path(__file__).parent
LOGOS = BASE / "logos"
SALIDA = BASE / "salida" / "Capacitacion_Comercial_Cremacion_Vangrupo.pptx"
TITULO = "Capacitación Comercial"
PIE = "Capacitación Comercial · Portafolio de Cremación · Oct/2026"

# padrón Mil Advisory (modelo "Crematorios El Salvador")
NAVY = "22263E"       # títulos, fondos oscuros
AZUL_OSC = "022952"   # tarjetas de precio y destacados
AZUL = "20578B"       # etiquetas y numeración
AMARILLO = "FCB832"   # acento: barras, pastillas, etiquetas sobre fondo oscuro
GRIS_T = "4A5170"     # texto secundario
GRIS_P = "6B7390"     # pie de página
CLARO_T = "D3DBEC"    # texto sobre fondo oscuro
FONDO = "FDFBFB"
FILA = "EEF1F7"       # filas alternas y cajas suaves
BORDE = "DDE2EC"
BLANCO = "FFFFFF"
FUENTE = "Montserrat"

W, H = G.W, G.H
X0, ANCHO = 128, 1664  # margen izquierdo y ancho útil, en px de un lienzo de 1920 × 1080

NUEVOS = [p for p in C.PRODUCTOS if not p.get("proximo")]
EXISTENTES = C.PRODUCTOS_EXISTENTES

AGENDA = [  # (bloque, tema, minutos)
    ("00", "Bienvenida y objetivos", 5),
    ("01", "El concepto: qué vendemos", 8),
    ("02", "Por qué vender los nuevos productos", 7),
    ("03", "Los productos, uno a uno", 25),
    ("04", "Política de comisiones", 10),
    ("05", "Técnicas de venta", 10),
    ("06", "Manejo de objeciones", 10),
    ("07", "Dudas y cierre", 10),
]
MINUTOS = dict((num, m) for num, _, m in AGENDA)


# ---------------------------------------------------------------------------
# primitivas (coordenadas en px de 1920 × 1080)
# ---------------------------------------------------------------------------
def px(v):
    return Emu(int(v * 6350))


def caja(s, x, y, w, h, fondo=None, borde=None, forma=MSO_SHAPE.RECTANGLE, radio=None):
    sh = G.caja(s, px(x), px(y), px(w), px(h), fondo=fondo, borde=borde, forma=forma, grosor=1.0)
    if radio is not None:
        sh.adjustments[0] = radio
    return sh


def texto(s, x, y, w, h, contenido, *, size=14, color=NAVY, espaciado=None, **k):
    tb = G.texto(s, px(x), px(y), px(w), px(h), contenido, size=size, color=color, font=FUENTE, **k)
    if espaciado:  # espaciado entre letras, en centésimas de punto (como las etiquetas del modelo)
        for r in tb._element.iter(qn("a:rPr")):
            r.set("spc", str(espaciado))
    return tb


def lista(items, marca="•", color=AZUL, size=13):
    return G.lista(items, marca=marca, color_marca=color, size=size)


def imagen(s, ruta, x, y, w=None, h=None):
    ancho, alto = Image.open(ruta).size
    if w and h:  # encajar dentro de la caja, centrado
        esc = min(w / ancho, h / alto)
        ww, hh = ancho * esc, alto * esc
        return s.shapes.add_picture(str(ruta), px(x + (w - ww) / 2), px(y + (h - hh) / 2), px(ww), px(hh))
    return s.shapes.add_picture(str(ruta), px(x), px(y), px(w) if w else None, px(h) if h else None)


def logo_mil(s, x, y, w, oscuro=False):
    ruta = LOGOS / ("mil_advisory_blanco.png" if oscuro else "mil_advisory_azul.png")
    if ruta.exists():
        imagen(s, ruta, x, y, w=w)


def notas(s, texto_notas):
    s.notes_slide.notes_text_frame.text = texto_notas


def nueva(prs, fondo=FONDO):
    return G.nueva(prs, fondo)


def etiqueta(s, x, y, w, txt, color=AZUL, size=11):
    return texto(s, x, y, w, 34, txt.upper(), size=size, bold=True, color=color, espaciado=150)


def pastilla(s, x, y, w, h, txt, fondo=AMARILLO, color=NAVY, size=14):
    caja(s, x, y, w, h, fondo=fondo, forma=MSO_SHAPE.ROUNDED_RECTANGLE, radio=0.5)
    texto(s, x, y, w, h, txt, size=size, bold=True, color=color, alinear=PP_ALIGN.CENTER, ancla=MSO_ANCHOR.MIDDLE)


def tarjeta(s, x, y, w, h, titulo, cuerpo, *, size_t=15, size_c=12, fondo=BLANCO, barra=AMARILLO):
    caja(s, x, y, w, h, fondo=fondo, borde=BORDE, forma=MSO_SHAPE.ROUNDED_RECTANGLE, radio=0.04)
    if barra:
        caja(s, x + 24, y + 24, 56, 6, fondo=barra)
    texto(s, x + 20, y + 42, w - 40, 70, titulo, size=size_t, bold=True, color=NAVY, interlineado=1.05)
    texto(s, x + 20, y + 112, w - 40, h - 124, cuerpo, size=size_c, color=GRIS_T)


def tabla(s, x, y, w, encabezados, filas, anchos, *, size=11, alto_fila=60, alto_cab=46):
    t = s.shapes.add_table(len(filas) + 1, len(encabezados), px(x), px(y), px(w),
                           px(alto_cab + alto_fila * len(filas))).table
    total = sum(anchos)
    for i, a in enumerate(anchos):
        t.columns[i].width = px(w * a / total)
    for r in range(len(filas) + 1):
        t.rows[r].height = px(alto_cab if r == 0 else alto_fila)
        for c in range(len(encabezados)):
            celda = t.cell(r, c)
            celda.margin_left = celda.margin_right = px(12)
            celda.margin_top = celda.margin_bottom = px(5)
            celda.vertical_anchor = MSO_ANCHOR.MIDDLE
            if r == 0:
                valor, fondo, color, negrita = encabezados[c], NAVY, BLANCO, True
            else:
                valor = filas[r - 1][c]
                fondo = FILA if r % 2 == 1 else BLANCO
                color, negrita = (NAVY, True) if c == 0 else (GRIS_T, False)
            celda.fill.solid()
            celda.fill.fore_color.rgb = G.rgb(fondo)
            p = celda.text_frame.paragraphs[0]
            celda.text_frame.word_wrap = True
            run = p.add_run()
            run.text = valor
            run.font.name, run.font.size, run.font.bold = FUENTE, G.Pt(size), negrita
            run.font.color.rgb = G.rgb(color)
    return t


def rombos(s, x=1748, y=44):
    caja(s, x, y, 44, 44, fondo=NAVY, forma=MSO_SHAPE.DIAMOND)
    caja(s, x, y + 44, 44, 44, fondo=CLARO_T, forma=MSO_SHAPE.DIAMOND)


def encabezado(s, kicker, titulo, intro="", pill=""):
    """Cabecera del modelo: logo, pastilla y rombos arriba; etiqueta, título y barra amarilla."""
    logo_mil(s, X0, 52, 204)
    if pill:
        pastilla(s, 1423, 48, 273, 75, pill)
    rombos(s)
    etiqueta(s, X0, 118, 1250, kicker)
    texto(s, X0, 150, 1560, 84, titulo, size=28, bold=True, interlineado=1.05)
    caja(s, X0, 236, 120, 8, fondo=AMARILLO)
    if intro:
        texto(s, X0, 258, ANCHO, 70, intro, size=13, color=GRIS_T)


def pie(s, n, oscuro=False):
    texto(s, X0, 982, 168, 38, f"{n:02d}", size=12, bold=True, color=AMARILLO if oscuro else AZUL)
    texto(s, 865, 982, 927, 38, PIE, size=12, color=CLARO_T if oscuro else GRIS_P, alinear=PP_ALIGN.RIGHT)


def separador(prs, n, num, titulo, frase):
    s = nueva(prs, NAVY)
    caja(s, 0, 0, 1920, 1080, fondo=NAVY)
    caja(s, 1180, 0, 740, 1080, fondo=AZUL_OSC)
    for i, (dx, dy, tam, color) in enumerate([(1420, 300, 260, AMARILLO), (1600, 480, 200, CLARO_T),
                                              (1330, 560, 150, AZUL)]):
        caja(s, dx, dy, tam, tam, fondo=color, forma=MSO_SHAPE.DIAMOND)
    logo_mil(s, X0, 64, 240, oscuro=True)
    texto(s, X0, 250, 600, 260, num, size=110, bold=True, color=AMARILLO)
    texto(s, X0, 520, 1000, 200, titulo, size=40, bold=True, color=BLANCO, interlineado=1.05)
    caja(s, X0, 735, 120, 8, fondo=AMARILLO)
    texto(s, X0, 765, 1000, 90, frase, size=16, italic=True, color=CLARO_T)
    pastilla(s, X0, 870, 230, 64, f"{MINUTOS[num]} minutos", size=13)
    pie(s, n, oscuro=True)
    return s


# ---------------------------------------------------------------------------
# 00 · Apertura
# ---------------------------------------------------------------------------
def portada(prs):
    s = nueva(prs, NAVY)
    foto = caja(s, 0, 0, 1920, 820, fondo=AZUL_OSC)
    foto.name = "FOTO portada (reemplazar en Canva)"
    for dx, dy, tam, color in [(1330, 250, 300, AZUL), (1560, 400, 220, NAVY), (1450, 560, 130, AMARILLO)]:
        caja(s, dx, dy, tam, tam, fondo=color, forma=MSO_SHAPE.DIAMOND)
    caja(s, 1300, 64, 524, 111, fondo=NAVY, forma=MSO_SHAPE.ROUNDED_RECTANGLE, radio=0.15)
    texto(s, 1336, 80, 465, 44, "CAPACITACIÓN INTERNA", size=13, bold=True, color=AMARILLO, espaciado=50)
    texto(s, 1336, 122, 465, 40, "Octubre / 2026", size=11, color=CLARO_T)
    texto(s, 96, 300, 1150, 60, C.CAMPANA.upper(), size=14, bold=True, color=AMARILLO, espaciado=150)
    texto(s, 96, 360, 1150, 200, "Portafolio de Cremación: lanzamientos y columbarios", size=34,
          bold=True, color=BLANCO, interlineado=1.1)
    texto(s, 96, 560, 1150, 60, "Equipo comercial Vangrupo · Sesión online · 85 minutos", size=16, color=CLARO_T)
    caja(s, 0, 756, 1920, 64, fondo=AMARILLO)
    texto(s, 96, 851, 1250, 105, "CAPACITACIÓN", size=48, bold=True, color=BLANCO, interlineado=1.05)
    texto(s, 96, 952, 1250, 105, "COMERCIAL", size=48, color=BLANCO, interlineado=1.05)
    logo_mil(s, 1430, 885, 380, oscuro=True)
    notas(s, "Abrir la sala 5 minutos antes. Dar la bienvenida a medida que se conectan y "
             "confirmar que todos ven la pantalla.")


def acuerdos(prs, n):
    s = nueva(prs)
    encabezado(s, "Bienvenida", "Acuerdos para la sesión online", pill="Bienvenida")
    items = [
        ("Cámara encendida", "Nos vemos las caras: es una capacitación, no un webinar."),
        ("Micrófono en silencio", "Lo activamos para participar en las prácticas y en las dudas."),
        ("Preguntas en el chat", "Las anotamos y respondemos al final de cada bloque y en el espacio de dudas."),
        ("Material disponible", "El Playbook Comercial y la Ficha Técnica quedan como consulta después de la sesión."),
    ]
    w = (ANCHO - 3 * 32) / 4
    for i, (t, c) in enumerate(items):
        tarjeta(s, X0 + i * (w + 32), 300, w, 320, t, c, size_c=13)
    caja(s, X0, 660, ANCHO, 170, fondo=FILA, forma=MSO_SHAPE.ROUNDED_RECTANGLE, radio=0.08)
    caja(s, X0, 660, 10, 170, fondo=AMARILLO)
    etiqueta(s, X0 + 44, 690, 600, "Tenga a mano")
    texto(s, X0 + 44, 730, ANCHO - 88, 90, "El Playbook Comercial, la Ficha Técnica de Cremación y una "
          "calculadora para el ejercicio de comisiones.", size=16)
    pie(s, n)
    notas(s, "00 · Bienvenida (5 min en total con objetivos y agenda). Presentarse, explicar los "
             "acuerdos y pedir a cada uno que escriba en el chat su nombre y equipo.")


def objetivos(prs, n):
    s = nueva(prs)
    encabezado(s, "Bienvenida", "Al terminar esta capacitación, usted podrá…", pill="Objetivos")
    items = [
        "Explicar el concepto del portafolio de cremación: un lugar para volver, no un producto.",
        "Presentar cada producto con precio, qué incluye, sus reglas y su speech.",
        "Saber por qué los nuevos productos son una oportunidad para la familia y para usted.",
        "Calcular su comisión del mes con la nueva política (8% · 10% · 12%).",
        "Conducir la conversación de venta en 5 pasos, del primer contacto al cierre.",
        "Responder las objeciones más frecuentes con el método V·R·A.",
    ]
    for i, it in enumerate(items):
        y = 310 + i * 104
        caja(s, X0, y, 64, 64, fondo=NAVY, forma=MSO_SHAPE.OVAL)
        texto(s, X0, y, 64, 64, str(i + 1), size=16, bold=True, color=AMARILLO, alinear=PP_ALIGN.CENTER,
              ancla=MSO_ANCHOR.MIDDLE)
        texto(s, X0 + 96, y, ANCHO - 96, 64, it, size=17, ancla=MSO_ANCHOR.MIDDLE)
    pie(s, n)
    notas(s, "Leer los objetivos y preguntar: ¿cuál de estos temas le genera más dudas hoy? "
             "Pedir respuestas en el chat para ajustar el énfasis de la sesión.")


def agenda(prs, n):
    s = nueva(prs)
    encabezado(s, "Bienvenida", "Agenda · 85 minutos", pill="Agenda")
    maximo = max(m for _, _, m in AGENDA)
    for i, (num, tema, m) in enumerate(AGENDA):
        y = 296 + i * 74
        texto(s, X0, y, 90, 60, num, size=20, bold=True, color=AZUL, ancla=MSO_ANCHOR.MIDDLE)
        texto(s, X0 + 100, y, 760, 60, tema, size=15, bold=True, ancla=MSO_ANCHOR.MIDDLE)
        largo = 620 * m / maximo
        caja(s, X0 + 900, y + 16, largo, 28, fondo=AMARILLO if num == "03" else NAVY,
             forma=MSO_SHAPE.ROUNDED_RECTANGLE, radio=0.5)
        texto(s, X0 + 920 + largo, y, 150, 60, f"{m} min", size=13, bold=True, color=GRIS_T, ancla=MSO_ANCHOR.MIDDLE)
        caja(s, X0, y + 70, ANCHO, 2, fondo=BORDE)
    texto(s, X0, 893, ANCHO, 50, f"Total: {sum(m for _, _, m in AGENDA)} minutos, con 5 minutos de margen "
          "para llegar a 1 h 30.", size=12, italic=True, color=GRIS_T)
    pie(s, n)
    notas(s, "Mostrar la agenda y el tiempo de cada bloque. El bloque de productos es el más largo: "
             "pedir que las dudas de precios se dejen en el chat para el bloque 07.")


# ---------------------------------------------------------------------------
# 01 · Concepto
# ---------------------------------------------------------------------------
def concepto(prs, n):
    s = nueva(prs)
    encabezado(s, "01 · El concepto", "No vendemos parcelas: acompañamos familias", pill="Concepto")
    texto(s, X0, 300, 880, 470, C.QUIENES_SOMOS, size=14, color=GRIS_T, interlineado=1.3)
    caja(s, 1060, 300, 732, 470, fondo=AZUL_OSC, forma=MSO_SHAPE.ROUNDED_RECTANGLE, radio=0.05)
    etiqueta(s, 1100, 334, 650, "La pregunta que respondemos", color=AMARILLO)
    texto(s, 1100, 380, 650, 250, "\"¿Y después de la cremación, dónde las visitamos?\"", size=26, bold=True,
          color=BLANCO, ancla=MSO_ANCHOR.MIDDLE, interlineado=1.15)
    texto(s, 1100, 650, 650, 100, "Nuestra respuesta: un jardín o un columbario, un lugar digno y con nombre "
          "para volver.", size=13, color=CLARO_T)
    caja(s, X0, 800, ANCHO, 130, fondo=FILA, forma=MSO_SHAPE.ROUNDED_RECTANGLE, radio=0.1)
    caja(s, X0, 800, 10, 130, fondo=AMARILLO)
    texto(s, X0 + 44, 800, ANCHO - 88, 130,
          [[("REGLA DE ORO   ", {"bold": True, "color": AZUL, "size": 12}),
            (C.REGLA_DE_ORO, {"size": 14, "italic": True})]], ancla=MSO_ANCHOR.MIDDLE)
    pie(s, n)
    notas(s, "01 · Concepto (8 min). Preguntar al grupo: ¿qué hace hoy una familia con las cenizas "
             "después de la cremación? Dejar 2 o 3 respuestas y conectar con la pregunta del slide.")


def momentos(prs, n):
    s = nueva(prs)
    encabezado(s, "01 · El concepto", "Dos momentos de venta, dos actitudes", pill="Concepto")
    w = (ANCHO - 32) / 2
    for i, (t, c) in enumerate(C.MODOS_DE_VENTA):
        tarjeta(s, X0 + i * (w + 32), 300, w, 300, t, c, size_t=18, size_c=15, barra=AMARILLO if i else AZUL)
    etiqueta(s, X0, 640, 1000, "El asesor en cada momento")
    texto(s, X0, 680, ANCHO, 260, lista([
        "Prenecesidad: usted conduce la conversación, planifica con calma y ofrece cuotas.",
        "Necesidad inmediata: usted acoge, informa y resuelve; la venta es consecuencia del cuidado.",
        "En los dos casos: un lugar para volver es lo que la familia compra, no un producto.",
    ], size=15), espacio=10)
    pie(s, n)
    notas(s, "Diferenciar los dos momentos. En necesidad inmediata nunca presionar: Supremo Plus y "
             "Bella Vista ya incluyen la cremación y simplifican la decisión.")


# ---------------------------------------------------------------------------
# 02 · Por qué vender
# ---------------------------------------------------------------------------
def por_que_familia(prs, n):
    s = nueva(prs)
    encabezado(s, "02 · Por qué vender", "Por qué la familia los necesita", pill="Por qué vender")
    w = (ANCHO - 32) / 2
    for i, (t, c) in enumerate(C.POR_QUE_AHORA):
        tarjeta(s, X0 + (i % 2) * (w + 32), 300 + (i // 2) * 322, w, 290, t, c, size_t=18, size_c=15)
    pie(s, n)
    notas(s, "02 · Por qué vender (7 min). Estos son los argumentos de valor para la familia: "
             "volver a un lugar, precio accesible, naturaleza y decidir sin presión.")


def por_que_asesor(prs, n):
    s = nueva(prs)
    encabezado(s, "02 · Por qué vender", "Por qué es una oportunidad para usted", pill="Por qué vender")
    items = [
        ("Campaña de Finados", "Lanzamientos con 20% y columbarios con 15% de descuento, solo en Finados y durante noviembre."),
        ("Una sola decisión", "La Solución Modular resuelve la cremación; un jardín o un columbario resuelve el destino final."),
        ("Su base ya es cliente", "Cada afiliado a un plan funerario puede sumar la Solución Modular sin cambiar de plan."),
        ("Más ventas, más %", "Con 1 venta en el mes gana 8%; con 2, 10%; con 3 o más, 12% de toda la facturación."),
        ("Todo el portafolio", C.EQUIPOS_NOTA),
        ("Entrega a 12 meses", "Al terminar el columbario temporal de la Solución Modular, la familia elige un destino final: una nueva venta."),
    ]
    w = (ANCHO - 64) / 3
    for i, (t, c) in enumerate(items):
        tarjeta(s, X0 + (i % 3) * (w + 32), 296 + (i // 3) * 326, w, 306, t, c, size_t=16, size_c=12.5,
                barra=AZUL if i in (1, 5) else AMARILLO)
    pie(s, n)
    notas(s, "Mostrar que los nuevos productos se complementan: la Solución Modular abre la puerta y "
             "los jardines y columbarios completan la venta. Enlazar con la comisión escalonada.")


# ---------------------------------------------------------------------------
# 03 · Productos
# ---------------------------------------------------------------------------
def figuras_mil():
    """Figuras del playbook con la paleta Mil Advisory (archivos *_mil.png)."""
    F.AZUL, F.AZUL_P, F.DORADO, F.DORADO_B = "#" + NAVY, "#" + AZUL_OSC, "#" + AMARILLO, "#" + AMARILLO
    F.CLARO, F.TEXTO, F.VERDE = "#" + FILA, "#" + NAVY, "#" + AZUL
    P.TERRACOTA, P.APAGADO = AZUL_OSC, GRIS_P
    F.TONO_EMBUDO = "34,38,62"  # NAVY
    F.BASE_CSS = F.BASE_CSS.replace("#" + G.P.PRINCIPAL, "#" + NAVY).replace("#" + G.P.ACENTO, "#" + AMARILLO) \
        .replace("#" + G.P.TEXTO, "#" + NAVY).replace("'Liberation Sans'", "'Montserrat', 'Liberation Sans'")
    original = F.render
    F.render = lambda nombre, *a: original(f"{nombre}_mil", *a)
    try:
        rutas = {"portafolio": F.portafolio("08_portafolio_capacitacion", NUEVOS), "embudo": F.embudo(),
                 "ciclo": F.ciclo()}
    finally:
        F.render = original
    return rutas


def mapa_portafolio(prs, n, fig):
    s = nueva(prs)
    encabezado(s, "03 · Los productos", "El portafolio de cremación completo", pill="Productos")
    imagen(s, fig["portafolio"], X0, 290, ANCHO, 660)
    pie(s, n)
    notas(s, "03 · Productos (25 min). Vista general antes de ir uno a uno: arriba los lanzamientos de "
             "Finados (−20%), abajo los columbarios que ya vendemos (−15%).")


def producto(prs, n, p, nota):
    s = nueva(prs)
    encabezado(s, f"03 · {p['etiqueta']}", p["nombre"], pill="Productos")
    # columna izquierda: precio, qué es, incluye
    xi, wi = X0, 800
    caja(s, xi, 290, wi, 180, fondo=AZUL_OSC, forma=MSO_SHAPE.ROUNDED_RECTANGLE, radio=0.08)
    etiqueta(s, xi + 32, 310, wi - 64, p.get("etiqueta_precio", "Precio de lista"), color=AMARILLO, size=10)
    texto(s, xi + 32, 342, wi - 64, 64, p["precio"], size=26, bold=True, color=BLANCO)
    texto(s, xi + 32, 404, wi - 64, 60, p["pago"], size=10.5, color=CLARO_T)
    texto(s, xi, 486, wi, 140, p["que_es"], size=12.5, italic=True, color=GRIS_T)
    etiqueta(s, xi, 636, wi, "Qué incluye")
    texto(s, xi, 672, wi, 270, lista(p["incluye"], size=12.5), espacio=5)
    # columna derecha: reglas, speech, cierre
    xd, wd = 968, 824
    etiqueta(s, xd, 290, wd, "Reglas que no se negocian")
    texto(s, xd, 326, wd, 260, lista(p["reglas"], marca="▸", size=12), espacio=4)
    caja(s, xd, 596, wd, 224, fondo=BLANCO, borde=BORDE, forma=MSO_SHAPE.ROUNDED_RECTANGLE, radio=0.06)
    caja(s, xd, 596, 10, 224, fondo=AMARILLO)
    etiqueta(s, xd + 36, 608, wd - 60, "Speech", size=10)
    texto(s, xd + 36, 640, wd - 60, 176, p["speech"], size=11, italic=True, color=GRIS_T)
    caja(s, xd, 834, wd, 110, fondo=FILA, forma=MSO_SHAPE.ROUNDED_RECTANGLE, radio=0.1)
    caja(s, xd, 834, 10, 110, fondo=AZUL)
    texto(s, xd + 36, 834, wd - 60, 110, [[("CIERRE   ", {"bold": True, "color": AZUL, "size": 10}),
                                           (p["cierre"], {"size": 12})]], ancla=MSO_ANCHOR.MIDDLE)
    pie(s, n)
    notas(s, f"{p['nombre']} · {nota} Para quién: {p['para_quien']} Tip: {p['tip']}")


def ciclo(prs, n, fig):
    s = nueva(prs)
    encabezado(s, "03 · Jardín Ecológico y de Mascotas", "Cómo explicar el ciclo de 3 años",
               "Transparencia desde la primera conversación: el plazo es parte del valor, no letra chica.",
               pill="Productos")
    imagen(s, fig["ciclo"], X0, 340, ANCHO, 430)
    caja(s, X0, 800, ANCHO, 140, fondo=FILA, forma=MSO_SHAPE.ROUNDED_RECTANGLE, radio=0.1)
    caja(s, X0, 800, 10, 140, fondo=AMARILLO)
    texto(s, X0 + 44, 800, ANCHO - 88, 140,
          [[("OBJECIÓN   ", {"bold": True, "color": AZUL, "size": 11}),
            ("\"¿Y después de 3 años?\" → \"La urna ya se habrá integrado a la tierra, como era el deseo. "
             "El nombre pasa a la placa memorial del monumento, que queda para siempre.\"", {"size": 13})]],
          ancla=MSO_ANCHOR.MIDDLE)
    pie(s, n)
    notas(s, "1 min. Este es el punto que más genera dudas en los jardines de 3 años. Practicar la "
             "frase en voz alta con el grupo.")


def columbarios(prs, n):
    s = nueva(prs)
    encabezado(s, "03 · Portafolio existente", "Columbarios: lo que ya vendemos", C.INTRO_EXISTENTES,
               pill="Productos")
    tabla(s, X0, 375, ANCHO, ["Producto", "Precio de lista", "Finados y noviembre (−15%)", "Capacidad", "Incluye"],
          [tuple(f) for f in C.TABLA_PRECIOS_EXISTENTES], [1.3, 3.0, 2.4, 1.1, 2.3], size=11.5, alto_fila=76)
    texto(s, X0, 815, ANCHO, 80, C.UBICACION_DEFINIDA_FUTURO, size=11.5, italic=True, color=GRIS_T)
    pie(s, n)
    notas(s, "Recordar la diferencia clave: Supremo Plus y Bella Vista incluyen la cremación; Mármol o "
             "Cristal, Ónix y Obra de Arte son solo columbario (la cremación se contrata aparte, por "
             "ejemplo con la Solución Modular).")


def columbarios_speech(prs, n):
    s = nueva(prs)
    encabezado(s, "03 · Portafolio existente", "Columbarios: para quién y cómo presentarlos", pill="Productos")
    w = (ANCHO - 4 * 24) / 5
    for i, p in enumerate(EXISTENTES):
        x = X0 + i * (w + 24)
        caja(s, x, 290, w, 650, fondo=BLANCO, borde=BORDE, forma=MSO_SHAPE.ROUNDED_RECTANGLE, radio=0.04)
        caja(s, x + 22, 312, 56, 6, fondo=AMARILLO)
        texto(s, x + 20, 330, w - 40, 60, p["corto"], size=16, bold=True)
        texto(s, x + 20, 388, w - 40, 40, p["precio"], size=12, bold=True, color=AZUL)
        etiqueta(s, x + 20, 440, w - 40, "Para quién", size=9)
        texto(s, x + 20, 472, w - 40, 230, p["para_quien"], size=11, color=GRIS_T)
        etiqueta(s, x + 20, 700, w - 40, "Tip", size=9)
        texto(s, x + 20, 732, w - 40, 200, p["tip"], size=11, italic=True, color=GRIS_T)
    pie(s, n)
    notas(s, "Recorrer los cinco columbarios en 3 minutos. El speech completo de cada uno está en el "
             "Playbook Comercial, sección 04.")


def precios(prs, n):
    s = nueva(prs)
    encabezado(s, "03 · Precios y reglas", "Lanzamientos de Finados: precios y condiciones",
               "Precios sugeridos en US$ con IVA incluido. Consulte siempre la Ficha Técnica vigente.",
               pill="Productos")
    filas = [f for f in C.TABLA_PRECIOS if f[0] != "Jardín Ceremonial"]
    tabla(s, X0, 330, ANCHO, ["Producto", "Precio · lanzamiento (−20%)", "Pago", "Mantenimiento", "Plazo y notas"],
          filas, [1.5, 2.3, 1.9, 1.2, 3.2], size=11.5, alto_fila=66)
    etiqueta(s, X0, 726, 1000, "Reglas comerciales clave")
    reglas = dict(C.REGLAS_COMERCIALES)
    texto(s, X0, 762, ANCHO, 180, lista([
        reglas["Descuentos"],
        "No se promete: descuentos fuera de política, ubicaciones sin confirmar disponibilidad ni un valor de cuota.",
    ], size=11.5), espacio=4)
    pie(s, n)
    notas(s, "Recordar que el mantenimiento no es opcional y se explica antes de firmar. "
             f"{C.DESCUENTO_NO_ES_SALIDA}")


# ---------------------------------------------------------------------------
# 04 · Comisiones
# ---------------------------------------------------------------------------
def comisiones(prs, n):
    s = nueva(prs)
    encabezado(s, "04 · Política de comisiones de los productos de cremación", "Comisión: 8% · 10% · 12%",
               "Según la cantidad de ventas del mes (cualquier producto), sobre toda la facturación sin IVA.",
               pill="Comisiones")
    w = (ANCHO - 64) / 3
    for i, (ventas, pct, fact, com) in enumerate(C.ESCALA_COMISION):
        x, oscuro = X0 + i * (w + 32), i == 2
        caja(s, x, 340, w, 320, fondo=AZUL_OSC if oscuro else BLANCO, borde=None if oscuro else BORDE,
             forma=MSO_SHAPE.ROUNDED_RECTANGLE, radio=0.06)
        etiqueta(s, x, 368, w, ventas, color=AMARILLO if oscuro else AZUL, size=12)
        s.shapes[-1].text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        texto(s, x, 410, w, 150, pct, size=56, bold=True, color=BLANCO if oscuro else NAVY, alinear=PP_ALIGN.CENTER)
        texto(s, x + 20, 575, w - 40, 70, f"Ej.: {fact} facturados → {com}", size=12,
              color=CLARO_T if oscuro else GRIS_T, alinear=PP_ALIGN.CENTER)
    texto(s, X0, 700, ANCHO, 240, lista(C.REGLAS_COMISION[:4], size=13), espacio=6)
    pie(s, n)
    notas(s, "04 · Comisiones (10 min). El porcentaje se define por la cantidad de contratos del mes y "
             "se aplica sobre TODA la facturación del mes. Ejemplo con Soluciones Modulares a US$ 885 "
             "sin IVA cada una. No hay bonos adicionales.")


def comisiones_pago(prs, n):
    s = nueva(prs)
    encabezado(s, "04 · Política de comisiones de los productos de cremación", "Cuándo se paga y cuándo se descuenta",
               pill="Comisiones")
    tabla(s, X0, 290, ANCHO, ["Producto", "Cuándo se paga", "Estorno"], C.COMISIONES, [2.2, 4.0, 2.6], size=13,
          alto_fila=72)
    texto(s, X0, 650, ANCHO, 160, lista(C.REGLAS_COMISION[4:], size=13), espacio=6)
    caja(s, X0, 830, ANCHO, 110, fondo=FILA, forma=MSO_SHAPE.ROUNDED_RECTANGLE, radio=0.12)
    caja(s, X0, 830, 10, 110, fondo=AMARILLO)
    texto(s, X0 + 44, 830, ANCHO - 88, 110, C.COMISION_CUIDADO, size=12.5, italic=True, ancla=MSO_ANCHOR.MIDDLE)
    pie(s, n)
    notas(s, "Explicar el estorno con un ejemplo: si el cliente cancela, la comisión se descuenta de los "
             "pagos siguientes. Por eso calificar bien al cliente protege su comisión.")


def ejercicio_comision(prs, n):
    s = nueva(prs)
    encabezado(s, "04 · Ejercicio", "¿Cuánto gana Ana este mes?",
               "Calcule en 2 minutos y escriba su respuesta en el chat.", pill="Comisiones")
    caja(s, X0, 340, 800, 440, fondo=BLANCO, borde=BORDE, forma=MSO_SHAPE.ROUNDED_RECTANGLE, radio=0.05)
    etiqueta(s, X0 + 40, 370, 700, "El caso")
    texto(s, X0 + 40, 412, 720, 350, lista([
        "Ana vende en el mes 1 Solución Modular y 1 Jardín Individual, a precio de lista.",
        "Facturación sin IVA: US$ 885 + US$ 531 = US$ 1.416.",
        "¿Cuántas ventas son? ¿Qué porcentaje aplica? ¿Cuánto es su comisión?",
    ], size=15), espacio=12)
    caja(s, 968, 340, 824, 440, fondo=AZUL_OSC, forma=MSO_SHAPE.ROUNDED_RECTANGLE, radio=0.05)
    etiqueta(s, 1008, 370, 740, "La respuesta", color=AMARILLO)
    texto(s, 1008, 415, 740, 110, "2 ventas = 10%", size=36, bold=True, color=BLANCO)
    texto(s, 1008, 540, 740, 70, "10% × US$ 1.416 = US$ 141,60", size=20, bold=True, color=AMARILLO)
    texto(s, 1008, 630, 740, 120, "Con una tercera venta en el mes, el 12% se aplica sobre toda la facturación.",
          size=13, color=CLARO_T)
    texto(s, X0, 810, ANCHO, 80, "Valores de ejemplo a precio de lista. La base real es la facturación sin IVA, "
          "neta de descuentos, y se paga sobre lo cobrado.", size=11, italic=True, color=GRIS_T)
    pie(s, n)
    notas(s, "Mostrar primero solo el caso (tapar la respuesta o revelarla después de las respuestas en "
             "el chat). Preguntar: ¿qué pasa si Ana cierra una tercera venta?")


# ---------------------------------------------------------------------------
# 05 · Técnicas de venta
# ---------------------------------------------------------------------------
def perfiles(prs, n):
    s = nueva(prs)
    encabezado(s, "05 · Técnicas de venta", "A quién le vendemos: 5 perfiles", pill="Técnicas")
    tabla(s, X0, 290, ANCHO, ["Perfil", "Quién es", "Qué busca", "Cómo hablarle", "Producto ideal"],
          [tuple(p) for p in C.PERFILES], [1.5, 1.7, 2.2, 1.7, 3.2], size=11, alto_fila=104)
    texto(s, X0, 860, ANCHO, 90, C.FILTRO_CALIFICACION, size=11, italic=True, color=GRIS_T)
    pie(s, n)
    notas(s, "05 · Técnicas (10 min). Preguntar: ¿qué perfil atienden más en su equipo? Identificar el "
             "perfil define el tono y el producto que se ofrece primero.")


def embudo(prs, n, fig):
    s = nueva(prs)
    encabezado(s, "05 · Técnicas de venta", "El camino de la venta: del contacto a la posventa", pill="Técnicas")
    imagen(s, fig["embudo"], X0, 290, ANCHO, 660)
    pie(s, n)
    notas(s, "Destacar dos pasos: primer contacto en menos de 1 hora y la visita al jardín o al "
             "columbario siempre que sea posible. Un contacto no registrado no existe.")


def conversacion(prs, n):
    s = nueva(prs)
    encabezado(s, "05 · Técnicas de venta", "La conversación en 5 pasos", pill="Técnicas")
    w = (ANCHO - 4 * 24) / 5
    for i, (t, c) in enumerate(C.CONVERSACION):
        x = X0 + i * (w + 24)
        caja(s, x, 290, w, 370, fondo=NAVY if i % 2 == 0 else AZUL_OSC, forma=MSO_SHAPE.ROUNDED_RECTANGLE,
             radio=0.05)
        texto(s, x, 310, w, 100, str(i + 1), size=40, bold=True, color=AMARILLO, alinear=PP_ALIGN.CENTER)
        texto(s, x + 20, 420, w - 40, 60, t, size=16, bold=True, color=BLANCO, alinear=PP_ALIGN.CENTER)
        texto(s, x + 20, 490, w - 40, 160, c, size=12, color=CLARO_T, alinear=PP_ALIGN.CENTER)
    etiqueta(s, X0, 690, 1200, "Preguntas que abren la conversación")
    preguntas = [NUEVOS[0]["preguntas"][0], NUEVOS[1]["preguntas"][0], EXISTENTES[0]["preguntas"][0],
                 NUEVOS[0]["preguntas"][2]]
    texto(s, X0, 728, ANCHO, 220, lista(preguntas, marca="?", size=13), espacio=5)
    pie(s, n)
    notas(s, "Más preguntas que afirmaciones: la solución nace de la escucha. Hablar de tranquilidad, "
             "cuidado y memoria, no de producto. Cerrar siempre con un siguiente paso claro.")


# ---------------------------------------------------------------------------
# 06 · Objeciones
# ---------------------------------------------------------------------------
def metodo(prs, n):
    s = nueva(prs)
    encabezado(s, "06 · Manejo de objeciones", "El método V·R·A", C.PRINCIPIO_OBJECIONES, pill="Objeciones")
    w = (ANCHO - 64) / 3
    for i, (t, c) in enumerate(C.METODO_OBJECIONES):
        x = X0 + i * (w + 32)
        caja(s, x, 340, w, 400, fondo=BLANCO, borde=BORDE, forma=MSO_SHAPE.ROUNDED_RECTANGLE, radio=0.05)
        caja(s, x + (w - 120) / 2, 370, 120, 120, fondo=[NAVY, AMARILLO, AZUL][i], forma=MSO_SHAPE.OVAL)
        texto(s, x + (w - 120) / 2, 370, 120, 120, t[0], size=40, bold=True, color=NAVY if i == 1 else BLANCO,
              alinear=PP_ALIGN.CENTER, ancla=MSO_ANCHOR.MIDDLE)
        texto(s, x, 510, w, 60, t, size=20, bold=True, alinear=PP_ALIGN.CENTER)
        texto(s, x + 40, 580, w - 80, 150, c, size=14, color=GRIS_T, alinear=PP_ALIGN.CENTER)
    caja(s, X0, 780, ANCHO, 140, fondo=NAVY, forma=MSO_SHAPE.ROUNDED_RECTANGLE, radio=0.1)
    texto(s, X0 + 40, 780, ANCHO - 80, 140, "Una objeción no es un \"no\": es una duda que aún no resolvimos.",
          size=18, italic=True, bold=True, color=BLANCO, ancla=MSO_ANCHOR.MIDDLE, alinear=PP_ALIGN.CENTER)
    pie(s, n)
    notas(s, "06 · Objeciones (10 min). Validar la emoción, reposicionar sin discutir y avanzar con un "
             "paso concreto y amable.")


def objeciones(prs, n, grupo, titulo):
    s = nueva(prs)
    encabezado(s, "06 · Manejo de objeciones", titulo, pill="Objeciones")
    tabla(s, X0, 290, ANCHO, ["La objeción", "Validar", "Reposicionar", "Avanzar"], grupo,
          [2.0, 1.9, 4.6, 2.1], size=11, alto_fila=150)
    pie(s, n)
    notas(s, "Leer en voz alta cada objeción y pedir a un participante que la responda antes de mostrar "
             "la respuesta sugerida.")


def practica(prs, n):
    s = nueva(prs)
    encabezado(s, "06 · Práctica", "Role-play en parejas · 5 minutos",
               "En salas separadas: uno es el asesor, el otro es la familia. Después cambian de rol.",
               pill="Objeciones")
    casos = [
        ("Caso A · El Hijo Cuidador", "Busca la Solución Modular para sus padres y dice: \"Está caro\"."),
        ("Caso B · La familia católica", "Le interesa el Jardín Individual, pero cree que la cremación no está permitida."),
        ("Caso C · Las cenizas en casa", "Tiene las cenizas en casa hace un año y no ve por qué llevarlas a un columbario."),
    ]
    w = (ANCHO - 64) / 3
    for i, (t, c) in enumerate(casos):
        tarjeta(s, X0 + i * (w + 32), 340, w, 320, t, c, size_t=16, size_c=14)
    etiqueta(s, X0, 690, 1200, "Al volver a la sala principal")
    texto(s, X0, 728, ANCHO, 220, lista([
        "¿Qué frase de validación usó?",
        "¿Cómo reposicionó el valor sin discutir?",
        "¿Cuál fue el siguiente paso que propuso (visita, propuesta o firma)?",
    ], size=14), espacio=6)
    pie(s, n)
    notas(s, "Abrir salas de 2 personas por 5 minutos (2,5 por rol). Al volver, pedir a 2 parejas que "
             "compartan su respuesta.")


# ---------------------------------------------------------------------------
# 07 · Dudas y cierre
# ---------------------------------------------------------------------------
def checklist(prs, n):
    s = nueva(prs)
    encabezado(s, "07 · Antes de firmar", "Checklist de cierre", pill="Cierre")
    texto(s, X0, 300, 1040, 640, lista(C.CHECKLIST_CIERRE, marca="☐", size=15), espacio=14)
    caja(s, 1210, 290, 582, 650, fondo=FILA, forma=MSO_SHAPE.ROUNDED_RECTANGLE, radio=0.04)
    etiqueta(s, 1246, 318, 520, "Herramientas")
    texto(s, 1246, 360, 520, 570,
          [[(f"{t}\n", {"bold": True, "color": NAVY, "size": 12}), (c, {"size": 11, "color": GRIS_T})]
           for t, c in C.HERRAMIENTAS], espacio=8)
    pie(s, n)
    notas(s, "07 · Dudas y cierre (10 min). Repasar el checklist rápidamente: es lo que evita "
             "cancelaciones y estornos.")


def dudas(prs, n):
    s = nueva(prs, NAVY)
    caja(s, 1180, 0, 740, 1080, fondo=AZUL_OSC)
    for dx, dy, tam, color in [(1420, 300, 260, AMARILLO), (1600, 480, 200, CLARO_T), (1330, 560, 150, AZUL)]:
        caja(s, dx, dy, tam, tam, fondo=color, forma=MSO_SHAPE.DIAMOND)
    logo_mil(s, X0, 64, 240, oscuro=True)
    texto(s, X0, 230, 1000, 200, "¿DUDAS?", size=80, bold=True, color=AMARILLO)
    caja(s, X0, 455, 120, 8, fondo=AMARILLO)
    texto(s, X0, 480, 1000, 110, "Espacio abierto para preguntas: productos, precios, comisiones y casos reales.",
          size=20, color=BLANCO)
    temas = ["Productos y reglas", "Precios y descuentos", "Comisiones", "Casos de clientes"]
    for i, t in enumerate(temas):
        pastilla(s, X0 + (i % 2) * 470, 610 + (i // 2) * 100, 440, 76, t, size=14)
    texto(s, X0, 830, 1000, 90, "Las preguntas del chat que no alcancemos a responder se contestan por escrito "
          "después de la sesión.", size=13, italic=True, color=CLARO_T)
    pie(s, n, oscuro=True)
    notas(s, "Responder primero las preguntas acumuladas en el chat, agrupadas por tema. Anotar las que "
             "requieren validación de la Gerencia Comercial.")


def cierre(prs):
    s = nueva(prs, NAVY)
    foto = caja(s, 1180, 0, 740, 1080, fondo=AZUL_OSC)
    foto.name = "FOTO cierre (reemplazar en Canva)"
    for dx, dy, tam, color in [(1420, 300, 260, AMARILLO), (1600, 480, 200, CLARO_T), (1330, 560, 150, AZUL)]:
        caja(s, dx, dy, tam, tam, fondo=color, forma=MSO_SHAPE.DIAMOND)
    logo_mil(s, X0, 64, 240, oscuro=True)
    texto(s, X0, 220, 1000, 200, "¡GRACIAS!", size=80, bold=True, color=AMARILLO)
    caja(s, X0, 445, 120, 8, fondo=AMARILLO)
    texto(s, X0, 475, 1000, 250, f"\"{C.CIERRE_FRASE}\"", size=22, italic=True, color=BLANCO, interlineado=1.3)
    texto(s, X0, 760, 1000, 50, "¡Buenas ventas!", size=20, bold=True, color=AMARILLO)
    texto(s, X0, 820, 1000, 50, C.MARCAS, size=13, color=CLARO_T)
    texto(s, X0, 982, 1000, 38, PIE, size=12, color=CLARO_T)
    notas(s, "Agradecer, recordar dónde está el material (Playbook Comercial y Ficha Técnica) y el "
             "canal para dudas posteriores.")


def main():
    fig = figuras_mil()
    prs = Presentation()
    prs.slide_width, prs.slide_height = W, H
    n = 2
    portada(prs)
    acuerdos(prs, n); n += 1
    objetivos(prs, n); n += 1
    agenda(prs, n); n += 1
    separador(prs, n, "01", "El concepto: qué vendemos", C.LEMA); n += 1
    concepto(prs, n); n += 1
    momentos(prs, n); n += 1
    separador(prs, n, "02", "Por qué vender los nuevos productos", "Buenos para la familia, buenos para usted."); n += 1
    por_que_familia(prs, n); n += 1
    por_que_asesor(prs, n); n += 1
    separador(prs, n, "03", "Los productos, uno a uno", "Qué es, qué incluye, sus reglas y cómo presentarlo."); n += 1
    mapa_portafolio(prs, n, fig); n += 1
    tiempos = ["4 min.", "3 min.", "3 min.", "3 min.", "3 min."]
    for p, t in zip(NUEVOS, tiempos):
        producto(prs, n, p, t); n += 1
        if p["corto"] == "Jardín Ecológico":
            ciclo(prs, n, fig); n += 1
    columbarios(prs, n); n += 1
    columbarios_speech(prs, n); n += 1
    precios(prs, n); n += 1
    separador(prs, n, "04", "Política de comisiones", "La comisión premia la venta buena, no solo la venta."); n += 1
    comisiones(prs, n); n += 1
    comisiones_pago(prs, n); n += 1
    ejercicio_comision(prs, n); n += 1
    separador(prs, n, "05", "Técnicas de venta", "Conocer al cliente es la mitad de la venta."); n += 1
    perfiles(prs, n); n += 1
    embudo(prs, n, fig); n += 1
    conversacion(prs, n); n += 1
    separador(prs, n, "06", "Manejo de objeciones", "Detrás de cada objeción hay una emoción."); n += 1
    metodo(prs, n); n += 1
    objeciones(prs, n, C.OBJECIONES[:4], "Las objeciones más frecuentes (1/2)"); n += 1
    objeciones(prs, n, C.OBJECIONES[4:], "Las objeciones más frecuentes (2/2)"); n += 1
    practica(prs, n); n += 1
    separador(prs, n, "07", "Dudas y cierre", "Ninguna pregunta queda sin respuesta."); n += 1
    checklist(prs, n); n += 1
    dudas(prs, n); n += 1
    cierre(prs)
    SALIDA.parent.mkdir(exist_ok=True)
    prs.save(SALIDA)
    print(f"✔ {SALIDA} ({len(prs.slides)} diapositivas, {SALIDA.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
