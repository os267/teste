#!/usr/bin/env python3
"""
Ficha Técnica — Productos de Cremación · La Auxiliadora (Vangrupo)
Campaña Día de los Muertos (Finados).

Genera, a partir de una única fuente de datos (PRODUCTOS):
  1. Ficha_Tecnica_Cremacion_Vangrupo.xlsx
       - "Tabla General - Visión Comercial"
       - "Ficha Técnica Consolidada"
  2. Fichas_Tecnicas_Cremacion_Vangrupo.html  (listo para imprimir / guardar en PDF)

Uso:
    pip install pandas openpyxl
    python generar_ficha_tecnica.py [--salida DIRECTORIO]
"""

import argparse
import html
from pathlib import Path

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

# ---------------------------------------------------------------------------
# Identidad visual La Auxiliadora / Vangrupo
# ---------------------------------------------------------------------------
AZUL_MARINO = "1B365D"
AZUL_PROFUNDO = "0F2537"
DORADO = "C5A059"
DORADO_BRILLO = "D4AF37"
FONDO_ALTERNO = "F4F7FA"
FONDO_PROXIMO = "FBF3E1"
TEXTO = "2C3E50"
BLANCO = "FFFFFF"

MARCA = "La Auxiliadora · Vangrupo"
ETIQUETA_PROXIMO = "PRÓXIMO LANZAMIENTO · se lanzará en otro momento"
CAMPANA = "Campaña Día de los Muertos 2026"
N_CUOTAS = 120

# ---------------------------------------------------------------------------
# Fuente única de datos
# ---------------------------------------------------------------------------
PRODUCTOS = [
    {
        "id": "VG-CRE-01",
        "nombre": "Solución Modular de Cremación",
        "submarca": "Línea Cremación Modular",
        "categoria": "Cremación · Módulo add-on",
        "concepto": (
            "Módulo de cremación integrable a cualquier plan funerario vigente o "
            "nuevo de Vangrupo, sin necesidad de cambiar de plan."
        ),
        "capacidad": "Individual (1 titular / beneficiario por módulo).",
        "servicios": [
            "Proceso completo de cremación individual",
            "Urna cineraria de línea modular",
            "Trámites legales básicos",
            "Alquiler temporal de columbario por 1 año en Hogar de las Memorias",
            "Integración al plan funerario base (actual o nuevo)",
        ],
        "perfil": (
            "Afiliados actuales y nuevos que desean incorporar la cremación a su "
            "plan con una cuota mensual mínima."
        ),
        "precio": 1000,
        "precio_nota": "Por módulo individual",
        "pago": (f"Pago en hasta {N_CUOTAS} meses, con intereses.\n"
                 "Debe estar pagado en su totalidad para el uso de la cremación y el columbario"),
        "specs": [
            ("Tipo de producto", "Módulo adicional (add-on) a plan funerario"),
            ("Modalidad de cremación", "Individual"),
            ("Urna", "Cineraria, línea modular"),
            ("Gestión legal", "Trámites básicos incluidos"),
            ("Columbario", "Alquiler temporal · 12 meses incluido en Hogar de las Memorias"),
        ],
    },
    {
        "id": "VG-CRE-03I",
        "nombre": "Jardín de Cenizas · Individual",
        "submarca": "Jardines de la Memoria · Jardín 1",
        "categoria": "Destino final · Inhumación individual",
        "concepto": (
            "Inhumación de la urna de cenizas en un contenedor enterrado con tapa "
            "de granito grabada, en un jardín de plantas de sombra: un lugar "
            "físico de homenaje por 30 años desde la primera inhumación, renovable."
        ),
        "capacidad": "Individual (1 urna).",
        "servicios": [
            "Inhumación de la urna en contenedor individual",
            "Tapa de granito con los datos del difunto",
            "Ubicación en el Jardín 1, con paisajismo de plantas de sombra",
            "Espacio de contemplación con banco",
            "Permanencia de 30 años desde la primera inhumación, renovable por igual período",
        ],
        "perfil": (
            "Familias que desean un lugar propio para visitar y rendir "
            "homenaje, con una inversión moderada."
        ),
        "precio": 600,
        "precio_nota": "Por espacio individual · mantenimiento US$ 15/año",
        "pago": (
            "Pago único o financiado según política comercial vigente. "
            "Cuota de mantenimiento: US$ 15 anual."
        ),
        "specs": [
            ("Ambiente", "Jardín 1"),
            ("Contenedor", "Ø 32 cm × 40 cm de altura; enterrado dejando 20 cm a la vista"),
            ("Identificación", "Tapa de granito con la información del difunto"),
            ("Paisajismo", "Plantas de sombra de diferentes alturas y texturas"),
            ("Acceso", "Camino de 1,2 m en gravilla con bordillo prefabricado"),
            ("Permanencia", "30 años desde la primera inhumación, renovable por igual período"),
            ("Mantenimiento", "US$ 15 anual"),
        ],
    },
    {
        "id": "VG-CRE-03F",
        "nombre": "Jardín de Cenizas · Familiar",
        "submarca": "Jardines de la Memoria · Jardín 1",
        "categoria": "Destino final · Inhumación familiar",
        "concepto": (
            "Parcela familiar en el Jardín 1 con cuatro contenedores agrupados, "
            "cada uno con tapa de granito grabada, con permanencia de 30 años desde la "
            "primera inhumación, renovable por igual período."
        ),
        "capacidad": "Hasta 4 espacios (familiar).",
        "servicios": [
            "Inhumación de hasta 4 urnas",
            "Tapa de granito grabada para cada espacio",
            "Ubicación en el Jardín 1, con paisajismo de plantas de sombra",
            "Lugar de homenaje familiar por 30 años, renovable por igual período",
        ],
        "perfil": (
            "Familias que buscan un espacio propio para varias generaciones."
        ),
        "precio": 2000,
        "precio_nota": "Por parcela familiar · hasta 4 espacios · mantenimiento US$ 24/año",
        "pago": (
            "Pago único o financiado según política comercial vigente. "
            "Cuota de mantenimiento: US$ 24 anual."
        ),
        "specs": [
            ("Ambiente", "Jardín 1"),
            ("Capacidad", "4 contenedores agrupados en losa"),
            ("Identificación", "Tapa de granito por espacio, con la información del difunto"),
            ("Permanencia", "30 años desde la primera inhumación, renovable por igual período"),
            ("Acceso", "Camino de 1,2 m en gravilla con bordillo prefabricado"),
            ("Mantenimiento", "US$ 24 anual"),
        ],
    },
    {
        "id": "VG-CRE-03E",
        "nombre": "Jardín de Cenizas · Ecológico",
        "submarca": "Jardines de la Memoria · Jardín 2",
        "categoria": "Destino final · Inhumación ecológica",
        "concepto": (
            "La urna biodegradable se entierra directamente en el suelo, se cubre "
            "con tierra y se descompone integrándose a la naturaleza. Jardín con "
            "agua corriente y área de esparcimiento de cenizas."
        ),
        "capacidad": "Individual (1 urna).",
        "servicios": [
            "Inhumación ecológica de la urna directamente en el suelo",
            "Placa de identificación",
            "Ubicación en el Jardín 2 o en el Bosque de las Orquídeas",
            "Entorno natural con agua corriente",
            "Permanencia de 3 años; luego, placa memorial en el monumento (incluida)",
        ],
        "perfil": (
            "Personas con conciencia ambiental que desean que sus cenizas vuelvan "
            "a la tierra, con un lugar identificado para visitar."
        ),
        "precio": 750,
        "precio_nota": "Por espacio individual · placa memorial incluida",
        "pago": (
            "Pago único o financiado según política comercial vigente. "
            "Incluye la placa memorial en el monumento al término del plazo."
        ),
        "specs": [
            ("Ambientes", "Jardín 2 · Ecológico o Bosque de las Orquídeas"),
            ("Espacio por urna", "30 × 30 cm, 40 cm de profundidad"),
            ("Urna", "Biodegradable; se integra al suelo"),
            ("Identificación (Jardín 2)", "Placa de madera de 20 cm fijada a una varilla metálica, "
                                         "en posición vertical y sin contacto con el suelo"),
            ("Identificación (Bosque)", "Placa de mármol de 20 × 15 cm"),
            ("Permanencia", "3 años; luego el nombre pasa a una placa memorial en el "
                            "monumento y el espacio se reutiliza"),
            ("Placa memorial", "Incluida en el precio"),
            ("Acceso", "Camino de 1,2 m en gravilla con bordillo prefabricado"),
        ],
    },
    {
        "id": "VG-CRE-04",
        "nombre": "Jardín de Mascotas",
        "submarca": "Jardines de la Memoria · Mascotas",
        "categoria": "Destino final · Inhumación ecológica",
        "concepto": (
            "Jardín para inhumación ecológica de cenizas de mascotas: la urna "
            "biodegradable se entierra directamente en el suelo y se identifica "
            "con una placa de madera."
        ),
        "capacidad": "Individual (una mascota por servicio).",
        "servicios": [
            "Inhumación ecológica de la urna en el jardín",
            "Placa de madera de 20 cm para identificación",
            "Permanencia de 3 años; luego, placa memorial en el monumento (incluida)",
            "Cremación de la mascota y urna biodegradable (opción US$ 550)",
        ],
        "perfil": (
            "Familias que consideran a su mascota parte del hogar y desean un "
            "cierre digno."
        ),
        "precio_texto": "US$ 400 / US$ 550",
        "precios": (400, 550),
        "precio_nota": "US$ 400 solo espacio (urna aparte) · US$ 550 con cremación y urna",
        "pago": (
            "Pago único; puede contratarse como adicional al plan funerario. "
            "La opción de US$ 550 incluye la cremación de la mascota y la urna biodegradable; "
            "en la opción de US$ 400 (solo espacio) la urna biodegradable se adquiere por separado."
        ),
        "specs": [
            ("Tipo de producto", "Servicio de pago único"),
            ("Espacio por urna", "15 × 20 cm o 15 × 30 cm, según el tamaño de la urna"),
            ("Urna", "Biodegradable; se integra al suelo. Incluida solo en la opción con cremación "
                     "(US$ 550); con solo espacio (US$ 400) se adquiere por separado"),
            ("Identificación", "Placa de madera de 20 cm"),
            ("Permanencia", "3 años; luego el espacio se reutiliza"),
            ("Placa memorial", "Incluida en el precio; en el monumento al término del plazo"),
        ],
    },
    {
        "id": "VG-CRE-03C",
        "proximo_lanzamiento": True,
        "nombre": "Jardín de Cenizas · Ceremonial",
        "submarca": "Jardines de la Memoria · Jardín 3",
        "categoria": "Destino final · Inhumación con ceremonia",
        "concepto": (
            "Jardín para inhumación de urnas de cenizas con ceremonia de agua, "
            "con fuentes como elemento central del rito de despedida."
        ),
        "capacidad": "A definir.",
        "servicios": [
            "Inhumación de urnas de cenizas",
            "Ceremonia con agua en fuente",
        ],
        "perfil": (
            "Familias que valoran un rito de despedida simbólico y un entorno "
            "contemplativo."
        ),
        "precio_texto": "A definir",
        "precio_nota": "Producto en definición",
        "pago": "A definir.",
        "specs": [
            ("Ambiente", "Jardín 3"),
            ("Elemento central", "Fuente de agua para la ceremonia"),
            ("Entorno", "Barrera visual que separa el jardín del crematorio"),
        ],
    },
]


# ---------------------------------------------------------------------------
# Portafolio existente (columbarios con cremación) — en la Ficha Técnica, fuera del HTML
# ---------------------------------------------------------------------------
DESCUENTO_EXISTENTES = 0.15
ETIQUETA_DESCUENTO_EXISTENTES = f"Precio Finados y noviembre (−{DESCUENTO_EXISTENTES:.0%})"
PAGO_EXISTENTES = f"Pago único o financiado hasta {N_CUOTAS} meses, con intereses."
UBICACION = ("Definida: se elige el nicho al contratar · A futuro: el nicho se asigna "
             "más adelante. El precio varía según fila y nivel.")

PRODUCTOS_EXISTENTES = [
    {
        "id": "VG-COL-01",
        "nombre": "Columbario Supremo Plus",
        "submarca": "El Hogar de las Memorias",
        "categoria": "Servicio funerario + cremación + columbario",
        "concepto": (
            "Experiencia integral que combina servicio funerario y cremación, con un "
            "espacio conmemorativo para resguardar hasta dos urnas cinerarias en un "
            "entorno de respeto, acompañamiento y serenidad."
        ),
        "capacidad": "Hasta 2 urnas cinerarias (incluye 2 cremaciones).",
        "specs": [
            ("Material", "Cristal o mármol"),
            ("Columbario", "Estándar, espacio permanente para hasta 2 urnas"),
            ("Cremación", "2 cremaciones en crematorio propio, con certificado"),
            ("Preparación y resguardo", "Preparación química y custodia en laboratorio hasta por 5 días"),
            ("Velación", "Sala de velación 24 horas · La Auxiliadora: Capilla Maquilishuat o Básica · "
                         "Capillas Memoriales: Capilla Las Camelias o Básica"),
            ("Ubicación", UBICACION),
        ],
        "servicios": [
            "Columbario estándar de cristal o mármol para hasta 2 urnas",
            "Traslados durante todo el proceso funerario",
            "Preparación química y resguardo hasta por 5 días",
            "2 cremaciones y 2 urnas cinerarias básicas",
            "Certificado de cremación y ceremonias privadas de colocación",
            "Sala de velación 24 h, ataúd ceremonial y carroza tradicional",
            "Asesoría en trámites, libro de condolencias y 50 tarjetas de agradecimiento",
            "Programa Vive (acompañamiento en el duelo) y café y agua ilimitados",
        ],
        "opciones": [("Ubicación definida", 3400, 3900), ("Ubicación a futuro", 2700, 3200)],
        "precio_nota": "Precio según fila y nivel del columbario",
        "pago": PAGO_EXISTENTES,
        "perfil": (
            "Familias que quieren resolver en una sola compra el servicio funerario, la "
            "cremación y un lugar permanente para dos seres queridos."
        ),
    },
    {
        "id": "VG-COL-02",
        "nombre": "Columbario Mármol o Cristal",
        "submarca": "El Hogar de las Memorias",
        "categoria": "Destino final · Columbario",
        "concepto": (
            "Espacio permanente, elegante y sereno en mármol o cristal para preservar el "
            "legado de quienes más ama la familia, con un diseño atemporal."
        ),
        "capacidad": "Estándar: hasta 2 urnas.",
        "specs": [
            ("Material", "Mármol o cristal"),
            ("Permanencia", "Permanente"),
            ("Ubicación", UBICACION),
        ],
        "servicios": [
            "Espacio permanente en columbario de mármol o cristal",
            "Ubicación definida o a futuro, según la opción contratada",
        ],
        "opciones": [("Ubicación definida", 2600, None), ("Ubicación a futuro", 1200, 1900)],
        "precio_nota": "Solo columbario · precio según fila y nivel",
        "pago": PAGO_EXISTENTES,
        "perfil": (
            "Familias que buscan un lugar permanente y elegante para las cenizas, con la "
            "cremación ya resuelta o contratada aparte."
        ),
    },
    {
        "id": "VG-COL-03",
        "nombre": "Columbario Ónix",
        "submarca": "El Hogar de las Memorias",
        "categoria": "Destino final · Columbario premium",
        "concepto": (
            "Columbario de ónix que combina la exclusividad de una piedra natural con un "
            "diseño elegante; sus tonalidades cálidas y apariencia luminosa crean un "
            "espacio de paz, respeto y recuerdo perdurable."
        ),
        "capacidad": "Estándar: hasta 2 urnas · Familiar: hasta 4 urnas.",
        "specs": [
            ("Material", "Ónix natural"),
            ("Modalidades", "Estándar (2 urnas) y Familiar (4 urnas)"),
            ("Permanencia", "Permanente"),
        ],
        "servicios": [
            "Espacio permanente en columbario de ónix natural",
            "Modalidad estándar o familiar",
        ],
        "opciones": [("Estándar · ubicación definida", 3100, None),
                     ("Familiar · ubicación a futuro", 5000, None)],
        "precio_nota": "Solo columbario",
        "pago": PAGO_EXISTENTES,
        "perfil": "Familias que buscan exclusividad y una piedra natural de alta gama para el homenaje.",
    },
    {
        "id": "VG-COL-04",
        "nombre": "Columbario Obra de Arte",
        "submarca": "El Hogar de las Memorias",
        "categoria": "Destino final · Columbario familiar exclusivo",
        "concepto": (
            "Una expresión única de fe, memoria y belleza: tapa de ónix con obra de arte "
            "religiosa que preserva la memoria de toda una familia en un entorno de "
            "serenidad y contemplación."
        ),
        "capacidad": "Familiar: hasta 4 urnas.",
        "specs": [
            ("Material", "Tapa de ónix con obra de arte religiosa"),
            ("Modalidad", "Familiar (4 urnas)"),
            ("Ubicación", "Definida"),
            ("Permanencia", "Permanente"),
        ],
        "servicios": [
            "Columbario familiar permanente para hasta 4 urnas",
            "Tapa exclusiva de ónix con obra de arte religiosa",
        ],
        "opciones": [("Familiar · ubicación definida", 12500, None)],
        "precio_nota": "Solo columbario",
        "pago": PAGO_EXISTENTES,
        "perfil": "Familias de fe que desean un legado único y de máxima exclusividad.",
    },
    {
        "id": "VG-COL-05",
        "nombre": "Columbario Cristal · Bella Vista",
        "submarca": "Mausoleo vertical Bella Vista",
        "categoria": "Cremación + columbario",
        "concepto": (
            "Columbario de cristal en el mausoleo vertical Bella Vista que incluye el proceso "
            "completo de cremación: traslados, preparación, cremaciones, urnas y ceremonia "
            "de colocación."
        ),
        "capacidad": "Estándar: 2 cremaciones y 2 urnas · Familiar: 4 cremaciones y 4 urnas.",
        "specs": [
            ("Ubicación", "Mausoleo vertical Bella Vista"),
            ("Material", "Cristal"),
            ("Medidas", "30 × 30 × 30 cm"),
            ("Cremación", "2 (estándar) o 4 (familiar) cremaciones, con certificado"),
            ("Preparación y resguardo", "Preparación química y custodia en laboratorio hasta por 5 días"),
        ],
        "servicios": [
            "Columbario de cristal permanente (estándar o familiar)",
            "Traslados durante todo el proceso",
            "Preparación química y resguardo hasta por 5 días",
            "2 o 4 cremaciones y 2 o 4 urnas cinerarias básicas",
            "Certificado de cremación y ceremonias privadas de colocación",
        ],
        "opciones": [("Estándar · ubicación definida", 1800, None),
                     ("Estándar · ubicación a futuro", 1300, None),
                     ("Familiar · ubicación definida", 2900, None),
                     ("Familiar · ubicación a futuro", 2300, None)],
        "precio_nota": "Incluye cremación · precio según modalidad y ubicación",
        "pago": PAGO_EXISTENTES,
        "perfil": (
            "Familias que buscan la opción más accesible de cremación con columbario "
            "permanente, para 2 o 4 personas."
        ),
    },
]


def _rango(mn, mx, f=1.0) -> str:
    return usd(mn * f) if mx is None else f"{usd(mn * f)} – {usd(mx * f)}"


def texto_opciones(p: dict, f: float = 1.0) -> str:
    """Una línea por opción de precio (ubicación / modalidad)."""
    return "\n".join(f"{etq}: {_rango(mn, mx, f)}" for etq, mn, mx in p["opciones"])


# ---------------------------------------------------------------------------
# Utilidades de formato
# ---------------------------------------------------------------------------
def usd(valor: float) -> str:
    """US$ con separador de miles '.' y decimales ',' (formato latinoamericano)."""
    entero, dec = f"{valor:,.2f}".split(".")
    entero = entero.replace(",", ".")
    return f"US$ {entero}" if dec == "00" else f"US$ {entero},{dec}"


def texto_precio(p: dict) -> str:
    """Precio único, o rango cuando depende de variables (p. ej. cantidad de personas)."""
    if "precio_texto" in p:
        return p["precio_texto"]
    if "precio" in p:
        return usd(p["precio"])
    return f"{usd(p['precio_min'])} – {usd(p['precio_max'])}"


DESCUENTO_LANZAMIENTO = 0.20
ETIQUETA_DESCUENTO = f"Precio lanzamiento (−{DESCUENTO_LANZAMIENTO:.0%})"


def texto_lanzamiento(p: dict) -> str:
    """Precio con el descuento especial de lanzamiento."""
    f = 1 - DESCUENTO_LANZAMIENTO
    if "precios" in p:
        return " / ".join(usd(v * f) for v in p["precios"])
    if "precio" not in p:
        return "A definir"
    return usd(p["precio"] * f)


def viñetas(items: list) -> str:
    return "\n".join(f"• {i}" for i in items)


def relleno(color: str) -> PatternFill:
    return PatternFill("solid", start_color=color, end_color=color)


def borde(color: str, estilo: str = "thin") -> Border:
    lado = Side(style=estilo, color=color)
    return Border(left=lado, right=lado, top=lado, bottom=lado)


# ---------------------------------------------------------------------------
# Aba 1: Tabla General
# ---------------------------------------------------------------------------
COLUMNAS = [
    ("Nombre Comercial", 26),
    ("Categoría / Línea", 24),
    ("Concepto / Descripción", 42),
    ("Capacidad / Cobertura", 24),
    ("Servicios Incluidos & Diferenciales", 46),
    ("Perfil de Cliente", 36),
    ("Precio Sugerido (USD)", 22),
    (ETIQUETA_DESCUENTO, 22),
    ("Condiciones de Pago / Financiamiento", 34),
]

HOJA_TABLA = "Tabla Gral. - Visión Comercial"  # límite Excel: 31 caracteres
HOJA_FICHA = "Ficha Técnica Consolidada"
FILA_ENCABEZADO = 4  # 1: título, 2: subtítulo, 3: vacía, 4: encabezados


def dataframe_comercial() -> pd.DataFrame:
    filas = []
    for p in PRODUCTOS:
        filas.append([
            p["nombre"] + ("\n★ PRÓXIMO LANZAMIENTO" if p.get("proximo_lanzamiento") else ""),
            p["categoria"],
            p["concepto"],
            p["capacidad"],
            viñetas(p["servicios"]),
            p["perfil"],
            f"{texto_precio(p)}\n({p['precio_nota']})",
            texto_lanzamiento(p) + ("" if p.get("proximo_lanzamiento") else "\n(descuento de lanzamiento · Finados y noviembre)"),
            p["pago"],
        ])
    return pd.DataFrame(filas, columns=[c for c, _ in COLUMNAS])


def estilizar_tabla(ws) -> None:
    ncols = len(COLUMNAS)
    ultima = get_column_letter(ncols)

    # Título y subtítulo
    ws.merge_cells(f"A1:{ultima}1")
    ws["A1"] = f"{MARCA.upper()}  |  PORTAFOLIO DE CREMACIÓN — VISIÓN COMERCIAL"
    ws["A1"].font = Font(name="Calibri", size=16, bold=True, color=BLANCO)
    ws["A1"].fill = relleno(AZUL_PROFUNDO)
    ws["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[1].height = 34

    ws.merge_cells(f"A2:{ultima}2")
    ws["A2"] = CAMPANA
    ws["A2"].font = Font(name="Calibri", size=11, italic=True, bold=True, color=AZUL_PROFUNDO)
    ws["A2"].fill = relleno(DORADO)
    ws["A2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[2].height = 22

    # Encabezados
    for col, (_, ancho) in enumerate(COLUMNAS, start=1):
        ws.column_dimensions[get_column_letter(col)].width = ancho
        c = ws.cell(row=FILA_ENCABEZADO, column=col)
        c.font = Font(name="Calibri", size=11, bold=True, color=BLANCO)
        c.fill = relleno(AZUL_MARINO)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = Border(bottom=Side(style="medium", color=DORADO),
                          left=Side(style="thin", color=DORADO),
                          right=Side(style="thin", color=DORADO))
    ws.row_dimensions[FILA_ENCABEZADO].height = 36

    # Datos
    borde_fino = borde("D5DCE4")
    for i, fila in enumerate(ws.iter_rows(min_row=FILA_ENCABEZADO + 1,
                                          max_row=ws.max_row, max_col=ncols)):
        proximo = PRODUCTOS[i].get("proximo_lanzamiento", False)
        fondo = relleno(FONDO_PROXIMO) if proximo else (
            relleno(FONDO_ALTERNO) if i % 2 == 0 else relleno(BLANCO))
        max_lineas = 1
        for c in fila:
            c.fill = fondo
            c.border = borde_fino
            c.font = Font(name="Calibri", size=10, color=TEXTO)
            c.alignment = Alignment(vertical="top", wrap_text=True)
            ancho = ws.column_dimensions[c.column_letter].width
            texto = str(c.value or "")
            lineas = sum(max(1, -(-len(l) // int(ancho * 1.1))) for l in texto.split("\n"))
            max_lineas = max(max_lineas, lineas)
        fila[0].font = Font(name="Calibri", size=11, bold=True, color=AZUL_MARINO)
        if proximo:
            for c in fila:
                c.border = Border(top=Side(style="medium", color=DORADO),
                                  bottom=Side(style="medium", color=DORADO))
        fila[6].font = Font(name="Calibri", size=11, bold=True, color=AZUL_PROFUNDO)
        ws.row_dimensions[fila[0].row].height = max(30, 14.5 * max_lineas + 6)

    ws.freeze_panes = ws.cell(row=FILA_ENCABEZADO + 1, column=2)
    ws.auto_filter.ref = f"A{FILA_ENCABEZADO}:{ultima}{ws.max_row}"
    ws.sheet_view.showGridLines = False
    ws.sheet_properties.tabColor = AZUL_MARINO
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_title_rows = f"{FILA_ENCABEZADO}:{FILA_ENCABEZADO}"


# ---------------------------------------------------------------------------
# Aba 2: Ficha Técnica Consolidada (fichas individuales apiladas)
# ---------------------------------------------------------------------------
# Columnas: A (margen) | B (etiqueta) | C-E (valor) | F (margen)
COL_ETQ, COL_INI, COL_FIN = 2, 3, 5


def _bloque_titulo(ws, fila: int, texto: str) -> int:
    ws.merge_cells(start_row=fila, start_column=COL_ETQ, end_row=fila, end_column=COL_FIN)
    c = ws.cell(row=fila, column=COL_ETQ, value=texto.upper())
    c.font = Font(name="Calibri", size=10, bold=True, color=AZUL_PROFUNDO)
    c.fill = relleno(DORADO)
    c.alignment = Alignment(vertical="center", indent=1)
    ws.row_dimensions[fila].height = 20
    return fila + 1


def _fila_dato(ws, fila: int, etiqueta: str, valor: str, alterna: bool,
               destacado: bool = False) -> int:
    ce = ws.cell(row=fila, column=COL_ETQ, value=etiqueta)
    ce.font = Font(name="Calibri", size=10, bold=True, color=AZUL_MARINO)
    ce.alignment = Alignment(vertical="top", wrap_text=True, indent=1)
    ws.merge_cells(start_row=fila, start_column=COL_INI, end_row=fila, end_column=COL_FIN)
    cv = ws.cell(row=fila, column=COL_INI, value=valor)
    cv.alignment = Alignment(vertical="top", wrap_text=True)
    if destacado:
        cv.font = Font(name="Calibri", size=13, bold=True, color=AZUL_PROFUNDO)
    else:
        cv.font = Font(name="Calibri", size=10, color=TEXTO)
    fondo = relleno(FONDO_ALTERNO if alterna else BLANCO)
    for col in range(COL_ETQ, COL_FIN + 1):
        ws.cell(row=fila, column=col).fill = fondo
    lineas = sum(max(1, -(-len(l) // 78)) for l in str(valor).split("\n"))
    ws.row_dimensions[fila].height = max(20, 14.5 * lineas + 6) + (6 if destacado else 0)
    return fila + 1


def _marco(ws, fila_ini: int, fila_fin: int) -> None:
    """Borde dorado alrededor de la ficha."""
    grueso = Side(style="medium", color=DORADO)
    fino = Side(style="hair", color="D5DCE4")
    for f in range(fila_ini, fila_fin + 1):
        for col in range(COL_ETQ, COL_FIN + 1):
            c = ws.cell(row=f, column=col)
            c.border = Border(
                left=grueso if col == COL_ETQ else None,
                right=grueso if col == COL_FIN else None,
                top=grueso if f == fila_ini else None,
                bottom=grueso if f == fila_fin else fino,
            )


def _precios_lanzamiento(p: dict) -> list:
    return [("Precio sugerido", texto_precio(p), True),
            (ETIQUETA_DESCUENTO, texto_lanzamiento(p), True)]


def _precios_existentes(p: dict) -> list:
    return [("Precio", texto_opciones(p), True),
            (ETIQUETA_DESCUENTO_EXISTENTES, texto_opciones(p, 1 - DESCUENTO_EXISTENTES), True)]


def _seccion(ws, fila: int, titulo: str, subtitulo: str) -> int:
    """Franja que separa los grupos de fichas dentro de la misma aba."""
    for texto, tamano, color, alto in ((titulo, 13, BLANCO, 30), (subtitulo, 10, DORADO, 20)):
        ws.merge_cells(start_row=fila, start_column=COL_ETQ, end_row=fila, end_column=COL_FIN)
        c = ws.cell(row=fila, column=COL_ETQ, value=texto)
        c.font = Font(name="Calibri", size=tamano, bold=True, color=color)
        c.fill = relleno(AZUL_PROFUNDO)
        c.alignment = Alignment(horizontal="center", vertical="center")
        ws.row_dimensions[fila].height = alto
        fila += 1
    return fila + 1


def construir_fichas(ws, titulo="FICHA TÉCNICA CONSOLIDADA",
                     subtitulo=f"Portafolio de Cremación — {CAMPANA} y portafolio existente") -> None:
    secciones = [
        ("LANZAMIENTOS · FINADOS 2026",
         "Solución Modular y Jardines de la Memoria · descuento de lanzamiento −20%",
         PRODUCTOS, _precios_lanzamiento),
        ("PORTAFOLIO EXISTENTE · COLUMBARIOS",
         f"Columbarios y cremación · descuento −{DESCUENTO_EXISTENTES:.0%} en Finados y noviembre",
         PRODUCTOS_EXISTENTES, _precios_existentes),
    ]
    ws.sheet_view.showGridLines = False
    ws.sheet_properties.tabColor = DORADO
    for col, ancho in zip("ABCDEF", (3, 30, 30, 30, 30, 3)):
        ws.column_dimensions[col].width = ancho

    ws.merge_cells(start_row=1, start_column=COL_ETQ, end_row=1, end_column=COL_FIN)
    c = ws.cell(row=1, column=COL_ETQ, value=f"{titulo}  ·  {MARCA.upper()}")
    c.font = Font(name="Calibri", size=16, bold=True, color=BLANCO)
    c.fill = relleno(AZUL_PROFUNDO)
    c.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 34
    ws.merge_cells(start_row=2, start_column=COL_ETQ, end_row=2, end_column=COL_FIN)
    c = ws.cell(row=2, column=COL_ETQ, value=subtitulo)
    c.font = Font(name="Calibri", size=11, italic=True, color=DORADO)
    c.fill = relleno(AZUL_PROFUNDO)
    c.alignment = Alignment(horizontal="center", vertical="center")

    fila = 4
    saltos = []
    fichas = []
    for sec_titulo, sec_sub, productos, precios in secciones:
        fichas.append((sec_titulo, sec_sub, None, None))
        fichas += [(None, None, p, precios) for p in productos]
    for n, (sec_titulo, sec_sub, p, precios) in enumerate(fichas):
        if p is None:
            if n:
                saltos.append(fila - 2)
            fila = _seccion(ws, fila, sec_titulo, sec_sub)
            continue
        inicio = fila

        # Encabezado de la ficha
        ws.merge_cells(start_row=fila, start_column=COL_ETQ, end_row=fila, end_column=COL_FIN)
        c = ws.cell(row=fila, column=COL_ETQ, value=p["nombre"].upper())
        c.font = Font(name="Calibri", size=14, bold=True, color=BLANCO)
        c.alignment = Alignment(vertical="center", indent=1)
        for col in range(COL_ETQ, COL_FIN + 1):
            ws.cell(row=fila, column=col).fill = relleno(AZUL_MARINO)
        ws.row_dimensions[fila].height = 30
        fila += 1
        ws.merge_cells(start_row=fila, start_column=COL_ETQ, end_row=fila, end_column=COL_FIN)
        c = ws.cell(row=fila, column=COL_ETQ, value=f"{p['submarca']}  ·  {p['categoria']}")
        c.font = Font(name="Calibri", size=10, italic=True, color=BLANCO)
        c.alignment = Alignment(vertical="center", indent=1)
        for col in range(COL_ETQ, COL_FIN + 1):
            ws.cell(row=fila, column=col).fill = relleno(AZUL_PROFUNDO)
        ws.row_dimensions[fila].height = 20
        fila += 1
        if p.get("proximo_lanzamiento"):
            ws.merge_cells(start_row=fila, start_column=COL_ETQ, end_row=fila, end_column=COL_FIN)
            c = ws.cell(row=fila, column=COL_ETQ, value=f"★  {ETIQUETA_PROXIMO}")
            c.font = Font(name="Calibri", size=11, bold=True, color=AZUL_PROFUNDO)
            c.alignment = Alignment(horizontal="center", vertical="center")
            for col in range(COL_ETQ, COL_FIN + 1):
                ws.cell(row=fila, column=col).fill = relleno(DORADO_BRILLO)
            ws.row_dimensions[fila].height = 24
            fila += 1

        fila = _bloque_titulo(ws, fila, "Visión General")
        fila = _fila_dato(ws, fila, "Concepto", p["concepto"], True)
        fila = _fila_dato(ws, fila, "Capacidad / Cobertura", p["capacidad"], False)

        fila = _bloque_titulo(ws, fila, "Especificaciones Técnicas")
        for i, (k, v) in enumerate(p["specs"]):
            fila = _fila_dato(ws, fila, k, v, i % 2 == 0)
        fila = _fila_dato(ws, fila, "Servicios incluidos", viñetas(p["servicios"]),
                          len(p["specs"]) % 2 == 0)

        fila = _bloque_titulo(ws, fila, "Precio & Condiciones de Pago")
        for i, (etq, valor, dest) in enumerate(precios(p)):
            fila = _fila_dato(ws, fila, etq, valor, i % 2 == 0, destacado=dest)
        fila = _fila_dato(ws, fila, "Base de precio", p["precio_nota"], False)
        fila = _fila_dato(ws, fila, "Condiciones", p["pago"], True)

        fila = _bloque_titulo(ws, fila, "Perfil del Comprador")
        fila = _fila_dato(ws, fila, "Cliente objetivo", p["perfil"], True)

        _marco(ws, inicio, fila - 1)
        if n < len(fichas) - 1 and fichas[n + 1][2] is not None:
            saltos.append(fila)
        fila += 2  # separación entre fichas

    from openpyxl.worksheet.pagebreak import Break
    for f in saltos:
        ws.row_breaks.append(Break(id=f))
    ws.page_setup.orientation = "portrait"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_area = f"A1:F{fila - 2}"


# ---------------------------------------------------------------------------
# Aba 3: Política de comisiones de los productos de cremación
# ---------------------------------------------------------------------------
HOJA_COMISIONES = "Política de Comisiones"
IVA = 0.13
PRECIO_MODULAR = 1000  # con IVA; base del ejemplo de la escala

# (ventas en el mes, % comisión, cantidad de Soluciones Modulares del ejemplo, lectura)
ESCALA_COMISION = [
    ("1 venta", 0.08, 1, "Entrada"),
    ("2 ventas", 0.10, 2, ""),
    ("3 ventas o más", 0.12, 3, "Máximo"),
]

# (producto, momento de pago, estorno, observaciones)
PAGO_COMISION = [
    ("Solución Modular de Cremación", "Pago único cuando el cliente paga la 3ª cuota",
     "Si el cliente cancela antes de la 12ª cuota", ""),
    ("Jardines de Cenizas (Individual, Familiar, Ecológico)",
     "Contado: mes siguiente al pago. Financiado: proporcional a lo cobrado",
     "Cancelación en los primeros 90 días", ""),
    ("Jardín de Mascotas", "Mes siguiente al pago (pago único)", "Cancelación en los primeros 90 días", ""),
    ("Columbarios (portafolio existente)",
     "Contado: mes siguiente al pago. Financiado: proporcional a lo cobrado",
     "Cancelación en los primeros 90 días", "Mismo criterio de cantidad de ventas que los productos nuevos."),
]

REGLAS_COMISION = [
    "1 venta en el mes de cualquier producto de cremación = 8%; 2 ventas = 10%; 3 o más = 12%, "
    "sobre toda la facturación del mes.",
    "Cada contrato vendido cuenta como 1 venta, sin distinción por grupo de producto (nuevos y columbarios).",
    "Base de cálculo: facturación sin IVA (13%), neta de descuentos. La comisión se paga sobre lo cobrado.",
    "Mismo criterio para call center, contratados y freelancers. No hay bonos adicionales.",
    "Venta compartida (call center agenda, otro vendedor cierra): 1 venta para ambos; comisión 30% / 70%.",
    "No generan comisión ni cuentan como venta: cuotas de mantenimiento anual (US$ 15 / US$ 24).",
    "Estorno: la comisión se descuenta de los pagos siguientes al vendedor. Ventas anuladas no cuentan.",
]

ANCHOS_COMISION = [40, 30, 40, 36]


def _encabezado_tabla(ws, fila, titulos) -> None:
    for col, titulo in enumerate(titulos, start=1):
        c = ws.cell(row=fila, column=col, value=titulo)
        c.font = Font(name="Calibri", size=11, bold=True, color=BLANCO)
        c.fill = relleno(AZUL_MARINO)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = Border(bottom=Side(style="medium", color=DORADO))
    ws.row_dimensions[fila].height = 32


def _franja(ws, fila, texto, ncols) -> None:
    ws.merge_cells(start_row=fila, start_column=1, end_row=fila, end_column=ncols)
    c = ws.cell(row=fila, column=1, value=texto)
    c.font = Font(name="Calibri", size=10, bold=True, color=AZUL_PROFUNDO)
    c.fill = relleno(DORADO)
    c.alignment = Alignment(vertical="center", indent=1)
    ws.row_dimensions[fila].height = 20


def construir_comisiones(ws) -> None:
    ws.sheet_view.showGridLines = False
    ws.sheet_properties.tabColor = AZUL_PROFUNDO
    ncols = len(ANCHOS_COMISION)
    ultima = get_column_letter(ncols)
    for col, ancho in enumerate(ANCHOS_COMISION, start=1):
        ws.column_dimensions[get_column_letter(col)].width = ancho

    ws.merge_cells(f"A1:{ultima}1")
    ws["A1"] = f"{MARCA.upper()}  |  POLÍTICA DE COMISIONES DE LOS PRODUCTOS DE CREMACIÓN"
    ws["A1"].font = Font(name="Calibri", size=16, bold=True, color=BLANCO)
    ws["A1"].fill = relleno(AZUL_PROFUNDO)
    ws["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[1].height = 34
    ws.merge_cells(f"A2:{ultima}2")
    ws["A2"] = "Vigente en 2026 · comisión según la cantidad de ventas del mes (8% · 10% · 12%)"
    ws["A2"].font = Font(name="Calibri", size=11, bold=True, color=AZUL_PROFUNDO)
    ws["A2"].fill = relleno(DORADO_BRILLO)
    ws["A2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[2].height = 22

    borde_fino = borde("D5DCE4")

    def fila_datos(f, valores, i):
        fondo = relleno(FONDO_ALTERNO if i % 2 == 0 else BLANCO)
        for col, v in enumerate(valores, start=1):
            c = ws.cell(row=f, column=col, value=v)
            c.fill = fondo
            c.border = borde_fino
            c.font = Font(name="Calibri", size=10, color=TEXTO)
            c.alignment = Alignment(vertical="center", wrap_text=True)
        ws.cell(row=f, column=1).font = Font(name="Calibri", size=11, bold=True, color=AZUL_MARINO)

    f = 4
    _franja(ws, f, "1. ESCALA POR CANTIDAD DE VENTAS EN EL MES (cualquier producto de cremación)", ncols)
    f += 1
    _encabezado_tabla(ws, f, ["Ventas en el mes", "% comisión",
                              "Ejemplo: facturación con Solución Modular (sin IVA)", "Comisión del ejemplo"])
    sin_iva = round(100 * (1 + IVA))
    for i, (ventas, pct, cant, _lectura) in enumerate(ESCALA_COMISION):
        f += 1
        fila_datos(f, [ventas, pct, f"={cant}*{PRECIO_MODULAR}*100/{sin_iva}", f"=B{f}*C{f}"], i)
        ws.cell(row=f, column=2).number_format = "0%"
        ws.cell(row=f, column=2).font = Font(name="Calibri", size=12, bold=True, color=AZUL_PROFUNDO)
        ws.cell(row=f, column=2).alignment = Alignment(horizontal="center", vertical="center")
        for col in (3, 4):
            ws.cell(row=f, column=col).number_format = '"US$" #,##0.00'
            ws.cell(row=f, column=col).alignment = Alignment(horizontal="center", vertical="center")
        ws.cell(row=f, column=4).font = Font(name="Calibri", size=11, bold=True, color=AZUL_PROFUNDO)
        ws.row_dimensions[f].height = 24

    f += 2
    _franja(ws, f, "2. CUÁNDO SE PAGA Y CUÁNDO SE DESCUENTA", ncols)
    f += 1
    _encabezado_tabla(ws, f, ["Producto", "Momento de pago", "Estorno", "Observaciones"])
    for i, valores in enumerate(PAGO_COMISION):
        f += 1
        fila_datos(f, list(valores), i)
        ws.row_dimensions[f].height = 36

    f += 2
    _franja(ws, f, "3. REGLAS GENERALES", ncols)
    for n, regla in enumerate(REGLAS_COMISION, start=1):
        f += 1
        ws.merge_cells(start_row=f, start_column=1, end_row=f, end_column=ncols)
        c = ws.cell(row=f, column=1, value=f"{n}. {regla}")
        c.font = Font(name="Calibri", size=10, color=TEXTO)
        c.alignment = Alignment(vertical="center", wrap_text=True, indent=1)
        ws.row_dimensions[f].height = 22

    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True


def generar_excel(ruta: Path) -> None:
    df = dataframe_comercial()
    with pd.ExcelWriter(ruta, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name=HOJA_TABLA, index=False, startrow=FILA_ENCABEZADO - 1)
        writer.book.create_sheet(HOJA_FICHA)
        writer.book.create_sheet(HOJA_COMISIONES)

    wb = load_workbook(ruta)
    estilizar_tabla(wb[HOJA_TABLA])
    construir_fichas(wb[HOJA_FICHA])
    construir_comisiones(wb[HOJA_COMISIONES])
    wb.properties.title = f"Ficha Técnica Cremación — {MARCA}"
    wb.properties.creator = MARCA
    wb.save(ruta)


# ---------------------------------------------------------------------------
# Entrega 2: Fichas en HTML (imprimibles / exportables a PDF)
# ---------------------------------------------------------------------------
CSS = f"""
:root {{
  --azul: #{AZUL_MARINO}; --azul-profundo: #{AZUL_PROFUNDO};
  --dorado: #{DORADO}; --dorado-brillo: #{DORADO_BRILLO};
  --alterno: #{FONDO_ALTERNO}; --texto: #{TEXTO};
}}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: #E9EDF2; color: var(--texto);
  font-family: "Montserrat", "Segoe UI", Calibri, Arial, sans-serif; line-height: 1.45; }}
.portada {{ max-width: 820px; margin: 32px auto 0; padding: 0 16px; text-align: center; }}
.portada h1 {{ font-family: "Playfair Display", Georgia, serif; color: var(--azul-profundo);
  margin: 0 0 4px; font-size: 28px; }}
.portada p {{ margin: 0; color: var(--dorado); font-weight: 600; letter-spacing: .08em;
  text-transform: uppercase; font-size: 12px; }}
.ficha {{ max-width: 820px; margin: 24px auto; background: #fff;
  border: 2px solid var(--dorado); box-shadow: 0 6px 24px rgba(15,37,55,.12); }}
.ficha header {{ background: linear-gradient(135deg, var(--azul-profundo), var(--azul));
  color: #fff; padding: 22px 28px 18px; border-bottom: 4px solid var(--dorado); }}
.ficha header .marca {{ display: flex; justify-content: space-between; font-size: 11px;
  letter-spacing: .14em; text-transform: uppercase; color: var(--dorado-brillo); font-weight: 700; }}
.ficha header h2 {{ font-family: "Playfair Display", Georgia, serif; margin: 10px 0 4px;
  font-size: 26px; font-weight: 700; }}
.ficha header .sub {{ font-style: italic; opacity: .85; font-size: 13px; }}
.ficha.proximo {{ border: 3px dashed var(--dorado); }}
.ficha .aviso {{ background: var(--dorado-brillo); color: var(--azul-profundo); text-align: center;
  font-weight: 700; font-size: 13px; letter-spacing: .12em; text-transform: uppercase; padding: 8px 16px; }}
.cuerpo {{ padding: 8px 28px 24px; }}
.bloque h3 {{ margin: 18px 0 8px; font-size: 12px; letter-spacing: .12em; text-transform: uppercase;
  color: var(--azul-profundo); border-left: 4px solid var(--dorado); padding: 4px 10px;
  background: linear-gradient(90deg, rgba(197,160,89,.22), transparent); }}
table {{ width: 100%; border-collapse: collapse; font-size: 13.5px; }}
th, td {{ text-align: left; vertical-align: top; padding: 7px 10px; border-bottom: 1px solid #E1E6EC; }}
th {{ width: 34%; color: var(--azul); font-weight: 700; }}
tr:nth-child(odd) {{ background: var(--alterno); }}
ul {{ margin: 0; padding-left: 18px; }}
li {{ margin: 2px 0; }}
.precio {{ display: flex; flex-wrap: wrap; gap: 16px; align-items: stretch; }}
.precio .monto {{ flex: 0 0 auto; background: var(--azul); color: #fff; padding: 14px 20px;
  border-bottom: 3px solid var(--dorado); min-width: 220px; }}
.precio .monto small {{ display: block; color: var(--dorado-brillo); font-size: 11px;
  letter-spacing: .1em; text-transform: uppercase; }}
.precio .monto strong {{ font-size: 24px; font-family: "Playfair Display", Georgia, serif; }}
.precio .monto span {{ display: block; font-size: 12px; opacity: .85; }}
.precio .monto.lanz {{ background: var(--dorado); color: var(--azul-profundo); }}
.precio .monto.lanz small {{ color: var(--azul-profundo); }}
.precio .cond {{ flex: 1 1 260px; background: var(--alterno); padding: 12px 16px; font-size: 13.5px; }}
.perfil {{ font-size: 14px; }}
footer {{ border-top: 1px solid #E1E6EC; padding: 10px 28px; font-size: 11px; color: #7A8794;
  display: flex; justify-content: space-between; }}
@media (max-width: 600px) {{
  .cuerpo, .ficha header, footer {{ padding-left: 16px; padding-right: 16px; }}
  th {{ width: 42%; }}
}}
@media print {{
  @page {{ size: A4; margin: 12mm; }}
  body {{ background: #fff; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  .portada {{ display: none; }}
  .ficha {{ box-shadow: none; margin: 0 auto; max-width: none; zoom: .8;
    page-break-after: always; break-after: page; break-inside: avoid; }}
  .bloque h3 {{ margin: 12px 0 6px; }}
  th, td {{ padding: 5px 10px; }}
  .ficha:last-of-type {{ page-break-after: auto; break-after: auto; }}
}}
"""


def _li(items: list) -> str:
    return "<ul>" + "".join(f"<li>{html.escape(i)}</li>" for i in items) + "</ul>"


def ficha_html(p: dict) -> str:
    e = html.escape
    specs = "".join(f"<tr><th>{e(k)}</th><td>{e(v)}</td></tr>" for k, v in p["specs"])
    aviso = (f'\n  <div class="aviso">★ {e(ETIQUETA_PROXIMO)}</div>'
             if p.get("proximo_lanzamiento") else "")
    return f"""
<article class="ficha{' proximo' if p.get('proximo_lanzamiento') else ''}">
  <header>
    <div class="marca"><span>{e(MARCA)}</span><span>Ficha Técnica</span></div>
    <h2>{e(p['nombre'])}</h2>
    <div class="sub">{e(p['submarca'])} · {e(p['categoria'])}</div>
  </header>{aviso}
  <div class="cuerpo">
    <section class="bloque"><h3>Visión General</h3>
      <table>
        <tr><th>Concepto</th><td>{e(p['concepto'])}</td></tr>
        <tr><th>Capacidad / Cobertura</th><td>{e(p['capacidad'])}</td></tr>
      </table>
    </section>
    <section class="bloque"><h3>Especificaciones Técnicas</h3>
      <table>{specs}<tr><th>Servicios incluidos</th><td>{_li(p['servicios'])}</td></tr></table>
    </section>
    <section class="bloque"><h3>Precio &amp; Condiciones de Pago</h3>
      <div class="precio">
        <div class="monto"><small>Precio sugerido</small><strong>{e(texto_precio(p))}</strong>
          <span>{e(p['precio_nota'])}</span></div>
        <div class="monto lanz"><small>{e(ETIQUETA_DESCUENTO)}</small><strong>{e(texto_lanzamiento(p))}</strong>
          <span>Lanzamiento · válido en Finados y noviembre</span></div>
        <div class="cond"><b>Condiciones:</b> {e(p['pago'])}</div>
      </div>
    </section>
    <section class="bloque"><h3>Perfil del Comprador</h3>
      <p class="perfil">{e(p['perfil'])}</p>
    </section>
  </div>
  <footer><span>{e(CAMPANA)}</span></footer>
</article>"""


def generar_html(ruta: Path) -> None:
    fichas = "\n".join(ficha_html(p) for p in PRODUCTOS)
    ruta.write_text(f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Fichas Técnicas Cremación</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="portada">
  <h1>Portafolio de Cremación</h1>
  <p>{html.escape(MARCA)} · {html.escape(CAMPANA)}</p>
</div>
{fichas}
</body>
</html>
""", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--salida", default=".", help="Directorio de salida")
    args = parser.parse_args()
    salida = Path(args.salida)
    salida.mkdir(parents=True, exist_ok=True)

    xlsx = salida / "Ficha_Tecnica_Cremacion_Vangrupo.xlsx"
    pagina = salida / "Fichas_Tecnicas_Cremacion_Vangrupo.html"
    generar_excel(xlsx)
    generar_html(pagina)
    print(f"✔ Excel generado: {xlsx}")
    print(f"✔ HTML generado:  {pagina}")


if __name__ == "__main__":
    main()
