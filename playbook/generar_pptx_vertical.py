"""
Versión VERTICAL (A4) del Playbook Comercial para importar en Canva, con los logos
oficiales de La Auxiliadora, Hogar de las Memorias y Vangrupo (playbook/logos/).

Reutiliza las primitivas de generar_pptx.py con un lienzo vertical y un diseño de
cuadernillo: una página por tema y una página por producto.

Uso:  python3 playbook/generar_pptx_vertical.py
      ->  playbook/salida/Playbook_Comercial_Cremacion_Vangrupo_Vertical.pptx
"""
import sys
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches

sys.path.insert(0, str(Path(__file__).parent))
import contenido as C  # noqa: E402
import generar_pptx as G  # noqa: E402
import paleta as P  # noqa: E402

# Lienzo A4 vertical: las primitivas de generar_pptx leen estos valores del módulo.
G.W, G.H, G.MX = Inches(8.27), Inches(11.69), Inches(0.55)
W, H, MX = G.W, G.H, G.MX
ANCHO = W - 2 * MX
LOGOS = Path(__file__).parent / "logos"
SALIDA = Path(__file__).parent / "salida" / "Playbook_Comercial_Cremacion_Vangrupo_Vertical.pptx"

AZUL, AZUL_P, DORADO, CLARO, TEXTO, GRIS = G.AZUL, G.AZUL_P, G.DORADO, G.CLARO, G.TEXTO, G.GRIS
VERDE, CREMA, BLANCO = G.VERDE, G.CREMA, G.BLANCO
TITULOS = G.TITULOS
caja, texto, imagen, nueva, tarjeta, lista, tabla = G.caja, G.texto, G.imagen, G.nueva, G.tarjeta, G.lista, G.tabla
pie, encabezado = G.pie, G.encabezado


def logo(s, archivo, x, y, w, h):
    """Inserta un logo centrado dentro de la caja (x, y, w, h) sin deformarlo."""
    ruta = LOGOS / archivo
    ancho, alto = Image.open(ruta).size
    esc = min(w / ancho, h / alto)
    ww, hh = int(ancho * esc), int(alto * esc)
    s.shapes.add_picture(str(ruta), x + (w - ww) // 2, y + (h - hh) // 2, ww, hh)


def fila_logos(s, y, alto=Inches(1.25)):
    caja(s, MX, y, ANCHO, alto, fondo=BLANCO, forma=MSO_SHAPE.ROUNDED_RECTANGLE)
    archivos = ("la_auxiliadora.png", "hogar_de_las_memorias.png", "las_colinas.png", "vangrupo.png")
    w = (ANCHO - Inches(0.15) * (len(archivos) + 1)) // len(archivos)
    for i, archivo in enumerate(archivos):
        logo(s, archivo, MX + Inches(0.15) + i * (w + Inches(0.15)), y + Inches(0.15), w, alto - Inches(0.3))


def bloque(s, x, y, w, h, titulo, contenido, *, fondo=CLARO, acento=DORADO, size=10.5):
    caja(s, x, y, w, h, fondo=fondo)
    caja(s, x, y, w, Inches(0.07), fondo=acento)
    texto(s, x + Inches(0.15), y + Inches(0.12), w - Inches(0.3), Inches(0.3), titulo.upper(),
          size=9.5, bold=True, color=AZUL)
    texto(s, x + Inches(0.15), y + Inches(0.42), w - Inches(0.3), h - Inches(0.5), contenido, size=size, espacio=3)


# ---------------------------------------------------------------------------
# páginas
# ---------------------------------------------------------------------------
def portada(prs):
    s = nueva(prs, AZUL)
    fila_logos(s, Inches(0.6))
    texto(s, MX + Inches(0.1), Inches(3.3), ANCHO, Inches(0.4), C.CAMPANA.upper(), size=13, bold=True, color=DORADO)
    texto(s, MX + Inches(0.1), Inches(3.8), ANCHO, Inches(2.2), ["Playbook", "Comercial"],
          size=60, bold=True, color=BLANCO, font=TITULOS, interlineado=0.95, espacio=0)
    texto(s, MX + Inches(0.1), Inches(6.05), ANCHO, Inches(1.0), C.SUBTITULO, size=22, color="F1ECF7", font=TITULOS)
    caja(s, MX + Inches(0.15), Inches(7.25), Inches(1.4), Inches(0.06), fondo=DORADO)
    texto(s, MX + Inches(0.1), Inches(7.5), ANCHO, Inches(0.9), f"«{C.LEMA}»", size=16, italic=True,
          color=BLANCO, font=TITULOS)
    texto(s, MX + Inches(0.1), Inches(9.9), ANCHO, Inches(0.4), C.MARCAS, size=12, bold=True, color=DORADO)
    texto(s, MX + Inches(0.1), Inches(10.3), ANCHO, Inches(0.4), C.VERSION, size=10, color=P.TINTE)
    caja(s, 0, H - Inches(0.25), W, Inches(0.25), fondo=DORADO)


def como_usar(prs, n):
    s = nueva(prs)
    encabezado(s, "Antes de empezar", "Cómo usar este playbook")
    texto(s, MX, Inches(1.75), ANCHO, Inches(1.4), C.COMO_USAR, size=12.5)
    caja(s, MX, Inches(3.25), ANCHO, Inches(2.55), fondo=CREMA)
    caja(s, MX, Inches(3.25), Inches(0.08), Inches(2.55), fondo=DORADO)
    texto(s, MX + Inches(0.3), Inches(3.4), ANCHO - Inches(0.5), Inches(0.35), "PENDIENTES DE VALIDACIÓN",
          size=10.5, bold=True, color=AZUL)
    texto(s, MX + Inches(0.3), Inches(3.8), ANCHO - Inches(0.5), Inches(1.95), lista(C.PENDIENTES, size=11.5))
    texto(s, MX, Inches(6.0), ANCHO, Inches(0.5), "Contenido", size=22, bold=True, color=AZUL, font=TITULOS)
    for i, (num, tit) in enumerate(C.INDICE):
        y = Inches(6.6) + i * Inches(0.53)
        texto(s, MX, y, Inches(0.9), Inches(0.5), num, size=22, bold=True, color=DORADO, font=TITULOS)
        texto(s, MX + Inches(0.9), y + Inches(0.09), ANCHO - Inches(0.9), Inches(0.42), tit, size=14, bold=True, color=AZUL)
        caja(s, MX, y + Inches(0.49), ANCHO, Inches(0.012), fondo=P.LINEA)
    pie(s, n)


def quienes(prs, n):
    s = nueva(prs)
    encabezado(s, "01 · Quiénes somos", "Acompañamos familias")
    texto(s, MX, Inches(1.75), ANCHO, Inches(1.75), C.QUIENES_SOMOS, size=12)
    imagen(s, "01_portafolio", MX, Inches(3.5), ANCHO, Inches(3.15))
    w = (ANCHO - Inches(0.2)) // 2
    for i, (tit, txt) in enumerate(C.POR_QUE_AHORA):
        bloque(s, MX + (i % 2) * (w + Inches(0.2)), Inches(6.85) + (i // 2) * Inches(1.4), w, Inches(1.25),
               tit, txt, size=10.5)
    caja(s, MX, Inches(9.75), ANCHO, Inches(1.2), fondo=AZUL)
    texto(s, MX + Inches(0.25), Inches(9.75), ANCHO - Inches(0.5), Inches(1.2),
          [[("REGLA DE ORO   ", {"bold": True, "color": DORADO, "size": 10.5}),
            (C.REGLA_DE_ORO, {"color": BLANCO, "size": 12, "italic": True})]], ancla=MSO_ANCHOR.MIDDLE)
    pie(s, n)


def momentos(prs, n):
    s = nueva(prs)
    encabezado(s, "01 · Lo que vendemos", "Dos momentos de venta")
    for i, (tit, txt) in enumerate(C.MODOS_DE_VENTA):
        tarjeta(s, MX, Inches(1.8) + i * Inches(1.75), ANCHO, Inches(1.6), tit, txt,
                acento=AZUL if i == 0 else VERDE, size_t=15, size_c=12)
    texto(s, MX, Inches(5.45), ANCHO, Inches(0.5), "Qué producto lleva cada equipo", size=18, bold=True,
          color=AZUL, font=TITULOS)
    for i, (eq, desc, prod) in enumerate(C.EQUIPOS):
        y = Inches(6.05) + i * Inches(1.65)
        caja(s, MX, y, Inches(2.3), Inches(1.5), fondo=AZUL)
        texto(s, MX + Inches(0.12), y, Inches(2.06), Inches(1.5), eq, size=12, bold=True, color=BLANCO,
              ancla=MSO_ANCHOR.MIDDLE)
        caja(s, MX + Inches(2.3), y, ANCHO - Inches(2.3), Inches(1.5), fondo=CLARO)
        texto(s, MX + Inches(2.45), y + Inches(0.1), ANCHO - Inches(2.6), Inches(1.35),
              [[(desc, {"size": 10.5, "italic": True, "color": GRIS})],
               [("Producto foco: ", {"size": 10.5, "bold": True, "color": DORADO}), (prod, {"size": 10.5, "bold": True})]],
              espacio=4)
    pie(s, n)


def perfiles(prs, n):
    s = nueva(prs)
    encabezado(s, "02 · A quién le vendemos", "Cinco perfiles de cliente",
               "Identifique el perfil en los primeros minutos y adapte el tono.")
    for i, (nom, quien, busca, tono, prod) in enumerate(C.PERFILES):
        y = Inches(2.15) + i * Inches(1.5)
        caja(s, MX, y, Inches(2.1), Inches(1.38), fondo=AZUL)
        texto(s, MX + Inches(0.12), y, Inches(1.9), Inches(1.38),
              [[(nom, {"size": 12.5, "bold": True, "color": BLANCO})], [(quien, {"size": 9, "color": P.TINTE})]],
              ancla=MSO_ANCHOR.MIDDLE, espacio=2)
        caja(s, MX + Inches(2.1), y, ANCHO - Inches(2.1), Inches(1.38), fondo=CLARO)
        texto(s, MX + Inches(2.25), y + Inches(0.08), ANCHO - Inches(2.4), Inches(1.25), [
            [("Busca: ", {"bold": True, "color": AZUL}), (busca, {})],
            [("Tono: ", {"bold": True, "color": AZUL}), (tono, {})],
            [("Ideal: ", {"bold": True, "color": DORADO}), (prod, {"bold": True})],
        ], size=10.5, espacio=3)
    caja(s, MX, Inches(9.7), ANCHO, Inches(1.3), fondo=CREMA)
    texto(s, MX + Inches(0.25), Inches(9.7), ANCHO - Inches(0.5), Inches(1.3),
          [[("FILTRO N·O·A   ", {"bold": True, "color": AZUL, "size": 10}), (C.FILTRO_CALIFICACION, {"size": 10.5})]],
          ancla=MSO_ANCHOR.MIDDLE)
    pie(s, n)


def proceso(prs, n):
    s = nueva(prs)
    encabezado(s, "03 · El proceso de venta", "Del contacto a la posventa")
    imagen(s, "02_embudo", MX, Inches(1.7), ANCHO, Inches(3.35))
    imagen(s, "03_conversacion", MX, Inches(5.2), ANCHO, Inches(1.6))
    texto(s, MX, Inches(7.05), ANCHO, Inches(0.45), "Rituales del equipo", size=18, bold=True, color=AZUL, font=TITULOS)
    for i, (frec, rit) in enumerate(C.RITUALES):
        bloque(s, MX, Inches(7.6) + i * Inches(1.12), ANCHO, Inches(1.0), frec, rit, size=11)
    pie(s, n)


def producto(prs, n, p):
    proximo = p.get("proximo")
    s = nueva(prs)
    caja(s, 0, 0, W, Inches(1.6), fondo=P.APAGADO if proximo else AZUL)
    caja(s, 0, Inches(1.6), W, Inches(0.07), fondo=DORADO)
    texto(s, MX, Inches(0.25), Inches(4.6), Inches(0.3), p["etiqueta"].upper(), size=9.5, bold=True, color=DORADO)
    texto(s, MX, Inches(0.55), Inches(4.6), Inches(0.95), p["nombre"], size=21, bold=True, color=BLANCO,
          font=TITULOS, interlineado=1.0)
    texto(s, Inches(5.1), Inches(0.25), Inches(2.62), Inches(0.3),
          "PRÓXIMO LANZAMIENTO" if proximo else "PRECIO SUGERIDO", size=9.5, bold=True, color=DORADO,
          alinear=PP_ALIGN.RIGHT)
    texto(s, Inches(5.1), Inches(0.55), Inches(2.62), Inches(0.95), p["precio"],
          size=26 if len(p["precio"]) <= 10 else 19, bold=True, color=BLANCO, alinear=PP_ALIGN.RIGHT,
          ancla=MSO_ANCHOR.MIDDLE)
    texto(s, MX, Inches(1.78), ANCHO, Inches(0.35), p["pago"], size=11, italic=True, color=GRIS)
    texto(s, MX, Inches(2.18), ANCHO, Inches(1.15), [
        [("Qué es.  ", {"bold": True, "color": AZUL}), (p["que_es"], {})],
        [("Para quién.  ", {"bold": True, "color": AZUL}), (p["para_quien"], {})],
    ], size=11, espacio=4)
    w = (ANCHO - Inches(0.2)) // 2
    x2 = MX + w + Inches(0.2)
    bloque(s, MX, Inches(3.4), w, Inches(2.65), "Qué incluye", lista(p["incluye"], "✓", VERDE, 10.5), acento=VERDE)
    bloque(s, x2, Inches(3.4), w, Inches(2.65), "Reglas del producto", lista(p["reglas"], size=10.5))
    caja(s, MX, Inches(6.2), ANCHO, Inches(1.4), fondo=CREMA)
    caja(s, MX, Inches(6.2), Inches(0.08), Inches(1.4), fondo=DORADO)
    texto(s, MX + Inches(0.25), Inches(6.25), ANCHO - Inches(0.4), Inches(0.3), "SPEECH SUGERIDO", size=9.5,
          bold=True, color=AZUL)
    texto(s, MX + Inches(0.25), Inches(6.52), ANCHO - Inches(0.4), Inches(1.05), p["speech"], size=11,
          italic=True, color=AZUL_P, font=TITULOS)
    bloque(s, MX, Inches(7.75), w, Inches(1.75), "Preguntas de descubrimiento", lista(p["preguntas"], "?", P.PREGUNTAS[0], 9.5),
           acento=P.PREGUNTAS[0], fondo=P.PREGUNTAS[1])
    bloque(s, x2, Inches(7.75), w, Inches(1.75), "Frase de cierre", p["cierre"], acento=P.CIERRE[0],
           fondo=P.CIERRE[1], size=10.5)
    bloque(s, MX, Inches(9.65), w, Inches(1.45), "Objeción típica", p["objecion"], acento=P.OBJECION[0],
           fondo=P.OBJECION[1], size=9)
    bloque(s, x2, Inches(9.65), w, Inches(1.45), "Tip del asesor", p["tip"], acento=P.TIP[0],
           fondo=P.TIP[1], size=10.5)
    pie(s, n)


def figura(prs, n, seccion, titulo, fig, intro=""):
    s = nueva(prs)
    encabezado(s, seccion, titulo, intro)
    top = Inches(2.2) if intro else Inches(1.8)
    imagen(s, fig, MX, top, ANCHO, Inches(4.5))
    return s


def ciclo(prs, n):
    s = figura(prs, n, "04 · Jardín Ecológico y de Mascotas", "El ciclo de 3 años",
               "06_ciclo_ecologico")
    caja(s, MX, Inches(5.0), ANCHO, Inches(1.4), fondo=CREMA)
    caja(s, MX, Inches(5.0), Inches(0.08), Inches(1.4), fondo=DORADO)
    texto(s, MX + Inches(0.3), Inches(5.0), ANCHO - Inches(0.5), Inches(1.4),
          [[("TRANSPARENCIA   ", {"bold": True, "color": AZUL, "size": 10}),
            ("Explique el plazo de 3 años desde la primera conversación. La placa memorial está incluida en el "
             "Jardín Ecológico (US$ 750) y en la opción de Mascotas de US$ 550.", {"size": 11.5})]],
          ancla=MSO_ANCHOR.MIDDLE)
    pie(s, n)


def objeciones(prs, n, desde, hasta, con_metodo):
    s = nueva(prs)
    encabezado(s, "05 · Manejo de objeciones", "El método V·R·A" if con_metodo else "Objeciones frecuentes")
    y = Inches(1.75)
    if con_metodo:
        imagen(s, "04_objeciones", MX, y, ANCHO, Inches(2.25))
        y += Inches(2.45)
    anchos = [Inches(2.0), ANCHO - Inches(4.2), Inches(2.0)]
    for i, (obj, val, rep, ava) in enumerate(C.OBJECIONES[desde:hasta], start=desde + 1):
        caja(s, MX, y, ANCHO, Inches(0.45), fondo=AZUL)
        texto(s, MX + Inches(0.15), y, ANCHO - Inches(0.3), Inches(0.45), f"{i}.  {obj}", size=12, bold=True,
              color=BLANCO, ancla=MSO_ANCHOR.MIDDLE)
        x = MX
        for k, (letra, nombre, txt) in enumerate((("V", "Validar", f"«{val}»"), ("R", "Reposicionar", rep),
                                                   ("A", "Avanzar", f"«{ava}»"))):
            caja(s, x, y + Inches(0.5), anchos[k], Inches(1.75), fondo=CLARO)
            texto(s, x + Inches(0.1), y + Inches(0.55), anchos[k] - Inches(0.2), Inches(1.68), [
                [(f"{letra}  ", {"font": TITULOS, "size": 14, "bold": True, "color": DORADO}),
                 (nombre.upper(), {"size": 9, "bold": True, "color": AZUL})],
                [(txt, {"size": 10, "italic": letra != "R"})],
            ], espacio=2)
            x += anchos[k] + Inches(0.1)
        y += Inches(2.4)
    pie(s, n)


def precios(prs, n):
    s = nueva(prs)
    encabezado(s, "06 · Precios, reglas y condiciones", "Tabla de precios",
               "Fuente oficial: Ficha Técnica vigente. Precios sugeridos en US$, IVA incluido.")
    tabla(s, MX, Inches(2.2), ANCHO, ["Producto", "Precio", "Pago", "Mant.", "Plazo / condición"],
          [list(f) for f in C.TABLA_PRECIOS], [2.0, 1.4, 2.0, 1.1, 2.6], size=10, alto_fila=Inches(0.62),
          resaltar=lambda f: f[0] == "Jardín Ceremonial")
    caja(s, MX, Inches(6.85), ANCHO, Inches(1.3), fondo=CREMA)
    caja(s, MX, Inches(6.85), Inches(0.08), Inches(1.3), fondo=DORADO)
    texto(s, MX + Inches(0.3), Inches(6.85), ANCHO - Inches(0.5), Inches(1.3),
          [[("EL DESCUENTO NO ES LA SALIDA   ", {"bold": True, "color": AZUL, "size": 10}),
            (C.DESCUENTO_NO_ES_SALIDA, {"size": 11})]], ancla=MSO_ANCHOR.MIDDLE)
    pie(s, n)


def reglas(prs, n):
    s = nueva(prs)
    encabezado(s, "06 · Precios, reglas y condiciones", "Reglas comerciales")
    tabla(s, MX, Inches(1.8), ANCHO, ["Tema", "Regla"], [list(r) for r in C.REGLAS_COMERCIALES],
          [2.0, 5.2], size=11, alto_fila=Inches(0.95))
    pie(s, n)


def comisiones(prs, n):
    s = nueva(prs)
    encabezado(s, "07 · Política de comisiones", "Comisión única de 8%",
               "Sobre el precio sin IVA. Validar con la Gerencia Comercial.")
    imagen(s, "05_comisiones", MX, Inches(2.15), ANCHO, Inches(2.75))
    tabla(s, MX, Inches(5.1), ANCHO, ["Producto", "%", "Comisión", "Cuándo se paga", "Estorno"],
          [list(f) for f in C.COMISIONES], [2.0, 0.6, 1.2, 2.4, 1.6], size=9.5, alto_fila=Inches(0.72),
          resaltar=lambda f: f[0] == "Jardín Ceremonial")
    pie(s, n)


def comisiones_reglas(prs, n):
    s = nueva(prs)
    encabezado(s, "07 · Política de comisiones", "Reglas de comisión")
    texto(s, MX, Inches(1.85), ANCHO, Inches(4.6), lista(C.REGLAS_COMISION, size=13), espacio=10)
    caja(s, MX, Inches(6.6), ANCHO, Inches(1.5), fondo=AZUL)
    texto(s, MX + Inches(0.3), Inches(6.6), ANCHO - Inches(0.6), Inches(1.5), C.COMISION_CUIDADO, size=13,
          italic=True, color=BLANCO, font=TITULOS, ancla=MSO_ANCHOR.MIDDLE)
    pie(s, n)


def herramientas(prs, n):
    s = nueva(prs)
    encabezado(s, "08 · Herramientas de apoyo", "Lo que usted tiene a mano")
    for i, (tit, txt) in enumerate(C.HERRAMIENTAS):
        y = Inches(1.8) + i * Inches(0.88)
        caja(s, MX, y, ANCHO, Inches(0.78), fondo=CLARO)
        caja(s, MX, y, Inches(0.07), Inches(0.78), fondo=DORADO)
        texto(s, MX + Inches(0.2), y + Inches(0.04), ANCHO - Inches(0.3), Inches(0.72),
              [[(tit, {"bold": True, "color": AZUL, "size": 12})], [(txt, {"size": 10.5})]], espacio=1)
    caja(s, MX, Inches(6.35), ANCHO, Inches(4.65), fondo=AZUL)
    texto(s, MX + Inches(0.35), Inches(6.5), ANCHO - Inches(0.7), Inches(0.5), "Checklist antes de cerrar",
          size=20, bold=True, color=DORADO, font=TITULOS)
    texto(s, MX + Inches(0.35), Inches(7.15), ANCHO - Inches(0.7), Inches(3.8),
          [[("☐  ", {"color": DORADO, "size": 14}), (it, {"color": BLANCO, "size": 12.5})] for it in C.CHECKLIST_CIERRE],
          espacio=9)
    pie(s, n)


def cierre(prs):
    s = nueva(prs, AZUL)
    texto(s, Inches(0.8), Inches(2.4), W - Inches(1.6), Inches(3.6), f"«{C.CIERRE_FRASE}»", size=26, italic=True,
          color=BLANCO, font=TITULOS, alinear=PP_ALIGN.CENTER, ancla=MSO_ANCHOR.MIDDLE)
    caja(s, (W - Inches(1.4)) // 2, Inches(6.3), Inches(1.4), Inches(0.06), fondo=DORADO)
    texto(s, MX, Inches(6.6), ANCHO, Inches(0.5), C.MARCAS, size=13, bold=True, color=DORADO, alinear=PP_ALIGN.CENTER)
    fila_logos(s, Inches(9.2))
    caja(s, 0, H - Inches(0.25), W, Inches(0.25), fondo=DORADO)


def main():
    prs = Presentation()
    prs.slide_width, prs.slide_height = W, H
    n = 2
    portada(prs)
    for f in (como_usar, quienes, momentos, perfiles, proceso):
        f(prs, n); n += 1
    for p in C.PRODUCTOS:
        producto(prs, n, p); n += 1
        if p["corto"] == "Jardín Ecológico":
            ciclo(prs, n); n += 1
    for desde, hasta, metodo in ((0, 2, True), (2, 5, False), (5, 8, False)):
        objeciones(prs, n, desde, hasta, metodo); n += 1
    for f in (precios, reglas, comisiones, comisiones_reglas, herramientas):
        f(prs, n); n += 1
    cierre(prs)
    SALIDA.parent.mkdir(exist_ok=True)
    prs.save(SALIDA)
    print(f"✔ {SALIDA} ({len(prs.slides)} páginas, {SALIDA.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
