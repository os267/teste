import numpy as np, random, colorsys
from PIL import Image, ImageDraw, ImageFilter
random.seed(3); np.random.seed(3)
src=Image.open('foto_original.jpg').convert('RGB'); W,H=src.size
# path edges (inner = slope side, outer = road side), sampled along t
inner=[(-20,1620),(400,1560),(700,1480),(900,1400),(1060,1310),(1220,1215)]
outer=[(-20,1760),(700,1700),(1000,1600),(1110,1530),(1200,1470),(1230,1450)]
def interp(pts,n=200):
    pts=np.array(pts,float); d=np.r_[0,np.cumsum(np.hypot(*np.diff(pts,axis=0).T))]
    s=np.linspace(0,d[-1],n); return np.c_[np.interp(s,d,pts[:,0]),np.interp(s,d,pts[:,1])]
I=interp(inner); O=interp(outer)
def scale_at(y): return 0.35+0.65*np.clip((y-1050)/550,0,1)  # perspective size factor
# gravel layer: textura real do pedrisco branco da imagem de referência,
# com as sombras removidas e escalada conforme a perspectiva
ref=Image.open('referencia_pedrisco_branco.jpg').convert('RGB').crop((930,830,1530,1024))
t=np.asarray(ref).astype(float)
lum=np.asarray(ref.convert('L').filter(ImageFilter.GaussianBlur(18))).astype(float)
t=np.clip(212+(t/lum[...,None]*212-212)*0.75,0,255)
t=np.concatenate([t,t[:,::-1]],1); t=np.concatenate([t,t[::-1]],0)  # espelha p/ ficar contínua
th,tw=t.shape[:2]
ys,xs=np.mgrid[0:H,0:W].astype(float)
k=1/(scale_at(ys)*0.6)
u=(xs*k).astype(int)%tw; v=(ys*k).astype(int)%th
grav=Image.fromarray(t[v,u].astype('uint8')).filter(ImageFilter.GaussianBlur(0.7))
mask=Image.new('L',(W,H),0); md=ImageDraw.Draw(mask)
poly=[tuple(p) for p in I]+[tuple(p) for p in O[::-1]]
md.polygon(poly,fill=255)
out=src.copy(); out.paste(grav,(0,0),mask.filter(ImageFilter.GaussianBlur(1.2)))
d=ImageDraw.Draw(out)
# paver edging along both edges: blocks 20x10cm laid lengthwise
def edging(E, inward, base_w):
    # E: edge polyline; inward: +1 toward other edge
    L=np.r_[0,np.cumsum(np.hypot(*np.diff(E,axis=0).T))]
    pos=0; k=0
    while pos<L[-1]-1:
        y=np.interp(pos,L,E[:,1]); s=scale_at(y); blen=70*s; bw=base_w*s
        a=pos; b=min(pos+blen,L[-1])
        seg=[np.array([np.interp(t,L,E[:,0]),np.interp(t,L,E[:,1])]) for t in (a,b)]
        # normal pointing toward path interior: approximate using direction (0,inward)
        dvec=seg[1]-seg[0]; n=np.array([-dvec[1],dvec[0]]); n/= (np.linalg.norm(n)+1e-9)
        if n[1]*inward<0: n=-n
        p=[seg[0],seg[1],seg[1]+n*bw,seg[0]+n*bw]
        sh=random.randint(-10,10)
        col=(188+sh,188+sh,183+sh) if k%2==0 else (178+sh,178+sh,173+sh)
        d.polygon([tuple(q) for q in p],fill=col,outline=(125,125,120))
        # top highlight
        d.line([tuple(seg[0]),tuple(seg[1])],fill=(222,222,216),width=max(1,int(2*s)))
        pos=b; k+=1
edging(I,+1,22)   # slope side
edging(O,-1,40)   # road side (replaces curb)
out.save('simulacao.jpg',quality=92)
