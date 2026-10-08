import re, unicodedata

# (abreviação, nome, testamento, capítulos, aliases regex sem acento/minúsculo)
LIVROS = [
    ("Gn", "Gênesis", "AT", 50, r"genesis|gn"), ("Êx", "Êxodo", "AT", 40, r"exodo|exo|ex"),
    ("Lv", "Levítico", "AT", 27, r"levitico|lv"), ("Nm", "Números", "AT", 36, r"numeros|nm"),
    ("Dt", "Deuteronômio", "AT", 34, r"deuteronomio|dt"), ("Js", "Josué", "AT", 24, r"josue|js"),
    ("Jz", "Juízes", "AT", 21, r"juizes|jz"), ("Rt", "Rute", "AT", 4, r"rute|rt"),
    ("1Sm", "1 Samuel", "AT", 31, r"1 ?samuel|1 ?sm"), ("2Sm", "2 Samuel", "AT", 24, r"2 ?samuel|2 ?sm"),
    ("1Rs", "1 Reis", "AT", 22, r"1 ?reis|1 ?rs"), ("2Rs", "2 Reis", "AT", 25, r"2 ?reis|2 ?rs"),
    ("1Cr", "1 Crônicas", "AT", 29, r"1 ?cronicas|1 ?cr"), ("2Cr", "2 Crônicas", "AT", 36, r"2 ?cronicas|2 ?cr"),
    ("Ed", "Esdras", "AT", 10, r"esdras|ed"), ("Ne", "Neemias", "AT", 13, r"neemias|ne"),
    ("Et", "Ester", "AT", 10, r"ester|et"), ("Jó", "Jó", "AT", 42, r"jó"),
    ("Sl", "Salmos", "AT", 150, r"salmos?|sl"), ("Pv", "Provérbios", "AT", 31, r"proverbios|pv"),
    ("Ec", "Eclesiastes", "AT", 12, r"eclesiastes|ec"), ("Ct", "Cantares", "AT", 8, r"canticos|cantares|ct"),
    ("Is", "Isaías", "AT", 66, r"isaias|is"), ("Jr", "Jeremias", "AT", 52, r"jeremias|jr"),
    ("Lm", "Lamentações", "AT", 5, r"lamentacoes|lm"), ("Ez", "Ezequiel", "AT", 48, r"ezequiel|ez"),
    ("Dn", "Daniel", "AT", 12, r"daniel|dn"), ("Os", "Oseias", "AT", 14, r"oseias|os"),
    ("Jl", "Joel", "AT", 3, r"joel|jl"), ("Am", "Amós", "AT", 9, r"amos|am"),
    ("Ob", "Obadias", "AT", 1, r"obadias|ob"), ("Jn", "Jonas", "AT", 4, r"jonas|jn"),
    ("Mq", "Miqueias", "AT", 7, r"miqueias|mq"), ("Na", "Naum", "AT", 3, r"naum|na"),
    ("Hc", "Habacuque", "AT", 3, r"habacuque|hc"), ("Sf", "Sofonias", "AT", 3, r"sofonias|sf"),
    ("Ag", "Ageu", "AT", 2, r"ageu|ag"), ("Zc", "Zacarias", "AT", 14, r"zacarias|zc"),
    ("Ml", "Malaquias", "AT", 4, r"malaquias|ml"),
    ("Mt", "Mateus", "NT", 28, r"mateus|mt"), ("Mc", "Marcos", "NT", 16, r"marcos|mc"),
    ("Lc", "Lucas", "NT", 24, r"lucas|lc"), ("Jo", "João", "NT", 21, r"joao|jo"),
    ("At", "Atos", "NT", 28, r"atos|at"), ("Rm", "Romanos", "NT", 16, r"romanos|rm"),
    ("1Co", "1 Coríntios", "NT", 16, r"1 ?corintios|1 ?co|1 ?cor"), ("2Co", "2 Coríntios", "NT", 13, r"2 ?corintios|2 ?co|2 ?cor"),
    ("Gl", "Gálatas", "NT", 6, r"galatas|gl"), ("Ef", "Efésios", "NT", 6, r"efesios|ef"),
    ("Fp", "Filipenses", "NT", 4, r"filipenses|fp"), ("Cl", "Colossenses", "NT", 4, r"colossenses|cl"),
    ("1Ts", "1 Tessalonicenses", "NT", 5, r"1 ?tessalonicenses|1 ?ts"), ("2Ts", "2 Tessalonicenses", "NT", 3, r"2 ?tessalonicenses|2 ?ts"),
    ("1Tm", "1 Timóteo", "NT", 6, r"1 ?timoteo|1 ?tm"), ("2Tm", "2 Timóteo", "NT", 4, r"2 ?timoteo|2 ?tm"),
    ("Tt", "Tito", "NT", 3, r"tito|tt"), ("Fm", "Filemom", "NT", 1, r"filemom|fm"),
    ("Hb", "Hebreus", "NT", 13, r"hebreus|hb"), ("Tg", "Tiago", "NT", 5, r"tiago|tg"),
    ("1Pe", "1 Pedro", "NT", 5, r"1 ?pedro|1 ?pe"), ("2Pe", "2 Pedro", "NT", 3, r"2 ?pedro|2 ?pe"),
    ("1Jo", "1 João", "NT", 5, r"1 ?joao|1 ?jo"), ("2Jo", "2 João", "NT", 1, r"2 ?joao|2 ?jo"),
    ("3Jo", "3 João", "NT", 1, r"3 ?joao|3 ?jo"), ("Jd", "Judas", "NT", 1, r"judas|jd"),
    ("Ap", "Apocalipse", "NT", 22, r"apocalipse|ap"),
]
INFO = {a: dict(nome=n, test=t, caps=c, ordem=i) for i, (a, n, t, c, _) in enumerate(LIVROS)}
GENERO = {}
for a in INFO:
    o = INFO[a]["ordem"]
    GENERO[a] = ("Pentateuco" if o < 5 else "Históricos" if o < 17 else "Poéticos" if o < 22 else
                 "Profetas maiores" if o < 27 else "Profetas menores" if o < 39 else "Evangelhos" if o < 43 else
                 "Atos" if o == 43 else "Cartas de Paulo" if o < 57 else "Cartas gerais" if o < 65 else "Apocalipse")


def _sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c) or c == "́" and False)


def _norm(s):
    s = s.replace("Jó", "\x01").replace("jó", "\x01")  # protege Jó antes de tirar acentos
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)).lower()
    s = s.replace("\x01", "jó")
    s = re.sub(r"\b(1|i|primeira|primeiro)(ª|a)?\s*(?=(corintios|cor?|co|pedro|pe|joao|jo|timoteo|tm|tessalonicenses|ts|samuel|sm|reis|rs|cronicas|cr)\b)", "1 ", s)
    s = re.sub(r"\b(2|ii|segunda|segundo)(ª|a)?\s*(?=(corintios|cor?|co|pedro|pe|joao|jo|timoteo|tm|tessalonicenses|ts|samuel|sm|reis|rs|cronicas|cr)\b)", "2 ", s)
    s = re.sub(r"\b(3|iii|terceira)(ª|a)?\s*(?=(joao|jo)\b)", "3 ", s)
    return s


_ALT = sorted([(a, p) for a, _, _, _, ps in LIVROS for p in ps.split("|")], key=lambda x: -len(x[1]))
BOOK_RE = re.compile(r"(?<![\w])(" + "|".join(f"(?P<b{i}>{p})" for i, (_, p) in enumerate(_ALT)) + r")\.?(?![\w])")


def parse(texto):
    """Retorna lista de (abrev, capitulos:set) a partir de um texto de referências."""
    if not texto:
        return []
    s = _norm(texto)
    s = s.replace("–", "-").replace("—", "-").replace(" a ", "-").replace(" à ", "-").replace(" ao ", "-")
    s = re.sub(r"(?<=[a-z])-(?=\d)", " ", s)
    s = re.sub(r"(\d)\s*:\s*-?", r"\1.", s)
    s = re.sub(r"(\d)\s*\.\s*(\d)", r"\1.\2", s)
    s = re.sub(r"\s*-\s*", "-", s)
    s = re.sub(r"(\d)\s+e\s+(\d)", r"\1;\2", s)
    s = re.sub(r"(\d)ss\b", r"\1", s)
    ms = list(BOOK_RE.finditer(s))
    out = []
    for k, m in enumerate(ms):
        ab = next(_ALT[int(g[1:])][0] for g, v in m.groupdict().items() if v)
        seg = s[m.end(): ms[k + 1].start() if k + 1 < len(ms) else len(s)]
        # só aceita abreviações curtas se seguidas de número (evita "at", "os", "is" soltos)
        if len(m.group(1)) <= 3 and not re.match(r"\s*\d", seg) and ab not in ("Jó",):
            continue
        caps = set()
        for parte in re.split(r"[;/]", seg):
            sub = re.split(r",", parte)
            for j, p in enumerate(sub):
                p = p.strip()
                mm = re.match(r"(\d+)(?:\.(\d+))?(?:-(\d+)(?:\.(\d+))?)?", p)
                if not mm:
                    continue
                c1, v1, x, v2 = mm.groups()
                if j > 0 and not v1:
                    continue  # ", 24-36": versículos do mesmo capítulo
                c1 = int(c1)
                if v1 and x and v2:
                    c2 = int(x)
                elif not v1 and x:
                    c2 = int(x)
                else:
                    c2 = c1
                mx = INFO[ab]["caps"]
                if 1 <= c1 <= mx:
                    caps.update(range(c1, min(max(c1, c2), mx) + 1))
            if not re.match(r"\s*\d", parte) and caps:
                break
        out.append((ab, caps))
    # junta livros repetidos
    res = {}
    for ab, caps in out:
        res.setdefault(ab, set()).update(caps)
    return list(res.items())


def fmt(ab, caps):
    if not caps:
        return ab
    cs = sorted(caps)
    rngs, a = [], cs[0]
    for x, y in zip(cs, cs[1:] + [None]):
        if y != x + 1:
            rngs.append(f"{a}" if a == x else f"{a}–{x}")
            a = y
    return f"{ab} {', '.join(rngs)}"


if __name__ == "__main__":
    for t in ["Mt 7.13-29", "1Co 12.12ss", "Mt 5–7 (introdução à série)", "Gn 1.31–2.3; 2.15", "Jo 13–17", "Rt 1–4",
              "Gálatas (panorama do livro)", "Dn 4.10-17, 24-36", "Mc 10.35-45? / Fp 2.3", "Rm 1.20ss? / Jó 41.11",
              "Is 7.14; Mt 1.23; Is 53", "Salmos 23", "1 Coríntios 6. 1-11", "1ª Coríntios 1:18-2:5", "I Coríntios 1:10-17",
              "Eclesiastes 9:13 à 10:20", "Mateus 24:42-25:30", "Eclesiastes 5:8 - 6:12", "Romanos 6.15-23/ 7.1-6",
              "Apocalipse 3:14-21", "(At 12)", "(At 10 e 11)", "Atos 9", "Gl. 5:20 - 6:5", "Gálatas 3:26-4:-7",
              "Ef. 4.17 - 5:4", "Romanos 8-16", "Lucas 15", "Salmo 19", "(At-4)", "1Jo 2.28–3.3", "2Rs 22.8ss",
              "Jo 20.1-18", "1Jo 4.7ss", "Jn 2.10–3.3", "Sl 119.105", "Lc 18.18-30; 19.1-10", "Êx 20.1-3", "2Co 8–9",
              "Ef 1.3-14", "Jó 37.23; Sl 115.3; Dn 4.35 (vários textos)", "At 16.11-40", "Mt 16.18; 18.15-20", "Rt 1–4"]:
        print(f"{t:45s} -> {[fmt(a, c) for a, c in parse(t)]}")
