"""Insere placas de acrílico 15x10 cm, centralizadas, sobre as tampas de granito.

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

# Diâmetro real assumido da tampa de granito (cm) — define a escala da placa.
DIAMETRO_TAMPA_CM = 40.0
PLACA_CM = (15.0, 10.0)
ESPESSURA_CM = 1.0  # acrílico 5 mm + espaçadores

# Elipse do topo de cada tampa na foto: centro (x, y), semi-eixos (a, b), inclinação (graus)
TAMPAS = [
    {"centro": (388, 691), "a": 134, "b": 34, "rot": -1.0,
     "nome": "Maria Aparecida Silva", "datas": "1941 – 2023"},
    {"centro": (820, 485), "a": 76, "b": 12.7, "rot": -0.5,
     "nome": "José Carlos Pereira", "datas": "1938 – 2021"},
    {"centro": (1054.6, 405.7), "a": 49, "b": 5.3, "rot": 0.0,
     "nome": "Ana Beatriz Souza", "datas": "1952 – 2024"},
]

TEX_W, TEX_H = 1500, 1000  # textura 15x10 cm a 100 px/cm
SS = 4  # supersampling


def textura_placa(nome, datas):
    """Acrílico cristal com cantos arredondados e texto gravado (fosco branco)."""
    tex = Image.new("RGBA", (TEX_W, TEX_H), (0, 0, 0, 0))
    mask = Image.new("L", (TEX_W, TEX_H), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, TEX_W - 1, TEX_H - 1], 70, fill=255)

    # Corpo do acrílico: leve tom branco translúcido + brilho diagonal
    yy, xx = np.mgrid[0:TEX_H, 0:TEX_W]
    brilho = np.clip(1.0 - np.abs((xx / TEX_W) - (yy / TEX_H) * 0.6 - 0.25) * 3.0, 0, 1)
    alpha = 55 + 90 * brilho
    corpo = np.dstack([
        np.full_like(alpha, 235), np.full_like(alpha, 242), np.full_like(alpha, 245), alpha,
    ]).astype(np.uint8)
    tex = Image.fromarray(corpo, "RGBA")

    d = ImageDraw.Draw(tex)
    # Borda polida (bisel) brilhante
    d.rounded_rectangle([6, 6, TEX_W - 7, TEX_H - 7], 66, outline=(255, 255, 255, 230), width=22)
    d.rounded_rectangle([60, 60, TEX_W - 61, TEX_H - 61], 40, outline=(250, 250, 250, 170), width=8)

    texto = (250, 250, 250, 255)
    f_topo = ImageFont.truetype(FONTE_TEXTO, 95)
    f_nome = ImageFont.truetype(FONTE_NOME, 200)
    f_datas = ImageFont.truetype(FONTE_TEXTO, 150)
    f_rodape = ImageFont.truetype(FONTE_ITALICO, 105)

    # Quebra o nome em duas linhas se não couber
    linhas = [nome]
    if d.textlength(nome, font=f_nome) > TEX_W - 220:
        partes = nome.split()
        meio = (len(partes) + 1) // 2
        linhas = [" ".join(partes[:meio]), " ".join(partes[meio:])]
        f_nome = ImageFont.truetype(FONTE_NOME, 175)

    cx = TEX_W / 2
    y = 120
    d.text((cx, y), "EM MEMÓRIA DE", font=f_topo, fill=texto, anchor="ma")
    y += 150
    for linha in linhas:
        d.text((cx, y), linha, font=f_nome, fill=texto, anchor="ma")
        y += 190
    y += 25
    d.line([(cx - 260, y), (cx + 260, y)], fill=texto, width=8)
    y += 45
    d.text((cx, y), datas, font=f_datas, fill=texto, anchor="ma")
    d.text((cx, TEX_H - 110), "Saudades eternas", font=f_rodape, fill=texto, anchor="md")

    tex.putalpha(Image.fromarray(np.minimum(np.array(tex.getchannel("A")), np.array(mask))))
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


def colar_placa(base, t):
    tex = textura_placa(t["nome"], t["datas"])
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
    d = ImageDraw.Draw(camada)

    # Sombra suave projetada (sol vindo do fundo/esquerda)
    sombra = Image.new("L", (w, h), 0)
    desloc = [(x + 3 * SS, y + 2 * SS) for x, y in local(chao)]
    ImageDraw.Draw(sombra).polygon(desloc, fill=150)
    sombra = sombra.filter(ImageFilter.GaussianBlur(2.5 * SS))
    camada = Image.composite(Image.new("RGBA", (w, h), (5, 8, 6, 255)), camada, sombra)
    d = ImageDraw.Draw(camada)

    # Espessura: faces laterais visíveis (frente e lado direito)
    lt, lc = local(topo), local(chao)
    d.polygon([lt[3], lt[2], lc[2], lc[3]], fill=(225, 238, 240, 215))
    d.polygon([lt[1], lt[2], lc[2], lc[1]], fill=(190, 205, 208, 190))

    # Face superior com o texto
    src = [(0, 0), (TEX_W, 0), (TEX_W, TEX_H), (0, TEX_H)]
    face = tex.transform((w, h), Image.PERSPECTIVE, tuple(coef_perspectiva(lt, src)),
                         Image.BICUBIC)
    camada = Image.alpha_composite(camada, face)
    # Aresta frontal polida reflete o sol
    ImageDraw.Draw(camada).line([lt[3], lt[2]], fill=(255, 255, 255, 235), width=max(2, SS))

    camada = camada.resize((x1 - x0, y1 - y0), Image.LANCZOS)
    base.alpha_composite(camada, (x0, y0))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--entrada", default="insumos/jardin_tampas_granito.jpg")
    ap.add_argument("--saida", default="salida/jardin_placas_memorial.jpg")
    args = ap.parse_args()

    base = Image.open(args.entrada).convert("RGBA")
    for t in TAMPAS:
        colar_placa(base, t)
    base.convert("RGB").save(args.saida, quality=95)
    print(f"Imagem gerada: {args.saida}")


if __name__ == "__main__":
    main()
