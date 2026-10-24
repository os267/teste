"""
Genera la presentación de la Capacitación Comercial (16:9, sesión online de 80–90 min) para
importar en Canva, a partir de contenido.py y de las figuras de playbook/figuras/.
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
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches

sys.path.insert(0, str(Path(__file__).parent))
import contenido as C  # noqa: E402
import figuras as F  # noqa: E402
import generar_pptx as G  # noqa: E402
import paleta as P  # noqa: E402
from generar_pptx import (AZUL, AZUL_P, BLANCO, CLARO, CREMA, DORADO, GRIS, MX, TEXTO, TITULOS,  # noqa: E402
                          VERDE, H, W, caja, lista, nueva, tabla, tarjeta, texto)

BASE = Path(__file__).parent
LOGOS = BASE / "logos"
SALIDA = BASE / "salida" / "Capacitacion_Comercial_Cremacion_Vangrupo.pptx"
TITULO = "Capacitación Comercial"
SUBTITULO = "Portafolio de Cremación: lanzamientos y columbarios"

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


def tabla_cab(s, x, y, w, encabezados, filas, anchos, *, size=11, alto_fila=Inches(0.42), alto_cab=Inches(0.5)):
    """Como generar_pptx.tabla, pero con la fila de encabezado más baja que las de contenido."""
    t = tabla(s, x, y, w, encabezados, filas, anchos, size=size, alto_fila=alto_fila)
    t.rows[0].height = alto_cab
    return t


def imagen(s, ruta, x, y, w=None, h=None):
    ancho, alto = Image.open(ruta).size
    if w and h:  # encajar dentro de la caja, centrado
        esc = min(w / ancho, h / alto)
        ww, hh = int(ancho * esc), int(alto * esc)
        return s.shapes.add_picture(str(ruta), x + (w - ww) // 2, y + (h - hh) // 2, ww, hh)
    return s.shapes.add_picture(str(ruta), x, y, w, h)


def logo_mil(s, x, y, w, oscuro=False):
    ruta = LOGOS / ("mil_advisory_blanco.png" if oscuro else "mil_advisory_azul.png")
    if ruta.exists():
        imagen(s, ruta, x, y, w=w)


def notas(s, texto_notas):
    s.notes_slide.notes_text_frame.text = texto_notas


def pie(s, n, oscuro=False):
    color = P.TINTE if oscuro else GRIS
    texto(s, MX, H - Inches(0.45), Inches(9), Inches(0.3), f"{TITULO}  ·  {C.MARCAS}", size=9, color=color)
    logo_mil(s, W - MX - Inches(2.05), H - Inches(0.46), Inches(1.35), oscuro)
    texto(s, W - MX - Inches(0.5), H - Inches(0.45), Inches(0.5), Inches(0.3), str(n),
          size=9, color=color, alinear=PP_ALIGN.RIGHT)


def encabezado(s, bloque, seccion, titulo, intro=""):
    G.encabezado(s, f"{bloque} · {seccion}" if bloque else seccion, titulo, intro)


def separador(prs, n, num, titulo, frase):
    s = nueva(prs, AZUL)
    texto(s, MX + Inches(0.4), Inches(1.4), Inches(3.5), Inches(2.1), num, size=110, bold=True,
          color=DORADO, font=TITULOS)
    texto(s, MX + Inches(0.4), Inches(3.6), Inches(11.5), Inches(1.0), titulo, size=40, bold=True,
          color=BLANCO, font=TITULOS)
    caja(s, MX + Inches(0.45), Inches(4.7), Inches(1.4), Inches(0.06), fondo=DORADO)
    texto(s, MX + Inches(0.4), Inches(4.9), Inches(11), Inches(0.8), frase, size=16, italic=True, color=P.TINTE)
    texto(s, MX + Inches(0.4), Inches(5.8), Inches(4), Inches(0.4), f"◷  {MINUTOS[num]} minutos",
          size=13, bold=True, color=DORADO)
    pie(s, n, oscuro=True)
    return s


# ---------------------------------------------------------------------------
# 00 · Apertura
# ---------------------------------------------------------------------------
def portada(prs):
    s = nueva(prs, AZUL)
    caja(s, 0, H - Inches(0.25), W, Inches(0.25), fondo=DORADO)
    logo_mil(s, MX + Inches(0.2), Inches(0.6), Inches(2.6), oscuro=True)
    imagen(s, LOGOS / "vangrupo_blanco.png", W - MX - Inches(2.6), Inches(0.55), w=Inches(2.4))
    texto(s, MX + Inches(0.2), Inches(1.85), Inches(9), Inches(0.4), C.CAMPANA.upper(),
          size=13, bold=True, color=DORADO)
    texto(s, MX + Inches(0.2), Inches(2.3), Inches(12), Inches(1.3), TITULO,
          size=60, bold=True, color=BLANCO, font=TITULOS)
    texto(s, MX + Inches(0.2), Inches(3.6), Inches(11), Inches(0.7), SUBTITULO,
          size=26, color="F1ECF7", font=TITULOS)
    caja(s, MX + Inches(0.25), Inches(4.45), Inches(1.4), Inches(0.06), fondo=DORADO)
    texto(s, MX + Inches(0.2), Inches(4.7), Inches(11), Inches(0.5), f"\"{C.LEMA}\"",
          size=16, italic=True, color=BLANCO, font=TITULOS)
    texto(s, MX + Inches(0.2), Inches(5.9), Inches(11), Inches(0.35), C.MARCAS, size=13, bold=True, color=DORADO)
    texto(s, MX + Inches(0.2), Inches(6.35), Inches(11), Inches(0.35),
          "Equipo comercial · Sesión online · 85 minutos · Octubre 2026", size=11, color=P.TINTE)
    notas(s, "Abrir la sala 5 minutos antes. Dar la bienvenida a medida que se conectan y "
             "confirmar que todos ven la pantalla.")


def acuerdos(prs, n):
    s = nueva(prs)
    encabezado(s, "00", "Bienvenida", "Acuerdos para la sesión online")
    items = [
        ("Cámara encendida", "Nos vemos las caras: es una capacitación, no un webinar."),
        ("Micrófono en silencio", "Lo activamos para participar en las prácticas y en las dudas."),
        ("Preguntas en el chat", "Las anotamos y respondemos al final de cada bloque y en el espacio de dudas."),
        ("Material disponible", "El Playbook Comercial y la Ficha Técnica quedan como consulta después de la sesión."),
    ]
    w, gap = Inches(2.88), Inches(0.2)
    for i, (t, c) in enumerate(items):
        tarjeta(s, MX + i * (w + gap), Inches(2.2), w, Inches(2.2), t, c, size_c=13)
    caja(s, MX, Inches(4.9), W - 2 * MX, Inches(1.4), fondo=CREMA)
    caja(s, MX, Inches(4.9), Inches(0.08), Inches(1.4), fondo=DORADO)
    texto(s, MX + Inches(0.35), Inches(4.9), W - 2 * MX - Inches(0.6), Inches(1.4),
          [[("TENGA A MANO   ", {"bold": True, "color": AZUL, "size": 12}),
            ("El Playbook Comercial, la Ficha Técnica de Cremación y una calculadora para el ejercicio "
             "de comisiones.", {"size": 15})]], ancla=MSO_ANCHOR.MIDDLE)
    pie(s, n)
    notas(s, "00 · Bienvenida (5 min en total con objetivos y agenda). Presentarse, explicar los "
             "acuerdos y pedir a cada uno que escriba en el chat su nombre y equipo.")


def objetivos(prs, n):
    s = nueva(prs)
    encabezado(s, "00", "Bienvenida", "Al terminar esta capacitación, usted podrá…")
    items = [
        "Explicar el concepto del portafolio de cremación: un lugar para volver, no un producto.",
        "Presentar cada producto con precio, qué incluye, sus reglas y su speech.",
        "Saber por qué los nuevos productos son una oportunidad para la familia y para usted.",
        "Calcular su comisión del mes con la nueva política (8% · 10% · 12%).",
        "Conducir la conversación de venta en 5 pasos, del primer contacto al cierre.",
        "Responder las objeciones más frecuentes con el método V·R·A.",
    ]
    texto(s, MX, Inches(2.0), Inches(12), Inches(4.5), lista(items, marca="✔", color_marca=VERDE, size=18),
          espacio=12)
    pie(s, n)
    notas(s, "Leer los objetivos y preguntar: ¿cuál de estos temas le genera más dudas hoy? "
             "Pedir respuestas en el chat para ajustar el énfasis de la sesión.")


def agenda(prs, n):
    s = nueva(prs)
    encabezado(s, "00", "Bienvenida", "Agenda · 85 minutos")
    total = sum(m for _, _, m in AGENDA)
    x0, y0, ancho_total = MX, Inches(2.0), W - 2 * MX
    for i, (num, tema, m) in enumerate(AGENDA):
        y = y0 + i * Inches(0.55)
        texto(s, x0, y, Inches(0.8), Inches(0.5), num, size=22, bold=True, color=DORADO, font=TITULOS)
        texto(s, x0 + Inches(0.85), y + Inches(0.08), Inches(5.6), Inches(0.45), tema, size=15, bold=True,
              color=AZUL)
        largo = int((ancho_total - Inches(8.2)) * m / max(mm for _, _, mm in AGENDA))
        caja(s, x0 + Inches(6.6), y + Inches(0.14), largo, Inches(0.26), fondo=AZUL if num != "03" else VERDE)
        texto(s, x0 + Inches(6.7) + largo, y + Inches(0.08), Inches(1.2), Inches(0.4), f"{m} min",
              size=13, bold=True, color=GRIS)
        caja(s, x0, y + Inches(0.52), ancho_total, Inches(0.01), fondo=P.LINEA)
    texto(s, x0, y0 + len(AGENDA) * Inches(0.55) + Inches(0.1), ancho_total, Inches(0.4),
          f"Total: {total} minutos, con 5 minutos de margen para llegar a 1 h 30.", size=12, italic=True,
          color=GRIS)
    pie(s, n)
    notas(s, "Mostrar la agenda y el tiempo de cada bloque. El bloque de productos es el más largo: "
             "pedir que las dudas de precios se dejen en el chat para el bloque 07.")


# ---------------------------------------------------------------------------
# 01 · Concepto
# ---------------------------------------------------------------------------
def concepto(prs, n):
    s = nueva(prs)
    encabezado(s, "01", "El concepto", "No vendemos parcelas: acompañamos familias")
    texto(s, MX, Inches(1.8), Inches(6.3), Inches(3.8), C.QUIENES_SOMOS, size=15, interlineado=1.25)
    caja(s, Inches(7.25), Inches(1.8), Inches(5.5), Inches(3.6), fondo=AZUL)
    texto(s, Inches(7.55), Inches(1.95), Inches(4.9), Inches(0.4), "LA PREGUNTA QUE RESPONDEMOS",
          size=11, bold=True, color=DORADO)
    texto(s, Inches(7.55), Inches(2.4), Inches(4.9), Inches(2.0),
          "\"¿Y después de la cremación, dónde las visitamos?\"", size=28, italic=True, bold=True,
          color=BLANCO, font=TITULOS, ancla=MSO_ANCHOR.MIDDLE)
    texto(s, Inches(7.55), Inches(4.45), Inches(4.9), Inches(0.8),
          "Nuestra respuesta: un jardín o un columbario, un lugar digno y con nombre para volver.",
          size=13, color=P.TINTE)
    caja(s, MX, Inches(5.8), W - 2 * MX, Inches(0.9), fondo=CREMA)
    texto(s, MX + Inches(0.3), Inches(5.8), W - 2 * MX - Inches(0.6), Inches(0.9),
          [[("REGLA DE ORO   ", {"bold": True, "color": AZUL, "size": 12}),
            (C.REGLA_DE_ORO, {"size": 14, "italic": True})]], ancla=MSO_ANCHOR.MIDDLE)
    pie(s, n)
    notas(s, "01 · Concepto (8 min). Preguntar al grupo: ¿qué hace hoy una familia con las cenizas "
             "después de la cremación? Dejar 2 o 3 respuestas y conectar con la pregunta del slide.")


def momentos(prs, n):
    s = nueva(prs)
    encabezado(s, "01", "El concepto", "Dos momentos de venta, dos actitudes")
    w = Inches(5.9)
    for i, (t, c) in enumerate(C.MODOS_DE_VENTA):
        x = MX + i * (w + Inches(0.33))
        tarjeta(s, x, Inches(1.95), w, Inches(2.4), t, c, size_t=18, size_c=15,
                acento=VERDE if i == 0 else DORADO)
    texto(s, MX, Inches(4.7), Inches(12), Inches(0.4), "EL ASESOR EN CADA MOMENTO", size=11, bold=True,
          color=DORADO)
    texto(s, MX, Inches(5.1), Inches(12), Inches(1.6), lista([
        "Prenecesidad: usted conduce la conversación, planifica con calma y ofrece cuotas.",
        "Necesidad inmediata: usted acoge, informa y resuelve; la venta es consecuencia del cuidado.",
        "En los dos casos: un lugar para volver es lo que la familia compra, no un producto.",
    ], size=15), espacio=8)
    pie(s, n)
    notas(s, "Diferenciar los dos momentos. En necesidad inmediata nunca presionar: Supremo Plus y "
             "Bella Vista ya incluyen la cremación y simplifican la decisión.")


# ---------------------------------------------------------------------------
# 02 · Por qué vender
# ---------------------------------------------------------------------------
def por_que_familia(prs, n):
    s = nueva(prs)
    encabezado(s, "02", "Por qué vender", "Por qué la familia los necesita")
    w, gap = Inches(5.9), Inches(0.33)
    for i, (t, c) in enumerate(C.POR_QUE_AHORA):
        x = MX + (i % 2) * (w + gap)
        y = Inches(1.95) + (i // 2) * Inches(2.25)
        tarjeta(s, x, y, w, Inches(2.0), t, c, size_t=18, size_c=15)
    pie(s, n)
    notas(s, "02 · Por qué vender (7 min). Estos son los argumentos de valor para la familia: "
             "volver a un lugar, precio accesible, naturaleza y decidir sin presión.")


def por_que_asesor(prs, n):
    s = nueva(prs)
    encabezado(s, "02", "Por qué vender", "Por qué es una oportunidad para usted")
    items = [
        ("Campaña de Finados", "Lanzamientos con 20% y columbarios con 15% de descuento, solo en Finados y durante noviembre."),
        ("Una sola decisión", "La Solución Modular resuelve la cremación; un jardín o un columbario resuelve el destino final."),
        ("Su base ya es cliente", "Cada afiliado a un plan funerario puede sumar la Solución Modular sin cambiar de plan."),
        ("Más ventas, más %", "Con 1 venta en el mes gana 8%; con 2, 10%; con 3 o más, 12% de toda la facturación."),
        ("Todo el portafolio", C.EQUIPOS_NOTA),
        ("Entrega a 12 meses", "Al terminar el columbario temporal de la Solución Modular, la familia elige un destino final: una nueva venta."),
    ]
    w, gap = Inches(3.92), Inches(0.2)
    for i, (t, c) in enumerate(items):
        x = MX + (i % 3) * (w + gap)
        y = Inches(1.95) + (i // 3) * Inches(2.35)
        tarjeta(s, x, y, w, Inches(2.15), t, c, size_t=16, size_c=13,
                acento=VERDE if i in (1, 5) else DORADO)
    pie(s, n)
    notas(s, "Mostrar que los nuevos productos se complementan: la Solución Modular abre la puerta y "
             "los jardines y columbarios completan la venta. Enlazar con la comisión escalonada.")


# ---------------------------------------------------------------------------
# 03 · Productos
# ---------------------------------------------------------------------------
def mapa_portafolio(prs, n):
    s = nueva(prs)
    encabezado(s, "03", "Los productos", "El portafolio de cremación completo")
    nombre = "08_portafolio_capacitacion"
    ruta = BASE / "figuras" / f"{nombre}.png"
    if not ruta.exists():
        F.portafolio(nombre, NUEVOS)
    imagen(s, ruta, MX, Inches(1.75), W - 2 * MX, Inches(4.9))
    pie(s, n)
    notas(s, "03 · Productos (25 min). Vista general antes de ir uno a uno: arriba los lanzamientos de "
             "Finados (−20%), abajo los columbarios que ya vendemos (−15%).")


def producto(prs, n, p, nota):
    s = nueva(prs)
    encabezado(s, "03", p["etiqueta"], p["nombre"])
    # columna izquierda: precio, qué es, incluye
    xi, wi = MX, Inches(6.05)
    caja(s, xi, Inches(1.75), wi, Inches(1.3), fondo=AZUL)
    texto(s, xi + Inches(0.25), Inches(1.8), wi - Inches(0.5), Inches(0.5),
          p.get("etiqueta_precio", "PRECIO DE LISTA"), size=10, bold=True, color=DORADO)
    texto(s, xi + Inches(0.25), Inches(2.05), wi - Inches(0.5), Inches(0.5), p["precio"], size=24,
          bold=True, color=BLANCO, font=TITULOS)
    texto(s, xi + Inches(0.25), Inches(2.52), wi - Inches(0.5), Inches(0.5), p["pago"], size=10.5,
          color=P.TINTE)
    texto(s, xi, Inches(3.15), wi, Inches(0.9), p["que_es"], size=13, italic=True, color=TEXTO)
    texto(s, xi, Inches(4.1), wi, Inches(0.35), "QUÉ INCLUYE", size=11, bold=True, color=DORADO)
    texto(s, xi, Inches(4.45), wi, Inches(2.25), lista(p["incluye"], size=12.5), espacio=5)
    # columna derecha: reglas, speech, cierre
    xd, wd = Inches(7.0), W - Inches(7.0) - MX
    texto(s, xd, Inches(1.75), wd, Inches(0.35), "REGLAS QUE NO SE NEGOCIAN", size=11, bold=True, color=DORADO)
    texto(s, xd, Inches(2.1), wd, Inches(1.85), lista(p["reglas"], marca="▸", color_marca=AZUL, size=12),
          espacio=4)
    caja(s, xd, Inches(4.0), wd, Inches(1.75), fondo=CLARO)
    caja(s, xd, Inches(4.0), Inches(0.07), Inches(1.75), fondo=AZUL)
    texto(s, xd + Inches(0.25), Inches(4.05), wd - Inches(0.4), Inches(0.3), "SPEECH", size=10, bold=True,
          color=AZUL)
    texto(s, xd + Inches(0.25), Inches(4.33), wd - Inches(0.4), Inches(1.4), p["speech"], size=11.5,
          italic=True, color=TEXTO)
    caja(s, xd, Inches(5.85), wd, Inches(0.85), fondo=P.CIERRE[1])
    caja(s, xd, Inches(5.85), Inches(0.07), Inches(0.85), fondo=VERDE)
    texto(s, xd + Inches(0.25), Inches(5.85), wd - Inches(0.4), Inches(0.85),
          [[("CIERRE   ", {"bold": True, "color": VERDE, "size": 10}), (p["cierre"], {"size": 12})]],
          ancla=MSO_ANCHOR.MIDDLE)
    pie(s, n)
    notas(s, f"{p['nombre']} · {nota} Para quién: {p['para_quien']} Tip: {p['tip']}")


def ciclo(prs, n):
    s = nueva(prs)
    encabezado(s, "03", "Jardín Ecológico y de Mascotas", "Cómo explicar el ciclo de 3 años",
               "Transparencia desde la primera conversación: el plazo es parte del valor, no letra chica.")
    imagen(s, BASE / "figuras" / "06_ciclo_ecologico.png", MX, Inches(2.2), W - 2 * MX, Inches(3.4))
    caja(s, MX, Inches(5.75), W - 2 * MX, Inches(0.95), fondo=CREMA)
    texto(s, MX + Inches(0.3), Inches(5.75), W - 2 * MX - Inches(0.6), Inches(0.95),
          [[("OBJECIÓN   ", {"bold": True, "color": P.OBJECION[0], "size": 11}),
            ("\"¿Y después de 3 años?\" → \"La urna ya se habrá integrado a la tierra, como era el deseo. "
             "El nombre pasa a la placa memorial del monumento, que queda para siempre.\"", {"size": 13})]],
          ancla=MSO_ANCHOR.MIDDLE)
    pie(s, n)
    notas(s, "1 min. Este es el punto que más genera dudas en los jardines de 3 años. Practicar la "
             "frase en voz alta con el grupo.")


def columbarios(prs, n):
    s = nueva(prs)
    encabezado(s, "03", "Portafolio existente", "Columbarios: lo que ya vendemos", C.INTRO_EXISTENTES)
    filas = [(f[0], f[1], f[2], f[3], f[4]) for f in C.TABLA_PRECIOS_EXISTENTES]
    tabla_cab(s, MX, Inches(2.55), W - 2 * MX, ["Producto", "Precio de lista", "Finados y noviembre (−15%)",
                                            "Capacidad", "Incluye"],
          filas, [1.3, 3.0, 2.4, 1.1, 2.3], size=11.5, alto_fila=Inches(0.58))
    texto(s, MX, Inches(6.15), W - 2 * MX, Inches(0.5), C.UBICACION_DEFINIDA_FUTURO, size=11.5, italic=True,
          color=GRIS)
    pie(s, n)
    notas(s, "Recordar la diferencia clave: Supremo Plus y Bella Vista incluyen la cremación; Mármol o "
             "Cristal, Ónix y Obra de Arte son solo columbario (la cremación se contrata aparte, por "
             "ejemplo con la Solución Modular).")


def columbarios_speech(prs, n):
    s = nueva(prs)
    encabezado(s, "03", "Portafolio existente", "Columbarios: para quién y cómo presentarlos")
    w, gap = Inches(2.3), Inches(0.13)
    for i, p in enumerate(EXISTENTES):
        x = MX + i * (w + gap)
        caja(s, x, Inches(1.85), w, Inches(4.85), fondo=CLARO)
        caja(s, x, Inches(1.85), w, Inches(0.06), fondo=DORADO)
        texto(s, x + Inches(0.15), Inches(2.0), w - Inches(0.3), Inches(0.6), p["corto"], size=16, bold=True,
              color=AZUL, font=TITULOS)
        texto(s, x + Inches(0.15), Inches(2.55), w - Inches(0.3), Inches(0.4), p["precio"], size=12,
              bold=True, color=AZUL_P)
        texto(s, x + Inches(0.15), Inches(3.0), w - Inches(0.3), Inches(0.3), "PARA QUIÉN", size=9,
              bold=True, color=DORADO)
        texto(s, x + Inches(0.15), Inches(3.28), w - Inches(0.3), Inches(1.6), p["para_quien"], size=11)
        texto(s, x + Inches(0.15), Inches(4.85), w - Inches(0.3), Inches(0.3), "TIP", size=9, bold=True,
              color=P.TIP[0])
        texto(s, x + Inches(0.15), Inches(5.12), w - Inches(0.3), Inches(1.55), p["tip"], size=11,
              italic=True)
    pie(s, n)
    notas(s, "Recorrer los cinco columbarios en 3 minutos. El speech completo de cada uno está en el "
             "Playbook Comercial, sección 04.")


def precios(prs, n):
    s = nueva(prs)
    encabezado(s, "03", "Precios y reglas", "Lanzamientos de Finados: precios y condiciones",
               "Precios sugeridos en US$ con IVA incluido. Consulte siempre la Ficha Técnica vigente.")
    filas = [f for f in C.TABLA_PRECIOS if f[0] != "Jardín Ceremonial"]
    tabla_cab(s, MX, Inches(2.25), W - 2 * MX, ["Producto", "Precio · lanzamiento (−20%)", "Pago", "Mantenimiento",
                                            "Plazo y notas"],
          filas, [1.5, 2.3, 1.9, 1.2, 3.2], size=11.5, alto_fila=Inches(0.48))
    texto(s, MX, Inches(5.3), Inches(12), Inches(0.35), "REGLAS COMERCIALES CLAVE", size=11, bold=True,
          color=DORADO)
    reglas = dict(C.REGLAS_COMERCIALES)
    texto(s, MX, Inches(5.62), Inches(12), Inches(1.1), lista([
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
    encabezado(s, "04", "Política de comisiones de los productos de cremación", "Comisión: 8% · 10% · 12%",
               "Según la cantidad de ventas del mes (cualquier producto), sobre toda la facturación sin IVA.")
    w, gap = Inches(3.9), Inches(0.25)
    for i, (ventas, pct, fact, com) in enumerate(C.ESCALA_COMISION):
        x = MX + i * (w + gap)
        caja(s, x, Inches(2.3), w, Inches(2.4), fondo=AZUL if i == 2 else CLARO)
        caja(s, x, Inches(2.3), w, Inches(0.07), fondo=DORADO)
        oscuro = i == 2
        texto(s, x, Inches(2.45), w, Inches(0.4), ventas.upper(), size=13, bold=True,
              color=DORADO if oscuro else AZUL, alinear=PP_ALIGN.CENTER)
        texto(s, x, Inches(2.85), w, Inches(1.1), pct, size=54, bold=True, font=TITULOS,
              color=BLANCO if oscuro else AZUL, alinear=PP_ALIGN.CENTER)
        texto(s, x, Inches(3.95), w, Inches(0.6), f"Ej.: {fact} facturados → {com}", size=12,
              color=P.TINTE if oscuro else GRIS, alinear=PP_ALIGN.CENTER)
    texto(s, MX, Inches(5.0), W - 2 * MX, Inches(1.7), lista(C.REGLAS_COMISION[:4], size=13), espacio=5)
    pie(s, n)
    notas(s, "04 · Comisiones (10 min). El porcentaje se define por la cantidad de contratos del mes y "
             "se aplica sobre TODA la facturación del mes. Ejemplo con Soluciones Modulares a US$ 885 "
             "sin IVA cada una. No hay bonos adicionales.")


def comisiones_pago(prs, n):
    s = nueva(prs)
    encabezado(s, "04", "Política de comisiones de los productos de cremación", "Cuándo se paga y cuándo se descuenta")
    tabla_cab(s, MX, Inches(1.9), W - 2 * MX, ["Producto", "Cuándo se paga", "Estorno"], C.COMISIONES,
          [2.2, 4.0, 2.6], size=13, alto_fila=Inches(0.6))
    texto(s, MX, Inches(5.05), W - 2 * MX, Inches(1.2), lista(C.REGLAS_COMISION[4:], size=13), espacio=5)
    caja(s, MX, Inches(6.15), W - 2 * MX, Inches(0.6), fondo=CREMA)
    texto(s, MX + Inches(0.3), Inches(6.15), W - 2 * MX - Inches(0.6), Inches(0.6), C.COMISION_CUIDADO,
          size=12, italic=True, ancla=MSO_ANCHOR.MIDDLE)
    pie(s, n)
    notas(s, "Explicar el estorno con un ejemplo: si el cliente cancela, la comisión se descuenta de los "
             "pagos siguientes. Por eso calificar bien al cliente protege su comisión.")


def ejercicio_comision(prs, n):
    s = nueva(prs)
    encabezado(s, "04", "Ejercicio", "¿Cuánto gana Ana este mes?", "Calcule en 2 minutos y escriba su respuesta en el chat.")
    caja(s, MX, Inches(2.25), Inches(6.0), Inches(3.4), fondo=CLARO)
    caja(s, MX, Inches(2.25), Inches(6.0), Inches(0.07), fondo=DORADO)
    texto(s, MX + Inches(0.3), Inches(2.45), Inches(5.4), Inches(0.4), "EL CASO", size=11, bold=True, color=DORADO)
    texto(s, MX + Inches(0.3), Inches(2.85), Inches(5.4), Inches(2.7), lista([
        "Ana vende en el mes 1 Solución Modular y 1 Jardín Individual, a precio de lista.",
        "Facturación sin IVA: US$ 885 + US$ 531 = US$ 1.416.",
        "¿Cuántas ventas son? ¿Qué porcentaje aplica? ¿Cuánto es su comisión?",
    ], size=15), espacio=10)
    caja(s, Inches(7.0), Inches(2.25), W - Inches(7.0) - MX, Inches(3.4), fondo=AZUL)
    texto(s, Inches(7.3), Inches(2.45), Inches(5.0), Inches(0.4), "LA RESPUESTA", size=11, bold=True, color=DORADO)
    texto(s, Inches(7.3), Inches(2.9), Inches(5.0), Inches(1.0), "2 ventas = 10%", size=34, bold=True,
          color=BLANCO, font=TITULOS)
    texto(s, Inches(7.3), Inches(3.9), Inches(5.0), Inches(0.6), "10% × US$ 1.416 = US$ 141,60", size=20,
          bold=True, color=BLANCO)
    texto(s, Inches(7.3), Inches(4.6), Inches(5.0), Inches(0.9),
          "Con una tercera venta en el mes, el 12% se aplica sobre toda la facturación.", size=13,
          color=P.TINTE)
    texto(s, MX, Inches(5.9), W - 2 * MX, Inches(0.6),
          "Valores de ejemplo a precio de lista. La base real es la facturación sin IVA, neta de descuentos, y se paga sobre lo cobrado.",
          size=11, italic=True, color=GRIS)
    pie(s, n)
    notas(s, "Mostrar primero solo el caso (tapar la respuesta o revelarla después de las respuestas en "
             "el chat). Preguntar: ¿qué pasa si Ana cierra una tercera venta?")


# ---------------------------------------------------------------------------
# 05 · Técnicas de venta
# ---------------------------------------------------------------------------
def perfiles(prs, n):
    s = nueva(prs)
    encabezado(s, "05", "Técnicas de venta", "A quién le vendemos: 5 perfiles")
    filas = [(nom, quien, busca, tono, prod) for nom, quien, busca, tono, prod in C.PERFILES]
    tabla_cab(s, MX, Inches(1.8), W - 2 * MX, ["Perfil", "Quién es", "Qué busca", "Cómo hablarle", "Producto ideal"],
          filas, [1.5, 1.7, 2.2, 1.7, 3.2], size=11, alto_fila=Inches(0.75))
    texto(s, MX, Inches(6.15), W - 2 * MX, Inches(0.5), C.FILTRO_CALIFICACION, size=11, italic=True, color=GRIS)
    pie(s, n)
    notas(s, "05 · Técnicas (10 min). Preguntar: ¿qué perfil atienden más en su equipo? Identificar el "
             "perfil define el tono y el producto que se ofrece primero.")


def embudo(prs, n):
    s = nueva(prs)
    encabezado(s, "05", "Técnicas de venta", "El camino de la venta: del contacto a la posventa")
    imagen(s, BASE / "figuras" / "02_embudo.png", MX, Inches(1.75), W - 2 * MX, Inches(4.95))
    pie(s, n)
    notas(s, "Destacar dos pasos: primer contacto en menos de 1 hora y la visita al jardín o al "
             "columbario siempre que sea posible. Un contacto no registrado no existe.")


def conversacion(prs, n):
    s = nueva(prs)
    encabezado(s, "05", "Técnicas de venta", "La conversación en 5 pasos")
    w, gap = Inches(2.33), Inches(0.15)
    for i, (t, c) in enumerate(C.CONVERSACION):
        x = MX + i * (w + gap)
        caja(s, x, Inches(1.95), w, Inches(2.6), fondo=AZUL if i % 2 == 0 else AZUL_P)
        texto(s, x, Inches(2.05), w, Inches(0.8), str(i + 1), size=40, bold=True, color=DORADO,
              font=TITULOS, alinear=PP_ALIGN.CENTER)
        texto(s, x + Inches(0.15), Inches(2.85), w - Inches(0.3), Inches(0.45), t, size=16, bold=True,
              color=BLANCO, alinear=PP_ALIGN.CENTER)
        texto(s, x + Inches(0.15), Inches(3.35), w - Inches(0.3), Inches(1.15), c, size=12,
              color=P.TINTE, alinear=PP_ALIGN.CENTER)
    texto(s, MX, Inches(4.85), Inches(12), Inches(0.35), "PREGUNTAS QUE ABREN LA CONVERSACIÓN", size=11, bold=True,
          color=DORADO)
    preguntas = [NUEVOS[0]["preguntas"][0], NUEVOS[1]["preguntas"][0], EXISTENTES[0]["preguntas"][0],
                 NUEVOS[0]["preguntas"][2]]
    texto(s, MX, Inches(5.2), Inches(12), Inches(1.5), lista(preguntas, marca="?", size=13), espacio=4)
    pie(s, n)
    notas(s, "Más preguntas que afirmaciones: la solución nace de la escucha. Hablar de tranquilidad, "
             "cuidado y memoria, no de producto. Cerrar siempre con un siguiente paso claro.")


# ---------------------------------------------------------------------------
# 06 · Objeciones
# ---------------------------------------------------------------------------
def metodo(prs, n):
    s = nueva(prs)
    encabezado(s, "06", "Manejo de objeciones", "El método V·R·A", C.PRINCIPIO_OBJECIONES)
    w, gap = Inches(3.9), Inches(0.25)
    for i, (t, c) in enumerate(C.METODO_OBJECIONES):
        x = MX + i * (w + gap)
        caja(s, x, Inches(2.35), w, Inches(3.0), fondo=CLARO)
        caja(s, x, Inches(2.35), w, Inches(0.07), fondo=[P.OBJECION[0], DORADO, VERDE][i])
        texto(s, x, Inches(2.55), w, Inches(0.9), t[0], size=48, bold=True, font=TITULOS, color=AZUL,
              alinear=PP_ALIGN.CENTER)
        texto(s, x, Inches(3.45), w, Inches(0.5), t, size=20, bold=True, color=AZUL, alinear=PP_ALIGN.CENTER)
        texto(s, x + Inches(0.3), Inches(4.0), w - Inches(0.6), Inches(1.2), c, size=14,
              alinear=PP_ALIGN.CENTER)
    caja(s, MX, Inches(5.7), W - 2 * MX, Inches(0.9), fondo=AZUL)
    texto(s, MX + Inches(0.3), Inches(5.7), W - 2 * MX - Inches(0.6), Inches(0.9),
          "Una objeción no es un \"no\": es una duda que aún no resolvimos.", size=18, italic=True,
          color=BLANCO, font=TITULOS, ancla=MSO_ANCHOR.MIDDLE, alinear=PP_ALIGN.CENTER)
    pie(s, n)
    notas(s, "06 · Objeciones (10 min). Validar la emoción, reposicionar sin discutir y avanzar con un "
             "paso concreto y amable.")


def objeciones(prs, n, grupo, titulo):
    s = nueva(prs)
    encabezado(s, "06", "Manejo de objeciones", titulo)
    tabla_cab(s, MX, Inches(1.8), W - 2 * MX, ["La objeción", "Validar", "Reposicionar", "Avanzar"], grupo,
          [2.0, 1.9, 4.6, 2.1], size=11, alto_fila=Inches(1.08))
    pie(s, n)
    notas(s, "Leer en voz alta cada objeción y pedir a un participante que la responda antes de mostrar "
             "la respuesta sugerida.")


def practica(prs, n):
    s = nueva(prs)
    encabezado(s, "06", "Práctica", "Role-play en parejas · 5 minutos",
               "En salas separadas: uno es el asesor, el otro es la familia. Después cambian de rol.")
    casos = [
        ("Caso A · El Hijo Cuidador", "Busca la Solución Modular para sus padres y dice: \"Está caro\"."),
        ("Caso B · La familia católica", "Le interesa el Jardín Individual, pero cree que la cremación no está permitida."),
        ("Caso C · Las cenizas en casa", "Tiene las cenizas en casa hace un año y no ve por qué llevarlas a un columbario."),
    ]
    w, gap = Inches(3.9), Inches(0.25)
    for i, (t, c) in enumerate(casos):
        tarjeta(s, MX + i * (w + gap), Inches(2.3), w, Inches(2.4), t, c, size_t=15, size_c=14)
    texto(s, MX, Inches(5.0), Inches(12), Inches(0.35), "AL VOLVER A LA SALA PRINCIPAL", size=11, bold=True,
          color=DORADO)
    texto(s, MX, Inches(5.35), Inches(12), Inches(1.3), lista([
        "¿Qué frase de validación usó?",
        "¿Cómo reposicionó el valor sin discutir?",
        "¿Cuál fue el siguiente paso que propuso (visita, propuesta o firma)?",
    ], size=14), espacio=4)
    pie(s, n)
    notas(s, "Abrir salas de 2 personas por 5 minutos (2,5 por rol). Al volver, pedir a 2 parejas que "
             "compartan su respuesta.")


# ---------------------------------------------------------------------------
# 07 · Dudas y cierre
# ---------------------------------------------------------------------------
def checklist(prs, n):
    s = nueva(prs)
    encabezado(s, "07", "Antes de firmar", "Checklist de cierre")
    texto(s, MX, Inches(1.9), Inches(7.4), Inches(4.8), lista(C.CHECKLIST_CIERRE, marca="☐", color_marca=AZUL,
                                                             size=15), espacio=10)
    caja(s, Inches(8.4), Inches(1.9), W - Inches(8.4) - MX, Inches(4.8), fondo=CLARO)
    texto(s, Inches(8.65), Inches(2.05), Inches(4.0), Inches(0.4), "HERRAMIENTAS", size=11, bold=True, color=DORADO)
    texto(s, Inches(8.65), Inches(2.45), Inches(4.0), Inches(4.2),
          [[(f"{t}\n", {"bold": True, "color": AZUL, "size": 12}), (c, {"size": 11})] for t, c in C.HERRAMIENTAS],
          espacio=8)
    pie(s, n)
    notas(s, "07 · Dudas y cierre (10 min). Repasar el checklist rápidamente: es lo que evita "
             "cancelaciones y estornos.")


def dudas(prs, n):
    s = nueva(prs, AZUL)
    texto(s, MX + Inches(0.4), Inches(1.3), Inches(12), Inches(1.4), "¿Dudas?", size=80, bold=True,
          color=BLANCO, font=TITULOS)
    caja(s, MX + Inches(0.45), Inches(2.85), Inches(1.4), Inches(0.06), fondo=DORADO)
    texto(s, MX + Inches(0.4), Inches(3.1), Inches(11.5), Inches(0.6),
          "Espacio abierto para preguntas: productos, precios, comisiones y casos reales.", size=20,
          color=P.TINTE)
    temas = ["Productos y reglas", "Precios y descuentos", "Comisiones", "Casos de clientes"]
    w, gap = Inches(2.8), Inches(0.25)
    for i, t in enumerate(temas):
        x = MX + Inches(0.4) + i * (w + gap)
        caja(s, x, Inches(4.3), w, Inches(1.2), fondo=AZUL_P, borde=DORADO)
        texto(s, x, Inches(4.3), w, Inches(1.2), t, size=16, bold=True, color=BLANCO,
              alinear=PP_ALIGN.CENTER, ancla=MSO_ANCHOR.MIDDLE)
    texto(s, MX + Inches(0.4), Inches(5.85), Inches(11.5), Inches(0.5),
          "Las preguntas del chat que no alcancemos a responder se contestan por escrito después de la sesión.",
          size=13, italic=True, color=P.TINTE)
    pie(s, n, oscuro=True)
    notas(s, "Responder primero las preguntas acumuladas en el chat, agrupadas por tema. Anotar las que "
             "requieren validación de la Gerencia Comercial.")


def cierre(prs):
    s = nueva(prs, AZUL)
    caja(s, 0, H - Inches(0.25), W, Inches(0.25), fondo=DORADO)
    texto(s, Inches(1.5), Inches(1.2), W - Inches(3), Inches(2.8), f"\"{C.CIERRE_FRASE}\"", size=30, italic=True,
          color=BLANCO, font=TITULOS, alinear=PP_ALIGN.CENTER, ancla=MSO_ANCHOR.MIDDLE)
    caja(s, (W - Inches(1.4)) // 2, Inches(4.2), Inches(1.4), Inches(0.06), fondo=DORADO)
    texto(s, Inches(1.5), Inches(4.45), W - Inches(3), Inches(0.5), "¡Gracias y buenas ventas!", size=22, bold=True,
          color=DORADO, alinear=PP_ALIGN.CENTER, font=TITULOS)
    texto(s, Inches(1.5), Inches(5.05), W - Inches(3), Inches(0.5), C.MARCAS, size=14, bold=True,
          color=P.TINTE, alinear=PP_ALIGN.CENTER)
    logo_mil(s, (W - Inches(2.4)) // 2 - Inches(1.5), Inches(5.8), Inches(2.4), oscuro=True)
    imagen(s, LOGOS / "vangrupo_blanco.png", (W - Inches(2.2)) // 2 + Inches(1.5), Inches(5.75), w=Inches(2.2))
    notas(s, "Agradecer, recordar dónde está el material (Playbook Comercial y Ficha Técnica) y el "
             "canal para dudas posteriores.")


def main():
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
    mapa_portafolio(prs, n); n += 1
    tiempos = ["4 min.", "3 min.", "3 min.", "3 min.", "3 min."]
    for p, t in zip(NUEVOS, tiempos):
        producto(prs, n, p, t); n += 1
        if p["corto"] == "Jardín Ecológico":
            ciclo(prs, n); n += 1
    columbarios(prs, n); n += 1
    columbarios_speech(prs, n); n += 1
    precios(prs, n); n += 1
    separador(prs, n, "04", "Política de comisiones", "La comisión premia la venta buena, no solo la venta."); n += 1
    comisiones(prs, n); n += 1
    comisiones_pago(prs, n); n += 1
    ejercicio_comision(prs, n); n += 1
    separador(prs, n, "05", "Técnicas de venta", "Conocer al cliente es la mitad de la venta."); n += 1
    perfiles(prs, n); n += 1
    embudo(prs, n); n += 1
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
