"""
Contenido del Playbook Comercial — Portafolio de Cremación y Jardines de Cenizas.
La Auxiliadora · Hogar de las Memorias · Parque Memorial Las Colinas · Vangrupo.

Fuente única para la versión Google Docs (generar_docx.py) y la versión Canva
(generar_pptx.py). Datos de productos y precios: Ficha Técnica Cremación Vangrupo
(oct/2026) y diseño Canva "Jardines de Cenizas" (Luana Magedanz).
Estructura inspirada en el Playbook de Ventas Alta Loma.
"""

TITULO = "Playbook Comercial"
SUBTITULO = "Portafolio de Cremación y Jardines de Cenizas"
MARCAS = "La Auxiliadora · Hogar de las Memorias · Las Colinas · Vangrupo"
CAMPANA = "Campaña Día de los Muertos 2026"
LEMA = "Acompañar, no vender: la familia primero, siempre."
VERSION = "Versión 1.1 · Octubre 2026 · Uso interno del equipo comercial"

COMO_USAR = (
    "Este playbook es la referencia única del equipo comercial para el portafolio "
    "de cremación y jardines de cenizas. Reúne reglas, precios, discurso por producto, "
    "manejo de objeciones y política de comisiones. Se revisa cada trimestre con la "
    "Gerencia Comercial. Si algo cambia en la Ficha Técnica, este documento se actualiza."
)

PENDIENTES = [
    "Política de comisiones de los productos de cremación: 1 venta en el mes = 8%, 2 ventas = 10%, 3 o más = 12% sobre la facturación.",
    "Placas de madera: confirmar el tratamiento de la madera para contacto con el suelo.",
    "Jardín Ceremonial: producto en definición. No se vende ni se cotiza todavía.",
]

INDICE = [
    ("01", "Quiénes somos y lo que vendemos"),
    ("02", "A quién le vendemos"),
    ("03", "El proceso de venta"),
    ("04", "Producto por producto: speech y reglas"),
    ("05", "Manejo de objeciones"),
    ("06", "Precios, reglas y condiciones"),
    ("07", "Política de comisiones de los productos de cremación"),
    ("08", "Herramientas de apoyo"),
]

# ---------------------------------------------------------------------------
# 01 · Quiénes somos
# ---------------------------------------------------------------------------
QUIENES_SOMOS = (
    "En La Auxiliadora, Hogar de las Memorias y Parque Memorial Las Colinas, empresas de Vangrupo, no vendemos "
    "nichos, parcelas ni servicios: acompañamos a las familias salvadoreñas a honrar "
    "la memoria de quienes aman. La cremación es una decisión cada vez más elegida, y "
    "nuestros nuevos jardines de cenizas responden a una pregunta que muchas familias "
    "se hacen y pocas se atreven a decir: \"¿y después de la cremación, dónde las "
    "visitamos?\"."
)

POR_QUE_AHORA = [
    ("Un lugar para volver",
     "La familia tiene un sitio físico, digno y verde para visitar y recordar."),
    ("Precio accesible",
     "Desde US$ 320 en lanzamiento y con financiamiento: un destino final al alcance de más familias."),
    ("Naturaleza y legado",
     "Jardines de plantas de sombra, agua corriente y bosque: un homenaje que vive."),
    ("Sin decisiones bajo presión",
     "Planificar hoy evita que la familia decida en el peor momento."),
]

MODOS_DE_VENTA = [
    ("Prenecesidad (preventiva)",
     "Venta planificada, de ciclo largo. La familia contrata hoy para protegerse "
     "y pagar en cuotas. Es la venta que conducimos activamente."),
    ("Necesidad inmediata (emergencia)",
     "En el momento de la pérdida. Aquí no se \"vende\": se acoge, se informa con "
     "calma y se resuelve con agilidad y respeto."),
]

REGLA_DE_ORO = (
    "Nuestra diferencia no es el precio: es la atención. Antes de cada propuesta, "
    "pregúntese: \"¿esto acoge a la familia o solo cierra un negocio?\"."
)

# ---------------------------------------------------------------------------
# 02 · ICP
# ---------------------------------------------------------------------------
PERFILES = [
    ("El Planificador", "45–65 años, compra para sí mismo.",
     "Tranquilidad y legado. No quiere dejar cargas a su familia.",
     "Calma, sin prisa, datos claros.",
     "Solución Modular · Jardín Individual · Jardín Familiar"),
    ("El Hijo Cuidador", "25–45 años, compra para sus padres.",
     "Practicidad, control del presupuesto, evitar improvisar.",
     "Claro, práctico, comparativo.",
     "Solución Modular · Jardín Familiar"),
    ("La Familia en Urgencia", "En el momento de la pérdida.",
     "Quitar peso, dignidad, agilidad.",
     "Acogida total, nunca comercial.",
     "Jardín Individual · Jardín Ecológico"),
    ("El Consciente Ecológico", "30–55 años, valora la naturaleza.",
     "Volver a la tierra, sencillez, sostenibilidad.",
     "Inspirador, natural, sin solemnidad excesiva.",
     "Jardín Ecológico"),
    ("El Tutor de Mascota", "20–60 años, despide a su compañero.",
     "Respeto al vínculo, un lugar para recordar.",
     "Emocional, cálido y ligero.",
     "Jardín de Mascotas"),
]

FILTRO_CALIFICACION = (
    "Antes de invertir energía en un contacto, evalúe tres puntos: Necesidad "
    "(¿lo necesita?), Oportunidad (¿es el momento y tiene capacidad de pago?) y "
    "Adecuación (¿qué producto encaja con su perfil?). Calificar bien en la entrada "
    "evita morosidad en el cobro."
)

# ---------------------------------------------------------------------------
# 03 · Proceso
# ---------------------------------------------------------------------------
EMBUDO = [
    ("Contacto", "Llega por referido, evento, base de datos o visita. Se registra al instante."),
    ("Calificación", "Necesidad, oportunidad y adecuación. Primer contacto en menos de 1 hora."),
    ("Descubrimiento", "Escuchar a la familia: creencias, presupuesto, quién decide."),
    ("Propuesta", "Producto correcto para el perfil, con precio y cuotas claros."),
    ("Visita al jardín", "Siempre que sea posible: el jardín vende solo."),
    ("Cierre", "Contrato firmado, primera cuota y registro completo."),
    ("Posventa", "Bienvenida, recordatorios de mantenimiento, base para referidos."),
]

EQUIPOS = [
    ("UAF · Unidad de Apoyo Familiar",
     "Acompaña a la familia durante el servicio y trabaja referidos.",
     "Jardín Individual y Ecológico como destino de las cenizas; Solución Modular "
     "para el resto de la familia (venta de prenecesidad posterior)."),
    ("Pilares Alternativos",
     "Eventos, centros comerciales, bases de cancelaciones y telemercadeo.",
     "Solución Modular (cuota baja, fácil de explicar) y Jardín de Mascotas."),
    ("AML · Puerta a puerta",
     "Prospección sistemática en colonias.",
     "Solución Modular + Jardín Individual: la combinación más completa para el hogar."),
]

RITUALES = [
    ("Diario", "Alineación rápida de 10 minutos: pendientes y bloqueos."),
    ("Semanal", "Revisión del embudo: dónde se están quedando los contactos."),
    ("Mensual", "Resultado vs. meta, ajuste de ruta y reconocimiento."),
]

CONVERSACION = [
    ("Acoger", "Conectar antes de vender. ¿Quién es y qué lo trajo?"),
    ("Descubrir", "Más preguntas que afirmaciones. La solución nace de la escucha."),
    ("Presentar valor", "Hablar de tranquilidad, cuidado y memoria, no de \"producto\"."),
    ("Resolver dudas", "Validar la emoción, reposicionar, nunca discutir."),
    ("Avanzar", "Un siguiente paso claro y amable: visita, propuesta o firma."),
]

# ---------------------------------------------------------------------------
# 04 · Productos
# ---------------------------------------------------------------------------
PRODUCTOS = [
    {
        "nombre": "Solución Modular de Cremación",
        "corto": "Solución Modular",
        "etiqueta": "Cremación · Add-on",
        "precio": "US$ 1.000",
        "pago": "Lanzamiento (−20%): US$ 800 · Pago en hasta 120 meses, con intereses",
        "que_es": (
            "Módulo de cremación que se integra a cualquier plan funerario vigente o "
            "nuevo de Vangrupo, sin cambiar de plan."
        ),
        "incluye": [
            "Proceso completo de cremación individual",
            "Urna cineraria de línea modular",
            "Trámites legales básicos",
            "Alquiler temporal de columbario por 1 año en Hogar de las Memorias",
        ],
        "reglas": [
            "Se vende como adicional a un plan funerario (actual o nuevo).",
            "Cobertura individual: un módulo por titular o beneficiario.",
            "Debe estar pagado en su totalidad para usar la cremación y el columbario.",
            "El columbario temporal es por 12 meses; al término, la familia elige "
            "destino final (oportunidad para ofrecer un Jardín de Cenizas o un columbario).",
        ],
        "para_quien": "Afiliados actuales y nuevos que quieren sumar la cremación con una cuota mínima.",
        "speech": (
            "\"Usted ya protegió a su familia con su plan. Pagando en hasta 120 meses, "
            "puede sumar la cremación completa, con urna, trámites y un año de columbario incluido. Así "
            "nadie tendrá que decidir ni pagar de golpe en un momento difícil.\""
        ),
        "preguntas": [
            "¿Su plan actual incluye la cremación o solo el servicio funerario?",
            "¿Ha conversado en familia qué preferencia tiene usted?",
            "¿Qué le preocupa más: el costo o tener que decidir de urgencia?",
        ],
        "cierre": "\"¿Le parece si lo sumamos a su plan desde este mes, con la primera cuota de hoy?\"",
        "objecion": (
            "\"Mi plan ya es suficiente.\" → \"Su plan cubre el servicio funerario; la "
            "cremación y la urna se pagarían aparte y de una sola vez. Con el módulo "
            "queda todo cubierto en cuotas pequeñas.\""
        ),
        "tip": "Ofrézcalo siempre junto a un jardín: la familia resuelve cremación y destino final en una sola decisión.",
    },
    {
        "nombre": "Jardín de Cenizas · Individual",
        "corto": "Jardín Individual",
        "etiqueta": "Jardín 1 · Inhumación individual",
        "precio": "US$ 600",
        "pago": "Lanzamiento (−20%): US$ 480 · Pago único o financiado · Mantenimiento US$ 15/año",
        "que_es": (
            "Inhumación de la urna en un contenedor enterrado con tapa de granito "
            "grabada, en un jardín de plantas de sombra: un lugar para visitar por 30 años desde la primera inhumación, renovable."
        ),
        "incluye": [
            "Inhumación de la urna en contenedor individual (Ø 32 × 40 cm)",
            "Tapa de granito con los datos del ser querido",
            "Ubicación en el Jardín 1, con paisajismo de plantas de sombra",
            "Camino en gravilla y espacio de contemplación con banco",
        ],
        "reglas": [
            "Capacidad: 1 urna.",
            "Cuota de mantenimiento anual: US$ 15. Permanencia: 30 años desde la primera inhumación, renovable.",
            "El contenedor queda con 20 cm a la vista; la tapa de granito es la identificación.",
        ],
        "para_quien": "Familias que quieren un lugar propio para visitar, con una inversión moderada.",
        "speech": (
            "\"Después de la cremación, muchas familias se preguntan dónde dejar las "
            "cenizas. En nuestro Jardín 1, su ser querido descansa bajo una tapa de granito "
            "con su nombre, rodeado de plantas y con un banco para sentarse a recordar. "
            "Es un lugar para volver, con la dignidad que merece.\""
        ),
        "preguntas": [
            "¿Dónde le gustaría poder visitar a su ser querido?",
            "¿Tienen hoy las cenizas en casa o en un columbario temporal?",
            "¿Quién más de la familia participaría en las visitas?",
        ],
        "cierre": "\"¿Le gustaría conocer el jardín esta semana para elegir el lugar con calma?\"",
        "objecion": (
            "\"Prefiero tener las cenizas en casa.\" → \"Es comprensible querer tenerlas cerca. "
            "En el jardín, toda la familia puede visitarlas, y las cenizas quedan protegidas "
            "si algún día hay mudanzas o cambios en el hogar.\""
        ),
        "tip": "El jardín vende solo: priorice siempre la visita.",
    },
    {
        "nombre": "Jardín de Cenizas · Familiar",
        "corto": "Jardín Familiar",
        "etiqueta": "Jardín 1 · Parcela familiar",
        "precio": "US$ 2.000",
        "pago": "Lanzamiento (−20%): US$ 1.600 · Pago único o financiado · Mantenimiento US$ 24/año",
        "que_es": (
            "Parcela familiar en el Jardín 1 con cuatro contenedores agrupados, cada uno "
            "con tapa de granito grabada. Permanencia de 30 años desde la primera inhumación, renovable."
        ),
        "incluye": [
            "Inhumación de hasta 4 urnas",
            "Tapa de granito grabada para cada espacio",
            "Ubicación en el Jardín 1, con paisajismo de plantas de sombra",
            "Lugar de homenaje familiar por 30 años, renovable por igual período",
        ],
        "reglas": [
            "Capacidad: hasta 4 espacios.",
            "Permanencia: 30 años desde la primera inhumación, renovable por igual período.",
            "Cuota de mantenimiento anual: US$ 24 por parcela.",
        ],
        "para_quien": "Familias que buscan un espacio propio para varias generaciones.",
        "speech": (
            "\"Así como una familia comparte una casa, también puede compartir un lugar de "
            "memoria. La parcela familiar reúne hasta cuatro seres queridos en un mismo "
            "espacio, por 30 años renovables, y cuesta US$ 500 por espacio (US$ 400 con el precio de lanzamiento), menos que comprarlos por separado.\""
        ),
        "preguntas": [
            "¿Les gustaría que la familia esté reunida en un mismo lugar?",
            "¿Cuántas personas de la familia considerarían este destino?",
            "¿Prefieren pagarlo de una vez o en cuotas?",
        ],
        "cierre": "\"¿Reservamos hoy la parcela para su familia y la pagan en cuotas cómodas?\"",
        "objecion": (
            "\"Es mucho dinero.\" → \"Son US$ 500 por cada espacio, con financiamiento. Y es "
            "una decisión que se toma una sola vez para toda la familia.\""
        ),
        "tip": "Use el argumento por espacio (US$ 500) y no el total.",
    },
    {
        "nombre": "Jardín de Cenizas · Ecológico",
        "corto": "Jardín Ecológico",
        "etiqueta": "Jardín 2 · Bosque de las Orquídeas",
        "precio": "US$ 750",
        "pago": "Lanzamiento (−20%): US$ 600 · Pago único o financiado · Placa memorial incluida",
        "que_es": (
            "La urna biodegradable se entierra directamente en el suelo y se integra a la "
            "naturaleza. Jardín con agua corriente, en el Jardín 2 o en el Bosque de las "
            "Orquídeas."
        ),
        "incluye": [
            "Inhumación ecológica con urna biodegradable",
            "Placa de identificación (madera en el Jardín 2 · mármol en el Bosque)",
            "Entorno natural con agua corriente",
            "Permanencia de 3 años; luego, nombre en la placa memorial del monumento (incluida)",
        ],
        "reglas": [
            "Capacidad: 1 urna. Espacio de 30 × 30 cm, 40 cm de profundidad.",
            "Permanencia: 3 años. Después, el espacio se reutiliza.",
            "Placa memorial en el monumento: incluida en el precio de US$ 750.",
            "Explique el plazo de 3 años con total transparencia desde la primera conversación.",
        ],
        "para_quien": "Personas con conciencia ambiental que desean que sus cenizas vuelvan a la tierra.",
        "speech": (
            "\"Para quienes aman la naturaleza, el Jardín Ecológico es volver a la tierra. "
            "La urna se integra al suelo del bosque, junto al agua, y durante tres años la "
            "familia tiene un lugar señalado para visitar. Después, el nombre queda para "
            "siempre en el monumento memorial del jardín.\""
        ),
        "preguntas": [
            "¿Su ser querido tenía un vínculo especial con la naturaleza?",
            "¿Qué significa para ustedes \"volver a la tierra\"?",
            "¿Es importante para la familia un lugar con nombre para siempre?",
        ],
        "cierre": "\"¿Le parece si visitamos el Bosque de las Orquídeas y elegimos juntos el lugar?\"",
        "objecion": (
            "\"¿Y después de 3 años?\" → \"La urna ya se habrá integrado a la tierra, como era "
            "el deseo. El nombre pasa a la placa memorial del monumento, que queda para "
            "siempre en el jardín.\""
        ),
        "tip": "Para familias católicas, enfatice que las cenizas reposan en el cementerio, un lugar dedicado a la memoria.",
    },
    {
        "nombre": "Jardín de Mascotas",
        "corto": "Jardín de Mascotas",
        "etiqueta": "Mascotas · Inhumación ecológica",
        "precio": "US$ 400 / US$ 550",
        "pago": "Lanzamiento (−20%): US$ 320 / US$ 440 · US$ 400 solo espacio · US$ 550 con cremación",
        "que_es": (
            "Inhumación ecológica de las cenizas de la mascota: la urna biodegradable se entierra en el jardín y se identifica con una placa de madera. La opción de US$ 550 incluye también la cremación de la mascota."
        ),
        "incluye": [
            "Inhumación ecológica en el jardín de mascotas; cremación y urna biodegradable en la opción de US$ 550",
            "Placa de madera de 20 cm para identificación",
            "Permanencia de 3 años",
            "Placa memorial en el monumento al término del plazo (incluida)",
        ],
        "reglas": [
            "Capacidad: 1 mascota por servicio.",
            "Permanencia: 3 años. Después, el espacio se reutiliza.",
            "Placa memorial incluida. Urna biodegradable incluida solo con cremación (US$ 550); con solo espacio (US$ 400) se compra aparte.",
            "Pago único; puede contratarse como adicional al plan funerario.",
        ],
        "para_quien": "Familias que consideran a su mascota parte del hogar y desean un cierre digno.",
        "speech": (
            "\"Su compañero fue parte de la familia, y merece una despedida a la altura. En "
            "nuestro Jardín de Mascotas descansa con su nombre, en un lugar verde donde "
            "ustedes pueden volver a recordarlo. Y con la placa memorial, su nombre "
            "queda para siempre en el monumento del jardín.\""
        ),
        "preguntas": [
            "¿Cómo se llamaba su compañero?",
            "¿Ya se realizó la cremación o necesitan también ese servicio?",
            "¿Les gustaría un lugar para visitarlo con los niños?",
        ],
        "cierre": "\"¿Prefieren la opción con cremación incluida, para resolver todo en un solo paso?\"",
        "objecion": (
            "\"Es solo una mascota.\" → No discuta el vínculo de la familia. Si el cliente "
            "minimiza, respete y ofrezca la información por escrito para que decida con calma."
        ),
        "tip": "Llame a la mascota por su nombre durante toda la conversación.",
    },
    {
        "nombre": "Jardín de Cenizas · Ceremonial",
        "corto": "Jardín Ceremonial",
        "etiqueta": "Jardín 3 · Próximo lanzamiento",
        "precio": "A definir",
        "pago": "A definir",
        "que_es": (
            "Jardín para inhumación de urnas con ceremonia de agua, con fuentes como "
            "elemento central del rito de despedida."
        ),
        "incluye": [
            "Inhumación de urnas de cenizas",
            "Ceremonia con agua en fuente",
            "Barrera visual que separa el jardín del crematorio",
        ],
        "reglas": [
            "PRÓXIMO LANZAMIENTO: no se vende ni se cotiza todavía.",
            "Si un cliente muestra interés, registre su contacto como \"interesado Ceremonial\".",
        ],
        "para_quien": "Familias que valoran un rito de despedida simbólico y un entorno contemplativo.",
        "speech": (
            "\"Estamos preparando un nuevo jardín con una ceremonia de agua muy especial. "
            "Si le interesa, con gusto le aviso apenas esté disponible.\""
        ),
        "preguntas": ["¿Le gustaría que le avisemos cuando esté disponible?"],
        "cierre": "Registrar el interés y ofrecer, mientras tanto, el Jardín Individual o el Ecológico.",
        "objecion": "No aplica todavía.",
        "tip": "No prometa fechas ni precios.",
        "proximo": True,
    },
]

# Portafolio existente de columbarios (productos ya en venta; −15% en Finados y noviembre).
# Fuente: Columbarios - Cremaciones (Drive Vangrupo).
INTRO_EXISTENTES = (
    "Además de los lanzamientos, el portafolio de cremación incluye los columbarios que ya "
    "vendemos en El Hogar de las Memorias y en el mausoleo vertical Bella Vista. En Finados y "
    "durante noviembre tienen 15% de descuento. Se pagan al contado o financiados en hasta "
    "120 meses, con intereses."
)

UBICACION_DEFINIDA_FUTURO = (
    "Ubicación definida: el nicho se elige al contratar. Ubicación a futuro: se compra hoy y "
    "el nicho se asigna más adelante. El precio varía según la fila y el nivel."
)

PRODUCTOS_EXISTENTES = [
    {
        "nombre": "Columbario Supremo Plus",
        "corto": "Supremo Plus",
        "etiqueta": "Hogar de las Memorias · Servicio completo",
        "etiqueta_precio": "PRECIO SEGÚN UBICACIÓN",
        "precio": "US$ 2.700 – 3.900",
        "pago": "Finados y noviembre (−15%): desde US$ 2.295 · Pago único o hasta 120 meses, con intereses",
        "que_es": (
            "Integra en un solo contrato el servicio funerario, dos cremaciones y un columbario "
            "permanente de cristal o mármol para hasta dos urnas, en El Hogar de las Memorias."
        ),
        "incluye": [
            "Incluye columbario estándar permanente de cristal o mármol, para hasta 2 urnas",
            "Traslados, preparación y resguardo hasta 5 días; Programa Vive de acompañamiento en el duelo",
            "Urnas cinerarias básicas (2) y 2 cremaciones con certificado",
            "Capilla de velación 24 h, ataúd ceremonial y carroza tradicional",
        ],
        "reglas": [
            "Capacidad: hasta 2 urnas; incluye 2 cremaciones.",
            "Con ubicación definida: US$ 3.400 – 3.900; a futuro: US$ 2.700 – 3.200 (según fila y nivel).",
            "Elija velación en La Auxiliadora (Maquilishuat o Básica) o en Capillas Memoriales (Las Camelias o Básica).",
        ],
        "para_quien": "Familias que quieren resolver en una sola compra el funeral, la cremación y un lugar permanente para dos seres queridos.",
        "speech": (
            "\"Con el Supremo Plus su familia no tendrá que coordinar nada: el servicio funerario, "
            "la cremación y el lugar donde descansarán las cenizas quedan resueltos en un solo "
            "contrato, para dos personas y para siempre.\""
        ),
        "preguntas": [
            "¿Han pensado dónde quedarían las cenizas después de la cremación?",
            "¿Lo considera para usted y su pareja, o para sus padres?",
            "¿Prefiere elegir hoy el nicho o dejar la ubicación para más adelante?",
        ],
        "cierre": "\"¿Aprovechamos el precio de noviembre y elegimos hoy la ubicación?\"",
        "objecion": (
            "\"Es una inversión alta.\" → \"Incluye todo para dos personas: funeral, dos cremaciones "
            "y el columbario permanente. Y puede pagarse en hasta 120 meses.\""
        ),
        "tip": "Si el presupuesto no alcanza para la ubicación definida, ofrezca la ubicación a futuro: el mismo producto, a menor precio.",
    },
    {
        "nombre": "Columbario Mármol o Cristal",
        "corto": "Mármol o Cristal",
        "etiqueta": "Hogar de las Memorias · Columbario",
        "etiqueta_precio": "PRECIO SEGÚN UBICACIÓN",
        "precio": "US$ 1.200 – 2.600",
        "pago": "Finados y noviembre (−15%): desde US$ 1.020 · Pago único o hasta 120 meses, con intereses",
        "que_es": (
            "Ideal para las cenizas de la familia: columbario permanente de mármol o cristal en "
            "El Hogar de las Memorias, elegante, sereno y de diseño atemporal."
        ),
        "incluye": [
            "Incluye espacio permanente en columbario de mármol o cristal",
            "Tamaño estándar: hasta 2 urnas",
            "Ubicación definida o a futuro, según la opción contratada",
        ],
        "reglas": [
            "Cremación no incluida: se contrata aparte (por ejemplo, con la Solución Modular).",
            "Con ubicación definida: US$ 2.600; a futuro: US$ 1.200 – 1.900 (según fila y nivel).",
        ],
        "para_quien": "Familias que ya tienen la cremación resuelta y buscan un lugar permanente y elegante para las cenizas.",
        "speech": (
            "\"Las cenizas de su ser querido merecen un lugar propio y permanente. En El Hogar de "
            "las Memorias, el columbario de mármol o cristal guarda hasta dos urnas en un espacio "
            "sereno, donde la familia siempre podrá volver.\""
        ),
        "preguntas": [
            "¿Las cenizas están hoy en casa o en un columbario temporal?",
            "¿Prefieren el mármol o el cristal?",
            "¿Pensarían en un espacio para dos personas de la familia?",
        ],
        "cierre": "\"¿Visitamos El Hogar de las Memorias para que elija la fila y el nivel?\"",
        "objecion": (
            "\"Ya tengo las cenizas en casa.\" → \"Es natural tenerlas cerca. En el columbario quedan "
            "protegidas para siempre y toda la familia puede visitarlas.\""
        ),
        "tip": "Es el destino natural al terminar los 12 meses de columbario temporal de la Solución Modular.",
    },
    {
        "nombre": "Columbario Ónix",
        "corto": "Columbario Ónix",
        "etiqueta": "Hogar de las Memorias · Columbario premium",
        "etiqueta_precio": "PRECIO SEGÚN MODALIDAD",
        "precio": "US$ 3.100 / 5.000",
        "pago": "Finados y noviembre (−15%): US$ 2.635 / 4.250 · Único o hasta 120 meses, con intereses",
        "que_es": (
            "Inspirado en la belleza del ónix natural, de tonos cálidos y apariencia luminosa: un "
            "columbario exclusivo para un homenaje perdurable."
        ),
        "incluye": [
            "Incluye espacio permanente en columbario de ónix natural",
            "Tamaño estándar: hasta 2 urnas, con ubicación definida (US$ 3.100)",
            "Una opción familiar: hasta 4 urnas, con ubicación a futuro (US$ 5.000)",
        ],
        "reglas": [
            "Cremación no incluida: se contrata aparte.",
            "Con la modalidad estándar la ubicación es definida; con la familiar, a futuro.",
        ],
        "para_quien": "Familias que buscan exclusividad y una piedra natural de alta gama para el homenaje.",
        "speech": (
            "\"El ónix es una piedra natural única: su luz y sus tonos cálidos hacen de cada espacio "
            "un lugar de paz. Es un homenaje distinto, a la altura de quien usted ama.\""
        ),
        "preguntas": [
            "¿Qué tipo de homenaje imagina para su familia?",
            "¿Sería para dos personas o para la familia completa?",
        ],
        "cierre": "\"¿Le muestro el columbario de ónix para que vea la piedra en persona?\"",
        "objecion": (
            "\"Hay opciones más baratas.\" → \"Sí, y con gusto se las muestro. El ónix es para quien "
            "busca algo único: una piedra natural que no se repite.\""
        ),
        "tip": "Muestre la piedra en persona: la luz del ónix se aprecia mejor que en cualquier foto.",
    },
    {
        "nombre": "Columbario Obra de Arte",
        "corto": "Obra de Arte",
        "etiqueta": "Hogar de las Memorias · Columbario familiar",
        "etiqueta_precio": "PRECIO",
        "precio": "US$ 12.500",
        "pago": "Finados y noviembre (−15%): US$ 10.625 · Pago único o hasta 120 meses, con intereses",
        "que_es": (
            "Imagen religiosa sobre tapa de ónix: un columbario familiar que es una expresión "
            "única de fe, memoria y belleza."
        ),
        "incluye": [
            "Incluye columbario familiar permanente para hasta 4 urnas",
            "Tapa exclusiva de ónix con obra de arte religiosa",
            "Ubicación definida",
        ],
        "reglas": [
            "Capacidad: hasta 4 urnas (familiar).",
            "Cremación no incluida: se contrata aparte.",
        ],
        "para_quien": "Familias de fe que desean un legado único y de máxima exclusividad.",
        "speech": (
            "\"Este columbario es una obra de arte de fe: la tapa de ónix con imagen religiosa "
            "convierte el lugar de descanso de su familia en un espacio de oración y "
            "contemplación, para generaciones.\""
        ),
        "preguntas": [
            "¿Qué lugar tiene la fe en la forma en que su familia recuerda?",
            "¿Cuántos miembros de la familia lo considerarían?",
        ],
        "cierre": "\"¿Reservamos hoy el espacio familiar con el precio de noviembre?\"",
        "objecion": (
            "\"Es muy caro.\" → \"Es un legado para cuatro personas, para siempre, y puede pagarse en "
            "hasta 120 meses. Es la opción más exclusiva del portafolio.\""
        ),
        "tip": "Preséntelo con calma y en persona; no lo ofrezca a quien busca la opción más económica.",
    },
    {
        "nombre": "Columbario Cristal · Bella Vista",
        "corto": "Bella Vista",
        "etiqueta": "Mausoleo Bella Vista · Cremación + columbario",
        "etiqueta_precio": "PRECIO SEGÚN UBICACIÓN",
        "precio": "US$ 1.300 – 2.900",
        "pago": "Finados y noviembre (−15%): desde US$ 1.105 · Pago único o hasta 120 meses, con intereses",
        "que_es": (
            "Incluye el proceso completo de cremación y un columbario de cristal en el mausoleo "
            "vertical Bella Vista, dentro del cementerio."
        ),
        "incluye": [
            "Incluye columbario de cristal permanente (30 × 30 × 30 cm)",
            "Traslados, preparación y resguardo hasta 5 días",
            "Urnas y cremaciones: 2 en la modalidad estándar, 4 en la familiar",
            "Certificado de cremación y ceremonia privada de colocación",
        ],
        "reglas": [
            "Con modalidad estándar: definida US$ 1.800 · a futuro US$ 1.300.",
            "Con modalidad familiar: definida US$ 2.900 · a futuro US$ 2.300.",
            "En este producto la cremación está incluida: no hace falta contratarla aparte.",
        ],
        "para_quien": "Familias que buscan la opción más accesible de cremación con columbario permanente, para 2 o 4 personas.",
        "speech": (
            "\"Bella Vista resuelve en un solo paso la cremación y el lugar de descanso: un "
            "columbario de cristal en nuestro mausoleo vertical, para dos o cuatro personas, con "
            "todo el proceso incluido.\""
        ),
        "preguntas": [
            "¿Lo considera para dos personas o para la familia?",
            "¿Prefieren elegir ya la ubicación o dejarla a futuro?",
        ],
        "cierre": "\"¿Aprovechamos el precio de noviembre y lo dejamos resuelto hoy?\"",
        "objecion": (
            "\"Prefiero un jardín.\" → \"Perfecto, también tenemos los Jardines de Cenizas. Bella Vista "
            "es para quien prefiere un columbario, con la cremación ya incluida.\""
        ),
        "tip": "Es la puerta de entrada a los columbarios: cremación y destino final desde US$ 1.105 en noviembre.",
    },
]

# ---------------------------------------------------------------------------
# 05 · Objeciones
# ---------------------------------------------------------------------------
METODO_OBJECIONES = [
    ("Validar", "Reconocer la emoción: \"Entiendo, es una decisión importante.\""),
    ("Reposicionar", "Mostrar el valor desde otro ángulo, sin discutir."),
    ("Avanzar", "Proponer un siguiente paso concreto y amable."),
]

OBJECIONES = [
    ("\"No quiero pensar en eso, es de mala suerte.\"",
     "Entiendo, a nadie le gusta hablar de este tema.",
     "Planificar con calma es justamente lo que evita que su familia tenga que decidir "
     "en el peor momento. Es un acto de cuidado, no de pesimismo.",
     "¿Le dejo la información para que la conversen en casa?"),
    ("\"Soy católico, la cremación no está permitida.\"",
     "Su fe es muy importante y la respetamos.",
     "La Iglesia Católica permite la cremación desde 1963. Lo que pide es que las cenizas "
     "reposen en un lugar dedicado, como el cementerio, y no en casa ni dispersas. "
     "Nuestros jardines cumplen exactamente con eso.",
     "¿Le gustaría conocer el jardín y ver cómo es el lugar?"),
    ("\"Prefiero la sepultura tradicional.\"",
     "Es una tradición muy valiosa.",
     "El jardín conserva lo esencial de la sepultura: un lugar con nombre para visitar, "
     "con un costo mucho menor y en un entorno natural.",
     "¿Le muestro la diferencia de inversión entre ambas opciones?"),
    ("\"Está caro.\"",
     "Comprendo, es una inversión.",
     "En la urgencia los costos son mayores y se pagan de golpe. Hoy fija el precio y lo "
     "paga en cuotas: la Solución Modular se paga en hasta 120 meses.",
     "¿Le resulta más cómodo pagarlo en cuotas mensuales?"),
    ("\"Tengo que hablarlo con mi familia.\"",
     "Claro, es una decisión de familia.",
     "Facilite esa conversación: ofrezca un resumen simple y quedar disponible para "
     "resolver dudas de todos juntos.",
     "¿Puedo llamarle el [día] para ver si quedó alguna pregunta?"),
    ("\"Prefiero tener las cenizas en casa.\"",
     "Es natural querer tenerlas cerca.",
     "En el jardín toda la familia puede visitarlas, quedan protegidas ante mudanzas o "
     "cambios, y tienen un lugar con su nombre.",
     "¿Le gustaría visitar el jardín antes de decidir?"),
    ("\"¿Por qué pagar mantenimiento cada año?\"",
     "Es una pregunta muy válida.",
     "La cuota (US$ 15 o US$ 24 al año) mantiene el jardín siempre cuidado: poda, riego "
     "y limpieza. Es lo que garantiza que el lugar luzca digno en cada visita.",
     "¿Le explico qué incluye el cuidado del jardín?"),
    ("\"No confío en estos planes.\"",
     "Es una preocupación válida.",
     "Somos La Auxiliadora, Hogar de las Memorias y Las Colinas, empresas de Vangrupo con trayectoria "
     "en El Salvador. El contrato es transparente y puede visitar el jardín cuando quiera.",
     "¿Agendamos una visita sin compromiso?"),
]

PRINCIPIO_OBJECIONES = (
    "Detrás de cada objeción hay una emoción: miedo, duelo o desconfianza. Valide "
    "primero la emoción y después responda. Nunca rebata: reposicione."
)

# ---------------------------------------------------------------------------
# 06 · Precios y reglas
# ---------------------------------------------------------------------------
TABLA_PRECIOS = [
    ("Solución Modular", "US$ 1.000 · lanz. US$ 800", "Hasta 120 meses, con intereses", "—", "Columbario 1 año incluido"),
    ("Jardín Individual", "US$ 600 · lanz. US$ 480", "Único o financiado", "US$ 15/año", "30 años, renovable"),
    ("Jardín Familiar", "US$ 2.000 · lanz. US$ 1.600", "Único o financiado", "US$ 24/año", "Hasta 4 espacios · 30 años, renovable"),
    ("Jardín Ecológico", "US$ 750 · lanz. US$ 600", "Único o financiado", "—", "3 años · placa memorial incluida"),
    ("Jardín de Mascotas", "US$ 400 / 550 · lanz. US$ 320 / 440", "Pago único", "—", "3 años · placa incluida · cremación y urna en la opción de US$ 550"),
    ("Jardín Ceremonial", "A definir", "A definir", "A definir", "Próximo lanzamiento"),
]

TABLA_PRECIOS_EXISTENTES = [  # Producto, precio, Finados y noviembre (−15%), capacidad, incluye
    ("Supremo Plus", "Definida US$ 3.400–3.900 · Futuro US$ 2.700–3.200", "US$ 2.890–3.315 · US$ 2.295–2.720", "2 urnas", "Funeral + 2 cremaciones + columbario"),
    ("Mármol o Cristal", "Definida US$ 2.600 · Futuro US$ 1.200–1.900", "US$ 2.210 · US$ 1.020–1.615", "2 urnas", "Solo columbario"),
    ("Columbario Ónix", "Estándar US$ 3.100 · Familiar US$ 5.000", "US$ 2.635 · US$ 4.250", "2 o 4 urnas", "Solo columbario"),
    ("Obra de Arte", "Familiar US$ 12.500", "US$ 10.625", "4 urnas", "Solo columbario"),
    ("Bella Vista", "Estándar US$ 1.800 / 1.300 · Familiar US$ 2.900 / 2.300", "US$ 1.530 / 1.105 · US$ 2.465 / 1.955", "2 o 4 urnas", "Cremación + columbario"),
]

NOTA_EXISTENTES = (
    "Precios según fila y nivel (Bella Vista: definida / a futuro). Pago único o financiado en hasta "
    "120 meses, con intereses. El 15% vale solo en Finados y durante noviembre."
)

REGLAS_COMERCIALES = [
    ("Precios", "Precios sugeridos en US$ con IVA incluido. Consulte siempre la Ficha Técnica vigente."),
    ("Descuentos", "Productos de lanzamiento (ver Ficha Técnica): 20%. Portafolio existente de columbarios: 15%. Ambos descuentos valen solo en Finados y durante noviembre. Cualquier otro descuento, solo con autorización del supervisor (emergencia: máximo 5%)."),
    ("Mantenimiento", "Individual US$ 15/año y Familiar US$ 24/año. No es opcional: se explica antes de firmar."),
    ("Plazos", "Individual y Familiar: 30 años desde la primera inhumación, renovables. Ecológico y Mascotas: 3 años. Se explica con total transparencia en la primera conversación."),
    ("Placas memoriales", "Incluida en el Jardín Ecológico y en el Jardín de Mascotas."),
    ("Dueño del contacto", "Quien registra primero. Sin interacción en 15 días, el contacto puede reasignarse."),
    ("Lo que NO se promete", "Fechas o precios del Jardín Ceremonial; descuentos fuera de política; "
                             "ubicaciones específicas sin confirmar disponibilidad."),
]

DESCUENTO_NO_ES_SALIDA = (
    "Competimos por valor, no por precio. Antes de ofrecer un descuento, refuerce lo que "
    "está incluido y la calidad del jardín. Un descuento fácil enseña al cliente a dudar del valor."
)

# ---------------------------------------------------------------------------
# 07 · Política de comisiones de los productos de cremación: % según cantidad de ventas del mes
# ---------------------------------------------------------------------------
COMISION_TITULO = "Comisión por cantidad de ventas: 8% · 10% · 12%"
COMISION_RESUMEN = (
    "Vigente en 2026 para todos los productos de cremación. El porcentaje depende de cuántas ventas de "
    "cremación cierra el asesor en el mes (cualquier producto: Solución Modular, jardines o "
    "columbarios) y se aplica sobre toda la facturación del mes, sin IVA."
)

# (ventas en el mes, %, facturación de ejemplo con Solución Modular, comisión del ejemplo)
ESCALA_COMISION = [
    ("1 venta", "8%", "US$ 885", "US$ 70,80"),
    ("2 ventas", "10%", "US$ 1.770", "US$ 177,00"),
    ("3 ventas o más", "12%", "US$ 2.655", "US$ 318,60"),
]

COMISIONES_VALORES = [  # para la figura: comisión del mes con N Soluciones Modulares (US$ 885 sin IVA c/u)
    ("1 venta · 8%", 70.80), ("2 ventas · 10%", 177.00), ("3 ventas · 12%", 318.60),
]

# (producto, cuándo se paga, estorno)
COMISIONES = [
    ("Solución Modular", "Pago único al pagar el cliente la 3ª cuota", "Si cancela antes de la 12ª cuota"),
    ("Jardines de Cenizas", "Contado: mes siguiente · Financiado: proporcional a lo cobrado", "Cancelación en 90 días"),
    ("Jardín de Mascotas", "Mes siguiente al pago", "Cancelación en 90 días"),
    ("Columbarios (portafolio existente)", "Contado: mes siguiente · Financiado: proporcional a lo cobrado", "Cancelación en 90 días"),
]

REGLAS_COMISION = [
    "1 venta en el mes = 8%; 2 ventas = 10%; 3 o más = 12%, sobre toda la facturación del mes.",
    "Cuenta cualquier producto de cremación (nuevos y columbarios): cada contrato es 1 venta.",
    "Base de cálculo: facturación sin IVA (13%), neta de descuentos; se paga sobre lo cobrado.",
    "Mismo criterio para call center, contratados y freelancers. Sin bonos adicionales.",
    "Venta compartida (call center agenda, otro cierra): 1 venta para ambos; comisión 30% / 70%.",
    "No cuentan ni comisionan: cuotas de mantenimiento anual (US$ 15 / US$ 24).",
    "Estorno: la comisión se descuenta de los pagos siguientes al asesor; ventas anuladas no cuentan.",
]

COMISION_CUIDADO = (
    "La comisión premia la venta buena, no solo la venta: una familia que paga a tiempo "
    "vale más que un contrato que se cancela. Por eso el pago está ligado al cobro."
)

# ---------------------------------------------------------------------------
# 08 · Herramientas
# ---------------------------------------------------------------------------
HERRAMIENTAS = [
    ("Ficha Técnica de Cremación", "Precios, especificaciones y condiciones vigentes de cada producto."),
    ("Visita al jardín", "La herramienta de venta más poderosa. Agende siempre que sea posible."),
    ("Presentación \"Jardines de Cenizas\"", "Fotos y medidas de cada jardín para mostrar en la visita o en la casa."),
    ("Plazo de pago", "Comunique que se paga en hasta 120 meses con intereses; no prometa un valor de cuota."),
    ("Registro de contactos", "Un contacto no registrado no existe: sin datos no hay gestión ni comisión."),
]

CHECKLIST_CIERRE = [
    "Expliqué qué incluye el producto y qué no incluye.",
    "Expliqué la cuota de mantenimiento y el plazo (30 años renovables o 3 años), según el caso.",
    "Confirmé el precio y la forma de pago con la Ficha Técnica vigente.",
    "El descuento, si lo hubo, está dentro de la política y autorizado.",
    "El cliente recibió copia del contrato y el contacto de su asesor.",
    "Registré la venta completa el mismo día.",
]

CIERRE_FRASE = (
    "Cada familia que atendemos recordará cómo la tratamos en uno de los momentos más "
    "sensibles de su vida. Ese es nuestro verdadero producto."
)
