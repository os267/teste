# Sermões FDQC: texto base

- `sermoes_fdqc.xlsx`: os 240 vídeos da lista, com título completo, pregador, série, período aproximado, link e uma sugestão de texto base (com grau de confiança).
- `preencher_texto_base.py`: preenche a data exata e procura o texto base na descrição e na legenda de cada vídeo.

## Passo 1: script (rodar no seu computador)

```
pip install yt-dlp openpyxl
python preencher_texto_base.py sermoes_fdqc.xlsx
```

Gera `sermoes_fdqc_preenchida.xlsx`. Se o script parar no meio, rode de novo com o arquivo `_preenchida.xlsx`: ele continua de onde parou.

## Passo 2: NotebookLM para o que sobrar

1. Crie um caderno por série (ou por lote de até 50 vídeos) e adicione cada link como fonte do YouTube.
2. Use o prompt:

> Para cada fonte, informe: título do vídeo | texto bíblico base anunciado pelo pregador (livro, capítulo e versículos) | trecho da fala em que ele anuncia o texto. Se não houver um texto base anunciado, escreva "temático" e liste as passagens mais citadas. Responda em tabela.

3. Confira os casos duvidosos pelo trecho citado (o NotebookLM mostra a fonte) e cole o resultado na planilha.
