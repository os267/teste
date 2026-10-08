# Sermões FDQC: texto base

- `sermoes_fdqc.xlsx`: os 240 vídeos da lista, com título completo, pregador, série, período aproximado, link e uma sugestão de texto base (com grau de confiança).
- `sermoes_fdqc_preenchida.xlsx`: **planilha preenchida**. Os vídeos foram cruzados com o podcast da igreja (feed público do SoundCloud), e os 10 primeiros minutos de cada áudio foram transcritos para identificar o texto anunciado. Cada linha traz a data de publicação no podcast, o status do texto base e o trecho da transcrição que serve de evidência.
- `transcricoes/`: as transcrições automáticas (10 primeiros minutos) de 218 sermões.
- `preencher_texto_base.py`: alternativa via YouTube (data e legenda), para rodar no seu computador. Não é mais necessária.

## Alternativa: script do YouTube (rodar no seu computador)

```
pip install yt-dlp openpyxl
python preencher_texto_base.py sermoes_fdqc.xlsx
```

Gera `sermoes_fdqc_preenchida.xlsx`. Se o script parar no meio, rode de novo com o arquivo `_preenchida.xlsx`: ele continua de onde parou.

## NotebookLM para o que sobrar (linhas "Sem áudio no podcast")

1. Crie um caderno por série (ou por lote de até 50 vídeos) e adicione cada link como fonte do YouTube.
2. Use o prompt:

> Para cada fonte, informe: título do vídeo | texto bíblico base anunciado pelo pregador (livro, capítulo e versículos) | trecho da fala em que ele anuncia o texto. Se não houver um texto base anunciado, escreva "temático" e liste as passagens mais citadas. Responda em tabela.

3. Confira os casos duvidosos pelo trecho citado (o NotebookLM mostra a fonte) e cole o resultado na planilha.

## Atualização semanal automática

Toda quinta-feira à noite uma rotina agendada roda:

```
pip install faster-whisper openpyxl numpy
python sermoes/scripts/atualizar.py   # busca episódios novos no podcast e atualiza dados/sermoes.json
python sermoes/scripts/gerar.py       # (chamado pelo atualizar.py) gera planilha e dashboard
```

- `dados/sermoes.json`: a base (fonte de verdade). Para corrigir um texto base à mão, edite aqui e rode `gerar.py`.
- `dados/ultima_atualizacao.md`: resumo da última execução (o que entrou e o que precisa de revisão).
- `sermoes_fdqc_completa.xlsx` e `dashboard.html`: gerados a partir da base.
