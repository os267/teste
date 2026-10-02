"""Troca os cilindros de granito por concreto e insere placas de bronze 15x10 cm,
centralizadas sobre as tampas, como placas de memorialização.

Uso:
    pip install pillow numpy
    python gerar_placas_memorial.py --entrada insumos/jardin_tampas_granito.jpg \
        --saida salida/jardin_placas_memorial.jpg
"""
import argparse

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONTE_NOME = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
FONTE_TEXTO = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
FONTE_ITALICO = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"

# Diâmetro real assumido da tampa (cm) — define a escala da placa.
DIAMETRO_TAMPA_CM = 40.0
PLACA_CM = (15.0, 10.0)
ESPESSURA_CM = 0.6  # placa de bronze fundido

# Geometria de cada cilindro na foto:
#   centro/a/b/rot: elipse do topo da tampa (px, graus)
#   aba: altura da borda lateral da tampa (px)
#   corpo_a / corpo_base: meia-largura e base (y) do corpo abaixo da tampa (px)
TAMPAS = [
    {"centro": (388, 691), "a": 134, "b": 34, "rot": -1.0,
     "aba": 20, "corpo_a": 118, "corpo_base": 797,
     "nome": "Maria Aparecida Silva", "datas": "1941 – 2023"},
    {"centro": (820, 485), "a": 76, "b": 12.7, "rot": -0.5,
     "aba": 9, "corpo_a": 68, "corpo_base": 532,
     "nome": "José Carlos Pereira", "datas": "1938 – 2021"},
    {"centro": (1054.6, 405.7), "a": 49, "b": 5.3, "rot": 0.0,
     "aba": 8, "corpo_a": 44, "corpo_base": 434,
     "nome": "Ana Beatriz Souza", "datas": "1952 – 2024"},
]

TEX_W, TEX_H = 1500, 1000  # textura 15x10 cm a 100 px/cm
SS = 4  # supersampling

CONCRETO = np.array([186.0, 182.0, 174.0])  # cinza concreto aparente


# --------------------------------------------------------------------------- concreto

def mascaras_cilindro(t, shape, ss=1):
    """Máscaras booleanas (topo, aba, corpo) do cilindro, numa grade ss vezes mais fina."""
    h, w = shape
    yy, xx = (np.mgrid[0:h * ss, 0:w * ss].astype(float) + 0.5) / ss - 0.5
    cx, cy = t["centro"]
    a, b, aba = t["a"] + 2, t["b"] + 1.5, t["aba"]
    topo = ((xx - cx) / a) ** 2 + ((yy - cy) / b) ** 2 <= 1
    arco = cy + b * np.sqrt(np.clip(1 - ((xx - cx) / a) ** 2, 0, None))
    aba_m = (np.abs(xx - cx) <= a) & (yy >= cy) & (yy <= arco + aba) & ~topo
    ca = t["corpo_a"]
    base = t["corpo_base"] - 0.9 * b * (1 - np.sqrt(np.clip(1 - ((xx - cx) / ca) ** 2, 0, None)))
    corpo = (np.abs(xx - cx) <= ca) & (yy >= cy) & (yy <= base) & ~topo & ~aba_m
    return topo, aba_m, corpo, xx, yy


def cobertura(m, ss):
    """Reduz uma máscara supersampled para cobertura fracionária (anti-aliasing)."""
    h, w = m.shape[0] // ss, m.shape[1] // ss
    return m.reshape(h, ss, w, ss).mean(axis=(1, 3))


def ruido(shape, sigma, rng):
    img = Image.fromarray((rng.random(shape) * 255).astype(np.uint8))
    if sigma > 0:
        img = img.filter(ImageFilter.GaussianBlur(sigma))
    r = np.asarray(img, dtype=float)
    return (r - r.mean()) / (r.std() + 1e-6)


def aplicar_concreto(img, t, rng, ss=4):
    """Substitui o granito do cilindro por concreto, preservando luz e folhagem à frente."""
    cx, cy = t["centro"]
    x0, x1 = int(cx - t["a"] - 6), int(cx + t["a"] + 7)
    y0, y1 = int(cy - t["b"] - 6), int(t["corpo_base"] + 6)
    arr = img[y0:y1, x0:x1].astype(float)
    h, w, _ = arr.shape
    loc = dict(t, centro=(cx - x0, cy - y0), corpo_base=t["corpo_base"] - y0)
    topo, aba, corpo, xx, yy = mascaras_cilindro(loc, (h, w), ss)

    # Sombreamento por região (calculado na grade fina e depois reduzido)
    u = np.clip((xx - loc["centro"][0]) / t["a"], -1, 1)
    lateral = 0.78 - 0.18 * u - 0.10 * u ** 2  # luz do fundo-esquerda
    arco = loc["centro"][1] + t["b"] * np.sqrt(np.clip(1 - u ** 2, 0, None)) + t["aba"]
    sob_aba = 0.62 + 0.38 * np.clip((yy - arco) / max(2.0, t["aba"] * 0.6), 0, 1)
    base = loc["corpo_base"]
    chao = 1 - 0.25 * np.clip((yy - (base - 2.5 * t["aba"])) / (2.5 * t["aba"]), 0, 1)
    tom_ss = np.where(topo, 1.0, 0.0) + np.where(aba, lateral, 0.0) \
        + np.where(corpo, lateral * 0.80 * sob_aba * chao, 0.0)
    regiao_ss = topo | aba | corpo
    cob = cobertura(regiao_ss, ss)
    tom = cobertura(tom_ss, ss) / np.maximum(cob, 1e-6)
    cob_topo = cobertura(topo, ss)
    # Leve chanfro iluminado na borda entre topo e aba
    borda = cobertura(topo & ~np.roll(topo, -2 * ss, axis=0), ss)

    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    # Folhagem na frente do cilindro (verde, mais clara que o granito) fica intacta
    folha = (g > r * 1.05) & (g > b * 1.02) & (lum > 40) & (g - np.minimum(r, b) > 8)
    folha &= cob_topo < 0.5
    folha = np.asarray(Image.fromarray((folha * 255).astype(np.uint8))
                       .filter(ImageFilter.MedianFilter(3)).filter(ImageFilter.GaussianBlur(0.5)),
                       float) / 255.0

    # Luz difusa local (manchas de sol/sombra das árvores), sem os grãos do granito
    luz = np.asarray(Image.fromarray(np.clip(lum, 0, 255).astype(np.uint8))
                     .filter(ImageFilter.GaussianBlur(max(2.0, t["b"] / 6))), float)
    ref = np.median(luz[cob_topo > 0.99])
    mod = np.clip(luz / (ref + 1e-6), 0.6, 1.5) ** 0.35

    # Textura de concreto: grão fino + manchas suaves + poros
    escala = max(0.5, t["a"] / 134)
    textura = 5.5 * ruido((h, w), 0.6, rng) + 7.0 * ruido((h, w), 6 * escala, rng)
    poros = (rng.random((h, w)) < 0.004 * escala) * -28.0

    novo = CONCRETO[None, None, :] * (tom * mod)[..., None]
    novo += ((textura + poros) * tom)[..., None]
    novo += (borda * 18)[..., None]

    alfa = (cob * (1 - folha))[..., None]
    saida = img.copy()
    saida[y0:y1, x0:x1] = np.clip(arr * (1 - alfa) + np.clip(novo, 0, 255) * alfa, 0, 255)
    return saida


# --------------------------------------------------------------------------- placa de bronze

def textura_placa(nome, datas, rng):
    """Bronze fundido: fundo com pátina escura, letras e moldura em relevo polidas."""
    yy, xx = np.mgrid[0:TEX_H, 0:TEX_W].astype(float)

    # Fundo rebaixado: pátina marrom escura com textura jateada
    grao = ruido((TEX_H, TEX_W), 1.2, rng)
    fundo = np.dstack([
        78 + 7 * grao, 52 + 5 * grao, 28 + 3 * grao,
    ])

    # Relevo (moldura + texto) desenhado como máscara
    relevo = Image.new("L", (TEX_W, TEX_H), 0)
    d = ImageDraw.Draw(relevo)
    d.rounded_rectangle([0, 0, TEX_W - 1, TEX_H - 1], 40, outline=255, width=55)
    d.rounded_rectangle([95, 95, TEX_W - 96, TEX_H - 96], 20, outline=255, width=12)

    f_topo = ImageFont.truetype(FONTE_TEXTO, 92)
    f_nome = ImageFont.truetype(FONTE_NOME, 195)
    f_datas = ImageFont.truetype(FONTE_NOME, 145)
    f_rodape = ImageFont.truetype(FONTE_ITALICO, 100)

    linhas = [nome]
    if d.textlength(nome, font=f_nome) > TEX_W - 260:
        partes = nome.split()
        meio = (len(partes) + 1) // 2
        linhas = [" ".join(partes[:meio]), " ".join(partes[meio:])]
        f_nome = ImageFont.truetype(FONTE_NOME, 170)

    cx = TEX_W / 2
    y = 140
    d.text((cx, y), "EM MEMÓRIA DE", font=f_topo, fill=255, anchor="ma")
    y += 140
    for linha in linhas:
        d.text((cx, y), linha, font=f_nome, fill=255, anchor="ma")
        y += 180
    y += 20
    d.line([(cx - 240, y), (cx + 240, y)], fill=255, width=10)
    y += 40
    d.text((cx, y), datas, font=f_datas, fill=255, anchor="ma")
    d.text((cx, TEX_H - 130), "Saudades eternas", font=f_rodape, fill=255, anchor="md")

    m = np.asarray(relevo, float) / 255.0
    # Bisel do relevo: luz vinda de cima-esquerda
    alt = np.asarray(relevo.filter(ImageFilter.GaussianBlur(4)), float) / 255.0
    gy, gx = np.gradient(alt)
    bisel = np.clip(-(gx + gy) * 6, -1, 1)

    # Bronze polido com brilho metálico diagonal
    brilho = np.clip(1 - np.abs(xx / TEX_W * 0.8 + yy / TEX_H * 0.5 - 0.55) * 2.2, 0, 1)
    polido = np.dstack([
        176 + 60 * brilho, 128 + 52 * brilho, 62 + 34 * brilho,
    ])
    cor = fundo * (1 - m[..., None]) + polido * m[..., None]
    cor += (bisel * 55)[..., None]
    # Reflexo suave em toda a peça
    cor += (brilho * 18)[..., None]

    mask = Image.new("L", (TEX_W, TEX_H), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, TEX_W - 1, TEX_H - 1], 40, fill=255)
    tex = Image.fromarray(np.clip(cor, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
    tex.putalpha(mask)
    return tex


def coef_perspectiva(dst, src):
    """Coeficientes para Image.transform(PERSPECTIVE): mapeia saída (dst) -> textura (src)."""
    m = []
    for (x, y), (u, v) in zip(dst, src):
        m.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        m.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    b = np.array(src, dtype=float).reshape(8)
    return np.linalg.solve(np.array(m, dtype=float), b)


def quad_na_tampa(t, dy=0.0):
    """Cantos da placa (TL, TR, BR, BL) projetados no topo elíptico da tampa."""
    raio = DIAMETRO_TAMPA_CM / 2
    hw, hh = PLACA_CM[0] / 2, PLACA_CM[1] / 2
    sx, sy = t["a"] / raio, t["b"] / raio
    ang = np.radians(t["rot"])
    cos, sin = np.cos(ang), np.sin(ang)
    cx, cy = t["centro"]
    pts = []
    for u, v in [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]:
        # leve convergência de perspectiva: borda de trás um pouco mais estreita
        u *= 1.0 + 0.02 * (v / hh)
        x, y = u * sx, v * sy
        pts.append((cx + x * cos - y * sin, cy + x * sin + y * cos + dy))
    return pts


def colar_placa(base, t, rng):
    tex = textura_placa(t["nome"], t["datas"], rng)
    esp_px = ESPESSURA_CM * t["a"] / (DIAMETRO_TAMPA_CM / 2) * 0.75  # escala vertical ~75% da horizontal
    esp_px = max(1.0, min(esp_px, 6.0))
    topo = quad_na_tampa(t, dy=-esp_px)
    chao = quad_na_tampa(t)

    xs = [p[0] for p in topo + chao]
    ys = [p[1] for p in topo + chao]
    x0, y0 = int(min(xs)) - 12, int(min(ys)) - 12
    x1, y1 = int(max(xs)) + 12, int(max(ys)) + 12
    w, h = (x1 - x0) * SS, (y1 - y0) * SS

    def local(pts):
        return [((x - x0) * SS, (y - y0) * SS) for x, y in pts]

    camada = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    # Sombra suave projetada sobre o concreto
    sombra = Image.new("L", (w, h), 0)
    desloc = [(x + 3 * SS, y + 2 * SS) for x, y in local(chao)]
    ImageDraw.Draw(sombra).polygon(desloc, fill=120)
    sombra = sombra.filter(ImageFilter.GaussianBlur(2.5 * SS))
    camada = Image.composite(Image.new("RGBA", (w, h), (40, 36, 30, 255)), camada, sombra)
    d = ImageDraw.Draw(camada)

    # Espessura: faces laterais em bronze (frente e lado direito)
    lt, lc = local(topo), local(chao)
    d.polygon([lt[3], lt[2], lc[2], lc[3]], fill=(150, 100, 48, 255))
    d.polygon([lt[1], lt[2], lc[2], lc[1]], fill=(105, 68, 32, 255))

    # Face superior com o texto em relevo
    src = [(0, 0), (TEX_W, 0), (TEX_W, TEX_H), (0, TEX_H)]
    face = tex.transform((w, h), Image.PERSPECTIVE, tuple(coef_perspectiva(lt, src)),
                         Image.BICUBIC)
    camada = Image.alpha_composite(camada, face)
    # Aresta frontal polida reflete o sol
    ImageDraw.Draw(camada).line([lt[3], lt[2]], fill=(235, 190, 120, 230), width=max(2, SS))

    camada = camada.resize((x1 - x0, y1 - y0), Image.LANCZOS)
    base.alpha_composite(camada, (x0, y0))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--entrada", default="insumos/jardin_tampas_granito.jpg")
    ap.add_argument("--saida", default="salida/jardin_placas_memorial.jpg")
    args = ap.parse_args()

    rng = np.random.default_rng(7)
    arr = np.asarray(Image.open(args.entrada).convert("RGB"))
    for t in TAMPAS:
        arr = aplicar_concreto(arr, t, rng)
    base = Image.fromarray(arr).convert("RGBA")
    for t in TAMPAS:
        colar_placa(base, t, rng)
    base.convert("RGB").save(args.saida, quality=95)
    print(f"Imagem gerada: {args.saida}")


if __name__ == "__main__":
    main()
