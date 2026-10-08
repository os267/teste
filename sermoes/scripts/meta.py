import re,unicodedata
def _n(s): return ''.join(c for c in unicodedata.normalize('NFKD',s) if not unicodedata.combining(c)).lower()
SERIES=[('A Fábrica de Ídolos','fabrica de idolos'),('A Pessoa do Evangelho','pessoa do evangelho'),('A Vida no Reino','vida no reino'),
('Advento (2021)','^advento$'),('Anátema – O Outro Evangelho (Gálatas)','anatema'),('As Doutrinas da Graça','doutrinas da graca'),
('As Parábolas de Jesus','parabolas de jesus'),('Atos – O Evangelho em Movimento','^atos'),('Atributos Divinos','atributos divinos'),
('Cartas à Igreja (Apocalipse)','cartas . igreja'),('Celebração da Redenção','celebracao da redencao'),('Cristo em Nós','cristo em nos'),
('Cristo, Nossa Esperança','cristo, nossa esperanca'),('Cristão e Cultura','cristao e (a )?cultura'),('Céus | Igreja | Terra','^ceus'),
('Definição (Romanos 1–7)','^definicao'),('Disciplina é Liberdade','disciplina e liberdade'),('Disciplinas Espirituais','^disciplinas espirituais'),
('Efésios','^efesios'),('Ele Veio Para Servir','ele veio para servir'),('Em Cristo, no Mundo (1 Coríntios)','em cristo, no mundo'),
('Filipenses','^filipenses'),('Fome por Deus','fome por deus'),('Fé & Trabalho','fe & trabalho'),('Graça sobre Graça','graca sobre graca'),
('Igreja, O Evangelho Visível','evangelho visivel'),('Jonas','^jonas'),('Nova Era','nova era'),('O Evangelho Completo','evangelho completo'),
('O Evangelho na Vida','evangelho na vida'),('O Plano Perfeito (Romanos 8–16)','plano perfeito'),('O Poder de Deus (Romanos)','poder de deus'),
('Orando e Vivendo Salmos','orando e vivendo salmos'),('Oração','^oracao$'),('Prepare o Coração para a Páscoa','prepare o coracao'),
('Páscoa em Família','pascoa em familia'),('Reforma (2024)','^reforma$'),('Reformados','reformados'),('Sinais da Verdadeira Espiritualidade','^sinais'),
('Solitude & Comunidade','solitude & comunidade'),('Síndrome dos Gálatas','sindrome dos galatas'),('Trindade','^trindade$'),
('Vanitas Vanitatum (Eclesiastes)','vanitas'),('Verbos Cristãos','verbos cristaos'),('Fundamentos do NT','^fundamentos'),
('Igreja (2018)',r'^igreja \(primeiras'),('Vida Cristã Coerente','vida crista coerente'),('Teologue','teologue'),
('Conferência (RE)Pensando a Igreja','repensando'),('Podcast Ser Família','podcast ser familia'),('Vida Comum (podcast)','vida comum'),
('Com Todos os Santos','com todos os santos'),('Ensino das Escrituras','ensino das escrituras')]
PAT=re.compile(r'(?:Mini-?s[ée]rie|S[ÉE]RIE|S[ée]rie)\s*:?\s*([^)\]|]+)',re.I)
def serie(titulo,extra=''):
    cands=[x.strip(' -') for x in PAT.findall(titulo)]
    for k in ['Com Todos os Santos','Ensino das Escrituras','Teologue','Vida Comum','Podcast Ser Família','RE)Pensando','Re)pensando','Síndrome dos Gálatas','Fundamentos:','Vida Cristã Coerente']:
        if k.lower() in titulo.lower(): cands.append(k.replace('RE)Pensando','repensando').replace('Re)pensando','repensando').replace('Fundamentos:','fundamentos'))
    if extra: cands.append(extra)
    for c in cands:
        cn=_n(c).strip()
        for nome,p in SERIES:
            if re.search(p,cn): return nome
    return ''
PREG=[('Fabiano e Jaqueline Krehnke',r'fabiano e jaqueline'),('Jaqueline Krehnke',r'jaqueline'),('Fabiano Krehnke',r'fabiano'),
('Leandro Vieira',r'leandro vieira'),('Leandro Alves',r'leandro alves'),('Leandro Barreto',r'leandro barreto'),('Felipe Bartoszewski',r'bart\w*z\w*ski'),
('Felipe Garrote',r'garrote'),('Felipe Barros',r'felipe barros'),('Lucas Gregory',r'lucas gregory'),('Lucas Balzer',r'balzer'),('Lucas Ribas',r'lucas ribas'),
('Leivison Rosa',r'leivison'),('Juliano Marold',r'marold'),('Willian Amaral',r'willian amaral'),('Dayse Fontoura',r'dayse'),('Fabio Fontoura',r'fabio fontoura'),
('Marcelo Rutsatz',r'rutsatz'),('Fernando Souza',r'fernando souza'),('Yago Martins',r'yago'),('Igor Miguel',r'igor miguel'),('Thiago Guerra',r'thiago guerra'),
('Cristiano Gaspar',r'cristiano gaspar'),('Filipe Niel',r'filipe niel'),('Guilherme de Carvalho',r'guilherme de carvalho'),('Vanessa Belmonte',r'vanessa belmonte'),
('Paulo Borges Junior',r'paulo borges'),('Luciano Subirá',r'subira'),('Douglas Gonçalves',r'douglas goncalves'),('Valdir Reis',r'valdir reis'),
('Teofilo Hayashi',r'hayashi'),('Mario Freitas',r'mario freitas'),('Caleb Edwards & Justin Rizzo',r'caleb edwards')]
def pregador(titulo):
    t=_n(titulo)
    for nome,p in PREG:
        if re.search(p,t): return nome
    return ''
