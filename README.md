# Ficha Técnica — Portafolio de Cremación · La Auxiliadora (Vangrupo)

Campaña Día de los Muertos 2026.

## Generar los entregables

```bash
pip install pandas openpyxl
python generar_ficha_tecnica.py --salida salida
```

Salidas en `salida/`:

| Archivo | Contenido |
|---|---|
| `Ficha_Tecnica_Cremacion_Vangrupo.xlsx` | Hoja **Tabla Gral. - Visión Comercial** (comparativo por producto) y hoja **Ficha Técnica Consolidada** (fichas individuales con la paleta de marca, un salto de página por ficha). |
| `Fichas_Tecnicas_Cremacion_Vangrupo.html` | Fichas técnicas individuales listas para imprimir o guardar en PDF (Ctrl+P → A4, una ficha por página). |

Todos los datos de producto viven en la lista `PRODUCTOS` del script: al editarla, ambos entregables se regeneran de forma consistente.
