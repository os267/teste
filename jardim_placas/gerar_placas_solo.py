"""Remove as placas 'aéreas' (sobre a folhagem) e distribui placas de madeira
fincadas no solo por todo o jardim."""
import numpy as np, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont
random.seed(7)
im = Image.open('foto_original.webp').convert('RGB'); W, H = im.size
a = np.asarray(im).astype(float)

# 1) placas a remover (cx, cy, rx, ry, stake_bottom_y ou None)
REMOVER = [(196,605,15,14,None),(322,592,14,13,None),(292,621,14,13,640),(422,611,14,13,None),
           (855,605,16,15,None),(1152,569,16,14,None),(1272,569,16,14,None,(2.4,0)),(1286,616,16,15,None),
           (1475,665,17,17,None)]
def disc_mask(cx,cy,rx,ry,sb,pad=4):
    m = Image.new('L',(W,H),0); d = ImageDraw.Draw(m)
    d.ellipse([cx-rx-pad,cy-ry-pad,cx+rx+pad,cy+ry+pad],fill=255)
    if sb: d.rectangle([cx-3,cy,cx+3,sb],fill=255)
    return m.filter(ImageFilter.GaussianBlur(2))
def woodness(p):  # fração de pixels com cor de madeira clara
    r,g,b = p[...,0],p[...,1],p[...,2]
    return ((r>150)&(r>g+15)&(g>b+15)).mean()
for cx,cy,rx,ry,sb,*force in REMOVER:
    m = np.asarray(disc_mask(cx,cy,rx,ry,sb)).astype(float)/255
    best=None
    for dx,dy in (force or [(-2.4,0),(2.4,0),(-2.4,-.6),(2.4,-.6),(-3.2,.4),(3.2,.4)]):
        ox,oy = int(dx*rx), int(dy*ry)
        sh = np.roll(np.roll(a,oy,0),ox,1)   # sh[y,x] = a[y-oy, x-ox]
        y0,y1,x0,x1 = cy-ry-8,cy+ry+8,cx-rx-8,cx+rx+8
        sc = woodness(sh[y0:y1,x0:x1])
        if best is None or sc<best[0]: best=(sc,sh)
    a = a*(1-m[...,None]) + best[1]*m[...,None]

# 2) novas placas fincadas no solo: (x, y_do_solo, raio, nome, datas)
NOVAS = [(95,668,13,'LUNA','2009-2023'),(55,805,18,'MATEO RUIZ','1948-2021'),
         (545,676,14,'ROSA LEÓN','1952-2020'),(612,724,16,'JUAN CASTRO','1939-2022'),
         (935,748,17,'ELENA DÍAZ','1960-2024'),(1010,706,15,'TOMÁS VEGA','1945-2019'),
         (1565,772,20,'CARMEN SOTO','1950-2023'),(1310,770,20,'LUIS MORA','1941-2018'),
         (1395,868,24,'ANA TORRES','1955-2022'),(330,842,23,'PEDRO GIL','1947-2021'),
         (660,840,23,'SOFÍA REYES','1958-2024'),(1655,880,22,'RAÚL PAZ','1944-2020')]
out = Image.fromarray(np.clip(a,0,255).astype('uint8'))
try: FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; ImageFont.truetype(FONT,10)
except OSError: FONT = None
def placa(r, nome, datas):
    S=8; R=r*S; n=2*R+4*S
    img = Image.new('RGBA',(n,n),(0,0,0,0)); d=ImageDraw.Draw(img); c=n//2
    d.ellipse([c-R,c-R,c+R,c+R],fill=(122,84,52,255))                 # casca
    Ri=int(R*0.9); d.ellipse([c-Ri,c-Ri,c+Ri,c+Ri],fill=(214,174,124,255))
    for k in range(1,7):                                               # anéis
        rr=int(Ri*k/7); d.ellipse([c-rr,c-rr,c+rr,c+rr],outline=(196,154,104,255),width=max(1,S//2))
    d.ellipse([c-Ri,c-Ri,c+Ri,c+Ri],outline=(160,115,70,255),width=S)
    f1 = ImageFont.truetype(FONT,int(R*0.26)) if FONT else None
    f2 = ImageFont.truetype(FONT,int(R*0.18)) if FONT else None
    partes = nome.split(' ',1) if len(nome)>9 else [nome]
    linhas=[(p,f1) for p in partes]+[(datas,f2)]
    hs=[d.textbbox((0,0),t,font=f)[3] for t,f in linhas]; y=c-sum(hs)*0.6
    for (t,f),h in zip(linhas,hs):
        w=d.textlength(t,font=f); d.text((c-w/2,y),t,fill=(70,40,20,255),font=f); y+=h*1.25
    img=img.resize((n//S,n//S),Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.5))
    return img
d = ImageDraw.Draw(out)
for x,yg,r,nome,datas in NOVAS:
    h = int(r*0.95)                       # altura da estaca visível
    cy = yg - h - r
    # sombra no solo
    sh = Image.new('L',(W,H),0); ImageDraw.Draw(sh).ellipse([x-r*0.9,yg-r*0.18,x+r*0.9,yg+r*0.18],fill=110)
    out.paste((25,20,10),(0,0),sh.filter(ImageFilter.GaussianBlur(r*0.25)))
    # estaca
    w = max(2,int(r*0.18))
    ImageDraw.Draw(out).rectangle([x-w//2,cy,x+w//2,yg],fill=(78,55,35))
    ImageDraw.Draw(out).line([(x-w//2,cy),(x-w//2,yg)],fill=(110,80,52))
    p = placa(r,nome,datas)
    out.paste(p,(x-p.width//2,cy-p.height//2),p)
out.save('jardim_placas_solo.jpg',quality=92)
