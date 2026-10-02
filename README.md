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

## Placas de memorialização (visualização)

```bash
pip install pillow numpy
python gerar_placas_memorial.py                   # concreto + placa de bronze
python gerar_placas_memorial.py --versao madeira  # concreto + tampa de bolacha de madeira gravada a laser
```

Troca os cilindros de granito da foto `insumos/jardin_tampas_granito.jpg` por cilindros de concreto
aparente (mantendo a luz do ambiente e a folhagem na frente) e insere placas de bronze fundido de 15×10 cm,
centralizadas sobre as tampas, com moldura e texto em relevo ("Em memória de", nome, datas). Resultado em
`salida/jardin_placas_memorial.jpg`. Nomes, datas e geometria dos cilindros ficam na lista `TAMPAS` do script.
Na versão `madeira`, a tampa vira uma bolacha de madeira (anéis de crescimento e casca na borda) com o texto
gravado a laser direto na madeira, sem placa; resultado em `salida/jardin_tampa_madeira_laser.jpg`.
