"""Atualização semanal: inclui os episódios novos do podcast na base e regenera planilha e dashboard.

Uso:
    pip install faster-whisper openpyxl numpy   (e ffmpeg instalado)
    python sermoes/scripts/atualizar.py

Para cada episódio do feed que ainda não está em dados/sermoes.json:
  1. tenta tirar o texto base do título do episódio (ex.: "Salmos 24 - Série: ...");
  2. se o título não tiver referência, transcreve os 10 primeiros minutos do áudio
     e procura o texto que o pregador anuncia ("Mateus, capítulo 7, versículo 13 ao 29");
  3. grava o resultado, salva a transcrição em transcricoes/ e roda gerar.py.
Ao final escreve dados/ultima_atualizacao.md com o resumo (o que entrou e o que precisa de revisão).
"""
import json, os, re, subprocess, sys, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import parsedate_to_datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import biblia, meta

RAIZ = os.path.dirname(AQUI)
BASE = os.path.join(RAIZ, 'dados', 'sermoes.json')
RESUMO = os.path.join(RAIZ, 'dados', 'ultima_atualizacao.md')
TRANSC = os.path.join(RAIZ, 'transcricoes')

NUM = {'um': 1, 'uma': 1, 'primeiro': 1, 'dois': 2, 'duas': 2, 'segundo': 2, 'três': 3, 'tres': 3, 'quatro': 4, 'cinco': 5, 'seis': 6,
       'sete': 7, 'oito': 8, 'nove': 9, 'dez': 10, 'onze': 11, 'doze': 12, 'treze': 13, 'catorze': 14, 'quatorze': 14, 'quinze': 15,
       'dezesseis': 16, 'dezessete': 17, 'dezoito': 18, 'dezenove': 19, 'vinte': 20, 'trinta': 30, 'quarenta': 40, 'cinquenta': 50}
NUMW = r'\d{1,3}|' + '|'.join(sorted(NUM, key=len, reverse=True))


def n(x):
    return int(x) if x.isdigit() else NUM.get(x.lower(), 0)


def ref_titulo(t):
    """Extrai a referência bíblica do título do episódio (mesma regra usada na base)."""
    cands = re.findall(r'\(([^()]*)\)', t) + re.findall(r'\[([^\]]*)\]', t) + re.findall(r'//\s*([^-]+?)\s+-', t) + [t]
    for c in cands:
        c2 = re.split(r'\s*-?\s*S[ée]rie\b|\s+-\s+S[ÉE]RIE', c)[0]
        if not biblia.parse(c2) and 'Série' in c:
            c2 = re.sub(r'^.*?S[ée]rie [^-]+-\s*', '', c)
        if c is t:
            m = re.search(r'((?:\d\s*|I\s+|1ª\s*)?(?:Salmos?|Romanos|Filipenses|Efésios|Gálatas|Lucas|Mateus|Marcos|João|Eclesiastes|Apocalipse|Atos|Coríntios|Hebreus|Isaías|Gênesis|Êxodo)\s+[\d:.;\-– ]+\d)', t)
            c2 = m.group(1) if m else ''
        c2 = re.split(r'\s+-\s+(?=[A-Za-zÀ-ú])', c2)[0]
        if biblia.parse(c2):
            return c2.strip(' -()')
    return ''


LIVRO_FALADO = (r'(?P<ord>primeira|segunda|terceira|primeiro|segundo|1ª|2ª|1|2|3)?\s*(?:carta\s+)?(?:de\s+\w+\s+)?(?:a|ao|aos|às)?\s*'
                r'(?P<liv>[A-Za-zÀ-ú]{3,})')
FALA = re.compile(LIVRO_FALADO + r'[\s,]+(?:no\s+|do\s+)?cap[íi]tulo\s+(?:de\s+número\s+)?(?P<c>' + NUMW + r')'
                  r'(?:[\s,]+(?:dos?\s+|a\s+partir\s+do\s+)?(?:vers[íi]culos?|versos?)\s+(?P<v1>' + NUMW + r')'
                  r'(?:\s+(?:a|ao|até\s+o|até)\s+(?:o\s+)?(?:vers[íi]culo\s+)?(?P<v2>' + NUMW + r'))?)?', re.I)
CURTA = re.compile(LIVRO_FALADO + r'[\s,]+(?P<c>\d{1,3})[\s,.:]+(?P<v1>\d{1,3})(?:\s*(?:a|ao|até|-)\s*(?P<v2>\d{1,3}))?', re.I)


import difflib, unicodedata
_NOMES = {}
for _a, _n, _t, _c, _ in biblia.LIVROS:
    _base = re.sub(r'^\d\s*', '', _n)
    _NOMES[''.join(c for c in unicodedata.normalize('NFKD', _base.lower()) if not unicodedata.combining(c))] = _base
_NOMES.update({'atus': 'Atos', 'ebreus': 'Hebreus', 'corintos': 'Coríntios', 'corintes': 'Coríntios', 'corinte': 'Coríntios',
               'corinthians': 'Coríntios', 'ephesios': 'Efésios', 'efeios': 'Efésios', 'felipenses': 'Filipenses', 'romano': 'Romanos',
               'marx': 'Marcos', 'matheus': 'Mateus', 'galatas': 'Gálatas', 'exo': 'Êxodo', 'timotio': 'Timóteo', 'timote': 'Timóteo',
               'atimote': 'Timóteo', 'pedra': 'Pedro', 'tessaloncense': 'Tessalonicenses', 'salmo': 'Salmos', 'eclesiax': 'Eclesiastes'})


def livro_aprox(palavra):
    w = ''.join(c for c in unicodedata.normalize('NFKD', palavra.lower()) if not unicodedata.combining(c))
    if w in _NOMES:
        return _NOMES[w]
    m = difflib.get_close_matches(w, list(_NOMES), n=1, cutoff=0.78)
    return _NOMES[m[0]] if m else ''


def ref_falada(texto):
    """Procura o texto anunciado na fala; devolve (referência, trecho) da primeira menção válida."""
    for rx in (FALA, CURTA):
        for m in rx.finditer(texto):
            nome = livro_aprox(m.group('liv'))
            if not nome:
                continue
            liv = (m.group('ord') or '') + ' ' + nome
            ps = biblia.parse(f"{liv} {n(m.group('c'))}")
            if not ps:
                continue
            ab = ps[0][0]
            ref = f"{ab} {n(m.group('c'))}"
            if m.group('v1'):
                ref += f".{n(m.group('v1'))}" + (f"-{n(m.group('v2'))}" if m.group('v2') else '')
            return ref, texto[max(0, m.start() - 60): m.end() + 100]
    return '', ''


def transcrever(url, minutos=10):
    import numpy as np
    from faster_whisper import WhisperModel
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-t', str(minutos * 60), '-i', url, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'],
                         capture_output=True, timeout=600).stdout
    audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    global _MODELO
    if '_MODELO' not in globals():
        _MODELO = WhisperModel('base', device='cpu', compute_type='int8')
    segs, _ = _MODELO.transcribe(audio, language='pt', beam_size=1, vad_filter=True)
    return [(round(s.start), s.text.strip()) for s in segs]


def tipo_de(t, serie):
    tl = t.lower()
    if 'especial de natal' in tl: return 'Especial de Natal'
    if 'podcast' in tl or serie in ('Podcast Ser Família', 'Vida Comum (podcast)'): return 'Podcast / conversa'
    if serie in ('Teologue', 'Conferência (RE)Pensando a Igreja', 'Com Todos os Santos') or 'conferência' in tl: return 'Palestra / conferência'
    return 'Sermão'


def main():
    dados = json.load(open(BASE))
    conhecidos = {x['podcast'] for x in dados['sermoes'] if x.get('podcast')} | set(dados.get('podcast_ignorados', []))
    titulos = {(x['titulo'].strip().lower(), x['data']) for x in dados['sermoes']}
    root = ET.fromstring(urllib.request.urlopen(dados['feed'], timeout=60).read())
    novos, revisar = [], []
    for it in root.findall('.//item'):
        link, t = it.findtext('link'), (it.findtext('title') or '').strip()
        data = parsedate_to_datetime(it.findtext('pubDate')).strftime('%d/%m/%Y')
        if link in conhecidos or (t.lower(), data) in titulos:
            continue
        enc = it.find('enclosure')
        serie = meta.serie(t)
        rec = dict(id='N' + datetime.strptime(data, '%d/%m/%Y').strftime('%Y%m%d') + f'{len(novos):02d}', titulo=t,
                   pregador=meta.pregador(t), data=data, ano=int(data[-4:]), data_aprox=False, periodo='', texto='',
                   confianca='Não identificado', fonte='', serie=serie, tipo=tipo_de(t, serie), youtube='', podcast=link,
                   evidencia='', notebooklm='')
        rt = ref_titulo(t)
        faixa = re.search(r'(\d+)-(\d+)$', rt)
        so_intervalo_da_serie = bool(faixa and not re.search(r'[.:]', rt) and int(faixa.group(2)) - int(faixa.group(1)) > 2)
        if rt and not so_intervalo_da_serie:
            rec.update(texto=rt, confianca='Confirmado', fonte='Título do episódio')
        elif enc is not None:
            try:
                segs = transcrever(enc.get('url'))
                txt = ' '.join(s for _, s in segs)
                os.makedirs(TRANSC, exist_ok=True)
                nome = re.sub(r'[^\w-]+', '_', t)[:70]
                with open(os.path.join(TRANSC, f"{rec['id']}_{nome}.txt"), 'w') as f:
                    f.write(f"{t}\n{link}\n(transcrição automática dos 10 primeiros minutos)\n\n" +
                            '\n'.join(f'[{s // 60:02d}:{s % 60:02d}] {x}' for s, x in segs))
                ref, trecho = ref_falada(txt)
                if ref:
                    rec.update(texto=ref, confianca='Provável', fonte='Transcrição do áudio (automática)', evidencia='…' + trecho + '…')
                else:
                    rec.update(confianca='Temático', fonte='Transcrição do áudio (automática)')
            except Exception as e:  # sem áudio ou falha: entra sem texto, para revisão
                print('falha na transcrição:', t, e)
        if rec['confianca'] != 'Confirmado':
            revisar.append(rec)
        novos.append(rec)
        print(f"+ {data} | {t} | {rec['texto'] or '—'} ({rec['confianca']})")

    linhas = [f"# Atualização de {datetime.now().strftime('%d/%m/%Y %H:%M')}", '']
    if not novos:
        linhas.append('Nenhum episódio novo no podcast.')
    else:
        dados['sermoes'].extend(novos)
        json.dump(dados, open(BASE, 'w'), ensure_ascii=False, indent=0)
        subprocess.run([sys.executable, os.path.join(AQUI, 'gerar.py')], check=True)
        linhas.append(f'{len(novos)} episódio(s) novo(s):')
        linhas += [f"- {x['data']} · {x['titulo']} · **{x['texto'] or '—'}** ({x['confianca']})" for x in novos]
        if revisar:
            linhas += ['', 'Para revisar (texto vindo da transcrição automática ou não encontrado):']
            linhas += [f"- {x['titulo']}: {x['texto'] or 'sem texto'}{' — trecho: ' + x['evidencia'] if x['evidencia'] else ''}" for x in revisar]
    open(RESUMO, 'w').write('\n'.join(linhas) + '\n')
    print('\n'.join(linhas))
    return len(novos)


if __name__ == '__main__':
    main()
