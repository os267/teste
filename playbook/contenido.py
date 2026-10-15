"""
Contenido del Playbook Comercial — Portafolio de Cremación y Jardines de Cenizas.
La Auxiliadora · Hogar de las Memorias · Vangrupo.

Fuente única para la versión Google Docs (generar_docx.py) y la versión Canva
(generar_pptx.py). Datos de productos y precios: Ficha Técnica Cremación Vangrupo
(oct/2026) y diseño Canva "Jardines de Cenizas" (Luana Magedanz).
Estructura inspirada en el Playbook de Ventas Alta Loma.
"""

TITULO = "Playbook Comercial"
SUBTITULO = "Portafolio de Cremación y Jardines de Cenizas"
MARCAS = "La Auxiliadora · Hogar de las Memorias · Vangrupo"
CAMPANA = "Campaña Día de los Muertos 2026"
LEMA = "Acompañar, no vender: la familia primero, siempre."
VERSION = "Versión 1.0 · Octubre 2026 · Uso interno del equipo comercial"

COMO_USAR = (
    "Este playbook es la referencia única del equipo comercial para el portafolio "
    "de cremación y jardines de cenizas. Reúne reglas, precios, discurso por producto, "
    "manejo de objeciones y política de comisiones. Se revisa cada trimestre con la "
    "Gerencia Comercial. Si algo cambia en la Ficha Técnica, este documento se actualiza."
)

PENDIENTES = [
    "Política de comisiones: PROPUESTA pendiente de validación con el Gerente Comercial.",
    "Jardín de Mascotas: confirmar si la urna biodegradable está incluida en el precio.",
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
    ("07", "Política de comisiones"),
    ("08", "Herramientas de apoyo"),
]

# ---------------------------------------------------------------------------
# 01 · Quiénes somos
# ---------------------------------------------------------------------------
QUIENES_SOMOS = (
    "En La Auxiliadora y Hogar de las Memorias, empresas de Vangrupo, no vendemos "
    "nichos, parcelas ni servicios: acompañamos a las familias salvadoreñas a honrar "
    "la memoria de quienes aman. La cremación es una decisión cada vez más elegida, y "
    "nuestros nuevos jardines de cenizas responden a una pregunta que muchas familias "
    "se hacen y pocas se atreven a decir: «¿y después de la cremación, dónde las "
    "visitamos?»."
)

POR_QUE_AHORA = [
    ("Un lugar para volver",
     "La familia tiene un sitio físico, digno y verde para visitar y recordar."),
    ("Precio accesible",
     "Desde US$ 350 y con financiamiento: un destino final al alcance de más familias."),
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
     "En el momento de la pérdida. Aquí no se «vende»: se acoge, se informa con "
     "calma y se resuelve con agilidad y respeto."),
]

REGLA_DE_ORO = (
    "Nuestra diferencia no es el precio: es la atención. Antes de cada propuesta, "
    "pregúntese: «¿esto acoge a la familia o solo cierra un negocio?»."
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
    ("Presentar valor", "Hablar de tranquilidad, cuidado y memoria, no de «producto»."),
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
        "pago": "Hasta 120 cuotas mensuales (≈ US$ 8,50/mes)",
        "que_es": (
            "Módulo de cremación que se integra a cualquier plan funerario vigente o "
            "nuevo de Vangrupo, sin cambiar de plan."
        ),
        "incluye": [
            "Proceso completo de cremación individual",
            "Urna cineraria de línea modular",
            "Trámites legales básicos",
            "Alquiler temporal de columbario por 1 año",
        ],
        "reglas": [
            "Se vende como adicional a un plan funerario (actual o nuevo).",
            "Cobertura individual: un módulo por titular o beneficiario.",
            "El columbario temporal es por 12 meses; al término, la familia elige "
            "destino final (oportunidad para ofrecer un Jardín de Cenizas).",
        ],
        "para_quien": "Afiliados actuales y nuevos que quieren sumar la cremación con una cuota mínima.",
        "speech": (
            "«Usted ya protegió a su familia con su plan. Por menos de lo que cuesta un "
            "refresco a la semana, alrededor de ocho dólares al mes, puede sumar la "
            "cremación completa, con urna, trámites y un año de columbario incluido. Así "
            "nadie tendrá que decidir ni pagar de golpe en un momento difícil.»"
        ),
        "preguntas": [
            "¿Su plan actual incluye la cremación o solo el servicio funerario?",
            "¿Ha conversado en familia qué preferencia tiene usted?",
            "¿Qué le preocupa más: el costo o tener que decidir de urgencia?",
        ],
        "cierre": "«¿Le parece si lo sumamos a su plan desde este mes, con la primera cuota de hoy?»",
        "objecion": (
            "«Mi plan ya es suficiente.» → «Su plan cubre el servicio funerario; la "
            "cremación y la urna se pagarían aparte y de una sola vez. Con el módulo "
            "queda todo cubierto en cuotas pequeñas.»"
        ),
        "tip": "Ofrézcalo siempre junto a un jardín: la familia resuelve cremación y destino final en una sola decisión.",
    },
    {
        "nombre": "Jardín de Cenizas · Individual",
        "corto": "Jardín Individual",
        "etiqueta": "Jardín 1 · Inhumación individual",
        "precio": "US$ 600",
        "pago": "Pago único o financiado · Mantenimiento US$ 15/año",
        "que_es": (
            "Inhumación de la urna en un contenedor enterrado con tapa de granito "
            "grabada, en un jardín de plantas de sombra: un lugar permanente para visitar."
        ),
        "incluye": [
            "Inhumación de la urna en contenedor individual (Ø 32 × 40 cm)",
            "Tapa de granito con los datos del ser querido",
            "Ubicación en el Jardín 1, con paisajismo de plantas de sombra",
            "Camino en gravilla y espacio de contemplación con banco",
        ],
        "reglas": [
            "Capacidad: 1 urna.",
            "Cuota de mantenimiento anual: US$ 15.",
            "El contenedor queda con 20 cm a la vista; la tapa de granito es la identificación.",
        ],
        "para_quien": "Familias que quieren un lugar permanente para visitar, con una inversión moderada.",
        "speech": (
            "«Después de la cremación, muchas familias se preguntan dónde dejar las "
            "cenizas. En nuestro Jardín 1, su ser querido descansa bajo una tapa de granito "
            "con su nombre, rodeado de plantas y con un banco para sentarse a recordar. "
            "Es un lugar para volver, con la dignidad que merece.»"
        ),
        "preguntas": [
            "¿Dónde le gustaría poder visitar a su ser querido?",
            "¿Tienen hoy las cenizas en casa o en un columbario temporal?",
            "¿Quién más de la familia participaría en las visitas?",
        ],
        "cierre": "«¿Le gustaría conocer el jardín esta semana para elegir el lugar con calma?»",
        "objecion": (
            "«Prefiero tener las cenizas en casa.» → «Es comprensible querer tenerlas cerca. "
            "En el jardín, toda la familia puede visitarlas, y las cenizas quedan protegidas "
            "si algún día hay mudanzas o cambios en el hogar.»"
        ),
        "tip": "El jardín vende solo: priorice siempre la visita.",
    },
    {
        "nombre": "Jardín de Cenizas · Familiar",
        "corto": "Jardín Familiar",
        "etiqueta": "Jardín 1 · Parcela familiar",
        "precio": "US$ 2.000",
        "pago": "Pago único o financiado · Mantenimiento US$ 25/año",
        "que_es": (
            "Parcela familiar en el Jardín 1 con cuatro contenedores agrupados, cada uno "
            "con tapa de granito grabada. Sin plazo de permanencia."
        ),
        "incluye": [
            "Inhumación de hasta 4 urnas",
            "Tapa de granito grabada para cada espacio",
            "Ubicación en el Jardín 1, con paisajismo de plantas de sombra",
            "Lugar permanente de homenaje familiar, sin plazo",
        ],
        "reglas": [
            "Capacidad: hasta 4 espacios.",
            "Permanencia: sin plazo.",
            "Cuota de mantenimiento anual: US$ 25 por parcela.",
        ],
        "para_quien": "Familias que buscan un espacio propio y permanente para varias generaciones.",
        "speech": (
            "«Así como una familia comparte una casa, también puede compartir un lugar de "
            "memoria. La parcela familiar reúne hasta cuatro seres queridos en un mismo "
            "espacio, para siempre, y cuesta US$ 500 por espacio, menos que comprarlos por "
            "separado.»"
        ),
        "preguntas": [
            "¿Les gustaría que la familia esté reunida en un mismo lugar?",
            "¿Cuántas personas de la familia considerarían este destino?",
            "¿Prefieren pagarlo de una vez o en cuotas?",
        ],
        "cierre": "«¿Reservamos hoy la parcela para su familia y la pagan en cuotas cómodas?»",
        "objecion": (
            "«Es mucho dinero.» → «Son US$ 500 por cada espacio, con financiamiento. Y es "
            "una decisión que se toma una sola vez para toda la familia.»"
        ),
        "tip": "Use el argumento por espacio (US$ 500) y no el total.",
    },
    {
        "nombre": "Jardín de Cenizas · Ecológico",
        "corto": "Jardín Ecológico",
        "etiqueta": "Jardín 2 · Bosque de las Orquídeas",
        "precio": "US$ 600",
        "pago": "Pago único o financiado · Placa memorial US$ 150 al término del plazo",
        "que_es": (
            "La urna biodegradable se entierra directamente en el suelo y se integra a la "
            "naturaleza. Jardín con agua corriente, en el Jardín 2 o en el Bosque de las "
            "Orquídeas."
        ),
        "incluye": [
            "Inhumación ecológica con urna biodegradable",
            "Placa de identificación (madera en el Jardín 2 · mármol en el Bosque)",
            "Entorno natural con agua corriente",
            "Permanencia de 3 años; luego, nombre en la placa memorial del monumento",
        ],
        "reglas": [
            "Capacidad: 1 urna. Espacio de 30 × 30 cm, 40 cm de profundidad.",
            "Permanencia: 3 años. Después, el espacio se reutiliza.",
            "Placa memorial en el monumento: US$ 150 (se cobra al término del plazo).",
            "Explique el plazo de 3 años con total transparencia desde la primera conversación.",
        ],
        "para_quien": "Personas con conciencia ambiental que desean que sus cenizas vuelvan a la tierra.",
        "speech": (
            "«Para quienes aman la naturaleza, el Jardín Ecológico es volver a la tierra. "
            "La urna se integra al suelo del bosque, junto al agua, y durante tres años la "
            "familia tiene un lugar señalado para visitar. Después, el nombre queda para "
            "siempre en el monumento memorial del jardín.»"
        ),
        "preguntas": [
            "¿Su ser querido tenía un vínculo especial con la naturaleza?",
            "¿Qué significa para ustedes «volver a la tierra»?",
            "¿Es importante para la familia un lugar con nombre para siempre?",
        ],
        "cierre": "«¿Le parece si visitamos el Bosque de las Orquídeas y elegimos juntos el lugar?»",
        "objecion": (
            "«¿Y después de 3 años?» → «La urna ya se habrá integrado a la tierra, como era "
            "el deseo. El nombre pasa a la placa memorial del monumento, que queda para "
            "siempre en el jardín.»"
        ),
        "tip": "Para familias católicas, enfatice que las cenizas reposan en el cementerio, un lugar dedicado a la memoria.",
    },
    {
        "nombre": "Jardín de Mascotas",
        "corto": "Jardín de Mascotas",
        "etiqueta": "Mascotas · Inhumación ecológica",
        "precio": "US$ 350 / US$ 500",
        "pago": "US$ 350 solo jardín · US$ 500 jardín + cremación · Placa memorial US$ 50",
        "que_es": (
            "Inhumación ecológica de las cenizas de la mascota: la urna biodegradable se "
            "entierra en el jardín y se identifica con una placa de madera."
        ),
        "incluye": [
            "Inhumación ecológica en el jardín de mascotas",
            "Placa de madera de 20 cm para identificación",
            "Cremación de la mascota (opción Jardín + Cremación)",
            "Permanencia de 3 años; luego, nombre en la placa memorial del monumento",
        ],
        "reglas": [
            "Capacidad: 1 mascota por servicio.",
            "Permanencia: 3 años. Después, el espacio se reutiliza.",
            "Placa memorial en el monumento: US$ 50 (se cobra al término del plazo).",
            "Pago único; puede contratarse como adicional al plan funerario.",
        ],
        "para_quien": "Familias que consideran a su mascota parte del hogar y desean un cierre digno.",
        "speech": (
            "«Su compañero fue parte de la familia, y merece una despedida a la altura. En "
            "nuestro Jardín de Mascotas descansa con su nombre, en un lugar verde donde "
            "ustedes pueden volver a recordarlo. Podemos encargarnos también de la "
            "cremación, todo en un solo lugar.»"
        ),
        "preguntas": [
            "¿Cómo se llamaba su compañero?",
            "¿Ya realizaron la cremación o necesitan que nos encarguemos?",
            "¿Les gustaría un lugar para visitarlo con los niños?",
        ],
        "cierre": "«¿Prefieren la opción con cremación incluida, para no preocuparse por nada más?»",
        "objecion": (
            "«Es solo una mascota.» → No discuta el vínculo de la familia. Si el cliente "
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
            "Si un cliente muestra interés, registre su contacto como «interesado Ceremonial».",
        ],
        "para_quien": "Familias que valoran un rito de despedida simbólico y un entorno contemplativo.",
        "speech": (
            "«Estamos preparando un nuevo jardín con una ceremonia de agua muy especial. "
            "Si le interesa, con gusto le aviso apenas esté disponible.»"
        ),
        "preguntas": ["¿Le gustaría que le avisemos cuando esté disponible?"],
        "cierre": "Registrar el interés y ofrecer, mientras tanto, el Jardín Individual o el Ecológico.",
        "objecion": "No aplica todavía.",
        "tip": "No prometa fechas ni precios.",
        "proximo": True,
    },
]

# ---------------------------------------------------------------------------
# 05 · Objeciones
# ---------------------------------------------------------------------------
METODO_OBJECIONES = [
    ("Validar", "Reconocer la emoción: «Entiendo, es una decisión importante.»"),
    ("Reposicionar", "Mostrar el valor desde otro ángulo, sin discutir."),
    ("Avanzar", "Proponer un siguiente paso concreto y amable."),
]

OBJECIONES = [
    ("«No quiero pensar en eso, es de mala suerte.»",
     "Entiendo, a nadie le gusta hablar de este tema.",
     "Planificar con calma es justamente lo que evita que su familia tenga que decidir "
     "en el peor momento. Es un acto de cuidado, no de pesimismo.",
     "¿Le dejo la información para que la conversen en casa?"),
    ("«Soy católico, la cremación no está permitida.»",
     "Su fe es muy importante y la respetamos.",
     "La Iglesia Católica permite la cremación desde 1963. Lo que pide es que las cenizas "
     "reposen en un lugar dedicado, como el cementerio, y no en casa ni dispersas. "
     "Nuestros jardines cumplen exactamente con eso.",
     "¿Le gustaría conocer el jardín y ver cómo es el lugar?"),
    ("«Prefiero la sepultura tradicional.»",
     "Es una tradición muy valiosa.",
     "El jardín conserva lo esencial de la sepultura: un lugar con nombre para visitar, "
     "con un costo mucho menor y en un entorno natural.",
     "¿Le muestro la diferencia de inversión entre ambas opciones?"),
    ("«Está caro.»",
     "Comprendo, es una inversión.",
     "En la urgencia los costos son mayores y se pagan de golpe. Hoy fija el precio y lo "
     "paga en cuotas: la Solución Modular cuesta alrededor de US$ 8,50 al mes.",
     "¿Qué cuota mensual le resultaría cómoda?"),
    ("«Tengo que hablarlo con mi familia.»",
     "Claro, es una decisión de familia.",
     "Facilite esa conversación: ofrezca un resumen simple y quedar disponible para "
     "resolver dudas de todos juntos.",
     "¿Puedo llamarle el [día] para ver si quedó alguna pregunta?"),
    ("«Prefiero tener las cenizas en casa.»",
     "Es natural querer tenerlas cerca.",
     "En el jardín toda la familia puede visitarlas, quedan protegidas ante mudanzas o "
     "cambios, y tienen un lugar con su nombre.",
     "¿Le gustaría visitar el jardín antes de decidir?"),
    ("«¿Por qué pagar mantenimiento cada año?»",
     "Es una pregunta muy válida.",
     "La cuota (US$ 15 o US$ 25 al año) mantiene el jardín siempre cuidado: poda, riego "
     "y limpieza. Es lo que garantiza que el lugar luzca digno en cada visita.",
     "¿Le explico qué incluye el cuidado del jardín?"),
    ("«No confío en estos planes.»",
     "Es una preocupación válida.",
     "Somos La Auxiliadora y Hogar de las Memorias, empresas de Vangrupo con trayectoria "
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
    ("Solución Modular", "US$ 1.000", "Hasta 120 cuotas (≈ US$ 8,50/mes)", "—", "Columbario 1 año incluido"),
    ("Jardín Individual", "US$ 600", "Único o financiado", "US$ 15/año", "Sin plazo"),
    ("Jardín Familiar", "US$ 2.000", "Único o financiado", "US$ 25/año", "Hasta 4 espacios, sin plazo"),
    ("Jardín Ecológico", "US$ 600", "Único o financiado", "—", "3 años · placa memorial US$ 150"),
    ("Jardín de Mascotas", "US$ 350 / 500", "Pago único", "—", "3 años · placa memorial US$ 50"),
    ("Jardín Ceremonial", "A definir", "A definir", "A definir", "Próximo lanzamiento"),
]

REGLAS_COMERCIALES = [
    ("Precios", "Precios sugeridos en US$ con IVA incluido. Consulte siempre la Ficha Técnica vigente."),
    ("Descuentos", "Prenecesidad: hasta 20% según la campaña del mes. Emergencia: máximo 5%. "
                   "Siempre con autorización del supervisor."),
    ("Mantenimiento", "Individual US$ 15/año y Familiar US$ 25/año. No es opcional: se explica antes de firmar."),
    ("Plazo de 3 años", "Ecológico y Mascotas: se explica con total transparencia en la primera conversación."),
    ("Placas memoriales", "US$ 150 (personas) y US$ 50 (mascotas), cobradas al término del plazo."),
    ("Dueño del contacto", "Quien registra primero. Sin interacción en 15 días, el contacto puede reasignarse."),
    ("Lo que NO se promete", "Fechas o precios del Jardín Ceremonial; descuentos fuera de política; "
                             "ubicaciones específicas sin confirmar disponibilidad."),
]

DESCUENTO_NO_ES_SALIDA = (
    "Competimos por valor, no por precio. Antes de ofrecer un descuento, refuerce lo que "
    "está incluido y la calidad del jardín. Un descuento fácil enseña al cliente a dudar del valor."
)

# ---------------------------------------------------------------------------
# 07 · Comisiones (propuesta)
# ---------------------------------------------------------------------------
COMISIONES = [
    ("Solución Modular", "10%", "US$ 88,50", "Pago único al pagar el cliente la 3ª cuota", "Si cancela antes de la 12ª cuota"),
    ("Jardín Individual", "10%", "US$ 53,10", "Contado: mes siguiente · Financiado: proporcional a lo cobrado", "Cancelación en 90 días"),
    ("Jardín Familiar", "8%", "US$ 141,59", "Contado: mes siguiente · Financiado: proporcional a lo cobrado", "Cancelación en 90 días"),
    ("Jardín Ecológico", "10%", "US$ 53,10", "Contado: mes siguiente · Financiado: proporcional a lo cobrado", "Cancelación en 90 días"),
    ("Mascotas · solo jardín", "8%", "US$ 24,78", "Mes siguiente al pago", "Cancelación en 90 días"),
    ("Mascotas · jardín + cremación", "8%", "US$ 35,40", "Mes siguiente al pago", "Cancelación en 90 días"),
    ("Jardín Ceremonial", "A definir", "—", "—", "—"),
]

COMISIONES_VALORES = [  # para la figura
    ("Solución Modular", 88.50), ("Jardín Individual", 53.10), ("Jardín Familiar", 141.59),
    ("Jardín Ecológico", 53.10), ("Mascotas · solo jardín", 24.78), ("Mascotas + cremación", 35.40),
]

REGLAS_COMISION = [
    "Base de cálculo: valor efectivamente cobrado al cliente, sin IVA (13%).",
    "No generan comisión: cuotas de mantenimiento ni placas memoriales.",
    "Bono de venta combinada: US$ 15 al vender la Solución Modular junto con cualquier jardín.",
    "Acelerador Día de los Muertos (opcional): +2 pp en Individual y Ecológico hasta el 30/11/2026.",
    "Estorno: la comisión se descuenta de los pagos siguientes al asesor.",
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
    ("Presentación «Jardines de Cenizas»", "Fotos y medidas de cada jardín para mostrar en la visita o en la casa."),
    ("Simulación de cuotas", "Calcule la cuota con el cliente: transparencia genera confianza."),
    ("Registro de contactos", "Un contacto no registrado no existe: sin datos no hay gestión ni comisión."),
]

CHECKLIST_CIERRE = [
    "Expliqué qué incluye el producto y qué no incluye.",
    "Expliqué la cuota de mantenimiento o el plazo de 3 años, según el caso.",
    "Confirmé el precio y la forma de pago con la Ficha Técnica vigente.",
    "El descuento, si lo hubo, está dentro de la política y autorizado.",
    "El cliente recibió copia del contrato y el contacto de su asesor.",
    "Registré la venta completa el mismo día.",
]

CIERRE_FRASE = (
    "Cada familia que atendemos recordará cómo la tratamos en uno de los momentos más "
    "sensibles de su vida. Ese es nuestro verdadero producto."
)
