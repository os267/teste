"""
Genera las figuras del playbook como PNG (HTML + Chromium headless).

Uso: python playbook/figuras.py   → escribe playbook/figuras/*.png
"""
import html
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageChops

sys.path.insert(0, str(Path(__file__).parent))
import contenido as C  # noqa: E402
import paleta as P  # noqa: E402

SALIDA = Path(__file__).parent / "figuras"
CHROMIUM = "/opt/pw-browsers/chromium"

AZUL = "#" + P.PRINCIPAL
AZUL_P = "#" + P.PRINCIPAL_O
DORADO = "#" + P.ACENTO
DORADO_B = "#" + P.ACENTO_B
CLARO = "#" + P.CLARO
TEXTO = "#" + P.TEXTO
VERDE = "#" + P.VERDE
TONO_EMBUDO = "91,63,128"  # morado La Auxiliadora, en RGB para la transparencia de cada etapa

BASE_CSS = f"""
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: 'Liberation Sans', Arial, sans-serif; color: {TEXTO}; background: #fff; }}
.lienzo {{ padding: 28px 32px; }}
.titulo {{ font-size: 15px; letter-spacing: .14em; text-transform: uppercase; color: {AZUL};
  font-weight: 700; margin-bottom: 18px; border-left: 5px solid {DORADO}; padding-left: 10px; }}
"""

e = html.escape


def render(nombre: str, cuerpo: str, ancho: int, alto: int) -> Path:
    SALIDA.mkdir(exist_ok=True)
    destino = SALIDA / f"{nombre}.png"
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(f"<!doctype html><html><head><meta charset='utf-8'><style>{BASE_CSS}</style></head>"
                f"<body><div class='lienzo'>{cuerpo}</div></body></html>")
        ruta = f.name
    subprocess.run([CHROMIUM, "--headless", "--no-sandbox", "--hide-scrollbars",
                    "--force-device-scale-factor=2", f"--window-size={ancho},{alto}",
                    f"--screenshot={destino}", f"file://{ruta}"],
                   check=True, capture_output=True)
    recortar(destino)
    return destino


def recortar(destino: Path, margen: int = 40) -> None:
    """Quita el blanco sobrante al pie para que ninguna figura quede cortada ni con aire de más."""
    img = Image.open(destino).convert("RGB")
    caja = ImageChops.difference(img, Image.new("RGB", img.size, (255, 255, 255))).getbbox()
    if caja:
        img.crop((0, 0, img.width, min(img.height, caja[3] + margen))).save(destino)


def portafolio(nombre="01_portafolio", nuevos=None):
    nuevos = C.PRODUCTOS if nuevos is None else nuevos
    def tarjetas(productos, colores):
        html = ""
        for p, col in zip(productos, colores):
            extra = "<div class='prox'>PRÓXIMAMENTE</div>" if p.get("proximo") else ""
            html += f"""
            <div class='card' style='border-top:5px solid {col}'>
              {extra}
              <div class='et'>{e(p['etiqueta'].split(' · ')[0])}</div>
              <div class='nom'>{e(p['corto'])}</div>
              <div class='pre' style='color:{col}'>{e(p['precio'].replace(' / US$ ', ' / '))}</div>
              <div class='pag'>{e(p['pago'].split(' · ')[0])}</div>
            </div>"""
        return html
    columnas = len(nuevos)
    nuevos = tarjetas(nuevos, [AZUL, VERDE, "#" + P.TERRACOTA, VERDE, DORADO, "#" + P.APAGADO])
    existentes = tarjetas(C.PRODUCTOS_EXISTENTES, [AZUL_P] * len(C.PRODUCTOS_EXISTENTES))
    css = f"""
    <style>
    .grupo {{ font-size: 12px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color:{AZUL};
      margin: 4px 0 8px; }}
    .grid {{ display:grid; gap: 10px; margin-bottom: 14px; }}
    .g6 {{ grid-template-columns: repeat(6, 1fr); }}
    .g5 {{ grid-template-columns: repeat(5, 1fr); }}
    .card {{ background:{CLARO}; border-radius: 8px; padding: 10px 11px 12px; position:relative; }}
    .et {{ font-size: 9px; text-transform: uppercase; letter-spacing: .06em; color:#7D7887; }}
    .nom {{ font-size: 14px; font-weight: 700; color:{AZUL_P}; margin: 4px 0 5px; line-height: 1.2; }}
    .pre {{ font-size: 15px; font-weight: 700; }}
    .pag {{ font-size: 10.5px; margin-top: 4px; line-height: 1.3; }}
    .prox {{ position:absolute; top:-9px; right:8px; background:{DORADO_B}; color:{AZUL_P};
      font-size:8px; font-weight:700; letter-spacing:.06em; padding:3px 6px; border-radius: 4px; }}
    </style>"""
    return render(nombre, css + "<div class='titulo'>Portafolio de cremación</div>"
                  "<div class='grupo'>Lanzamientos de Finados · −20% en Finados y noviembre</div>"
                  f"<div class='grid g{columnas}'>{nuevos}</div>"
                  "<div class='grupo'>Columbarios · portafolio existente · −15% en Finados y noviembre</div>"
                  f"<div class='grid g5'>{existentes}</div>", 960, 600)


def embudo():
    filas = ""
    n = len(C.EMBUDO)
    for i, (etapa, desc) in enumerate(C.EMBUDO):
        ancho = 100 - i * 8
        tono = f"rgba({TONO_EMBUDO},{1 - i * 0.1:.2f})"
        filas += f"""
        <div class='fila'>
          <div class='barra' style='width:{ancho}%; background:{tono}'>
            <span class='num'>{i + 1}</span><span class='et'>{e(etapa)}</span></div>
          <div class='desc'>{e(desc)}</div>
        </div>"""
    css = f"""
    <style>
    .fila {{ display:grid; grid-template-columns: 330px 1fr; align-items:center; gap: 16px; margin-bottom: 8px; }}
    .barra {{ color:#fff; height: 44px; border-radius: 6px; display:flex; align-items:center; margin: 0 auto;
      padding-left: 14px; font-weight:700; font-size: 15px; }}
    .num {{ background:{DORADO}; color:{AZUL_P}; width:24px; height:24px; border-radius:50%; display:inline-flex;
      align-items:center; justify-content:center; font-size: 12px; margin-right: 10px; flex: 0 0 24px; }}
    .desc {{ font-size: 13.5px; line-height: 1.35; }}
    </style>"""
    return render("02_embudo", css + "<div class='titulo'>El embudo de ventas (prenecesidad)</div>" + filas,
                  960, 900)


def conversacion():
    pasos = ""
    for i, (p, d) in enumerate(C.CONVERSACION):
        pasos += f"""
        <div class='paso'>
          <div class='flecha'><span>{i + 1}</span>{e(p)}</div>
          <div class='desc'>{e(d)}</div>
        </div>"""
    css = f"""
    <style>
    .fila {{ display:grid; grid-template-columns: repeat(5, 1fr); gap: 6px; }}
    .flecha {{ background:{AZUL}; color:#fff; font-weight:700; font-size: 15px; height: 58px; display:flex;
      align-items:center; padding: 0 18px 0 22px;
      clip-path: polygon(0 0, 88% 0, 100% 50%, 88% 100%, 0 100%, 10% 50%); }}
    .paso:first-child .flecha {{ clip-path: polygon(0 0, 88% 0, 100% 50%, 88% 100%, 0 100%); padding-left: 14px; }}
    .flecha span {{ color:{DORADO_B}; margin-right: 8px; font-size: 18px; }}
    .desc {{ font-size: 12.5px; line-height: 1.4; padding: 10px 8px 0 6px; }}
    </style>"""
    return render("03_conversacion", css + "<div class='titulo'>La estructura de una buena conversación</div>"
                  f"<div class='fila'>{pasos}</div>", 960, 600)


def objeciones():
    nodos = ""
    for i, (p, d) in enumerate(C.METODO_OBJECIONES):
        nodos += f"""
        <div class='nodo'>
          <div class='circ'>{e(p[0])}</div>
          <div class='nom'>{i + 1}. {e(p)}</div>
          <div class='desc'>{e(d)}</div>
        </div>"""
        if i < len(C.METODO_OBJECIONES) - 1:
            nodos += "<div class='flecha'>➜</div>"
    css = f"""
    <style>
    .fila {{ display:flex; align-items:flex-start; justify-content:center; gap: 10px; }}
    .nodo {{ width: 250px; text-align:center; }}
    .circ {{ width: 86px; height: 86px; border-radius: 50%; background:{AZUL}; color:{DORADO_B}; font-size: 40px;
      font-weight:700; display:flex; align-items:center; justify-content:center; margin: 0 auto 10px;
      border: 4px solid {DORADO}; }}
    .nom {{ font-weight:700; color:{AZUL_P}; font-size: 17px; margin-bottom: 6px; }}
    .desc {{ font-size: 13px; line-height: 1.4; }}
    .flecha {{ font-size: 34px; color:{DORADO}; padding-top: 22px; }}
    .nota {{ margin-top: 18px; background:{CLARO}; border-left:4px solid {DORADO}; padding: 10px 14px; font-size: 13px; }}
    </style>"""
    return render("04_objeciones", css + "<div class='titulo'>Método V·R·A para manejar objeciones</div>"
                  f"<div class='fila'>{nodos}</div><div class='nota'>{e(C.PRINCIPIO_OBJECIONES)}</div>",
                  960, 700)


def comisiones():
    maximo = max(v for _, v in C.COMISIONES_VALORES)
    filas = ""
    for nombre, valor in C.COMISIONES_VALORES:
        ancho = valor / maximo * 82
        monto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        filas += f"""
        <div class='fila'><div class='nom'>{e(nombre)}</div>
          <div class='pista'><div class='bar' style='width:{ancho:.1f}%'></div>
          <span class='val'>US$ {monto}</span></div></div>"""
    css = f"""
    <style>
    .fila {{ display:grid; grid-template-columns: 220px 1fr; align-items:center; gap: 12px; margin-bottom: 10px; }}
    .nom {{ font-size: 14px; font-weight: 700; color:{AZUL_P}; text-align:right; }}
    .pista {{ display:flex; align-items:center; gap: 10px; }}
    .bar {{ height: 26px; background: linear-gradient(90deg, {AZUL}, {AZUL_P}); border-radius: 0 6px 6px 0;
      border-right: 4px solid {DORADO}; }}
    .val {{ font-size: 14px; font-weight:700; color:{AZUL}; white-space:nowrap; }}
    .nota {{ font-size: 11.5px; color:#7D7887; margin-top: 8px; }}
    </style>"""
    return render("05_comisiones", css + "<div class='titulo'>Comisión del mes según cantidad de ventas</div>"
                  + filas + "<div class='nota'>Ejemplo con Solución Modular (US$ 885 sin IVA c/u). El % se aplica sobre toda la facturación del mes; mantenimiento anual no comisiona.</div>",
                  960, 700)


def ciclo():
    pasos = [
        ("1", "Inhumación", "Urna biodegradable en el jardín, con placa de identificación."),
        ("2", "3 años", "La familia visita un lugar señalado; la urna se integra a la tierra."),
        ("3", "Placa memorial", "El nombre pasa al monumento del jardín (incluida en el Ecológico y en Mascotas)."),
        ("4", "Ciclo natural", "El espacio se reutiliza: el jardín sigue vivo para otras familias."),
    ]
    html_pasos = ""
    for i, (n, t, d) in enumerate(pasos):
        html_pasos += f"""<div class='paso'><div class='circ'>{n}</div><div class='t'>{e(t)}</div>
            <div class='d'>{e(d)}</div></div>"""
        if i < len(pasos) - 1:
            html_pasos += "<div class='linea'></div>"
    css = f"""
    <style>
    .fila {{ display:flex; align-items:flex-start; }}
    .paso {{ width: 200px; text-align:center; }}
    .linea {{ flex:1; height: 4px; background:{DORADO}; margin-top: 30px; }}
    .circ {{ width: 64px; height: 64px; border-radius:50%; background:{VERDE}; color:#fff; font-size: 26px;
      font-weight:700; display:flex; align-items:center; justify-content:center; margin: 0 auto 10px; }}
    .t {{ font-weight:700; color:{AZUL_P}; font-size: 16px; margin-bottom: 6px; }}
    .d {{ font-size: 12.5px; line-height: 1.4; }}
    </style>"""
    return render("06_ciclo_ecologico", css + "<div class='titulo'>Ciclo del Jardín Ecológico y de Mascotas</div>"
                  f"<div class='fila'>{html_pasos}</div>", 960, 600)


def equipos():
    cols = ""
    for nombre, rol in C.EQUIPOS:
        cols += f"""<div class='col'><div class='cab'>{e(nombre)}</div>
          <div class='rol'>{e(rol)}</div></div>"""
    css = f"""
    <style>
    .grid {{ display:grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }}
    .cab {{ background:{AZUL}; color:#fff; font-weight:700; font-size: 15px; padding: 12px 14px; border-radius: 8px 8px 0 0;
      border-bottom: 4px solid {DORADO}; }}
    .rol {{ background:{CLARO}; padding: 12px 14px; font-size: 13px; line-height:1.4; min-height: 64px; }}
    .nota {{ margin-top: 16px; border: 2px solid {DORADO}; border-radius: 8px; padding: 12px 14px; font-size: 14px;
      line-height:1.4; font-weight:700; color:{AZUL}; }}
    </style>"""
    return render("07_equipos", css + f"<div class='titulo'>{e(C.EQUIPOS_TITULO)}</div>"
                  f"<div class='grid'>{cols}</div><div class='nota'>{e(C.EQUIPOS_NOTA)}</div>", 960, 420)


def logos():
    """Franja de marcas para la portada (espacios reservados para logos oficiales)."""
    cajas = ""
    for marca in ("La Auxiliadora", "Hogar de las Memorias", "Vangrupo"):
        cajas += f"<div class='logo'><span>LOGO</span>{e(marca)}</div>"
    css = f"""
    <style>
    .fila {{ display:flex; justify-content:center; gap: 24px; }}
    .logo {{ width: 240px; height: 96px; border: 2px dashed {DORADO}; border-radius: 10px; display:flex;
      flex-direction:column; align-items:center; justify-content:center; color:{AZUL}; font-weight:700; font-size: 17px; }}
    .logo span {{ font-size: 10px; letter-spacing: .2em; color:#8E8799; margin-bottom: 4px; }}
    </style>"""
    return render("00_logos", css + f"<div class='fila'>{cajas}</div>", 900, 400)


if __name__ == "__main__":
    for fn in (logos, portafolio, embudo, conversacion, objeciones, comisiones, ciclo, equipos):
        print("✔", fn())
