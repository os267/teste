import numpy as np, random, colorsys
from PIL import Image, ImageDraw, ImageFilter
random.seed(3); np.random.seed(3)
src=Image.open('foto_original.jpg').convert('RGB'); W,H=src.size
# path edges (inner = slope side, outer = road side), sampled along t
inner=[(-20,1430),(300,1360),(600,1290),(850,1225),(1030,1150),(1220,1065)]
outer=[(-20,1700),(700,1700),(1000,1600),(1110,1530),(1200,1470),(1230,1450)]
def interp(pts,n=200):
    pts=np.array(pts,float); d=np.r_[0,np.cumsum(np.hypot(*np.diff(pts,axis=0).T))]
    s=np.linspace(0,d[-1],n); return np.c_[np.interp(s,d,pts[:,0]),np.interp(s,d,pts[:,1])]
I=interp(inner); O=interp(outer)
def scale_at(y): return 0.35+0.65*np.clip((y-1050)/550,0,1)  # perspective size factor
# gravel layer
grav=Image.new('RGB',(W,H),(150,145,135)); gd=ImageDraw.Draw(grav)
for _ in range(260000):
    x=random.uniform(0,W); y=random.uniform(1000,H); s=scale_at(y)
    r=random.uniform(1.2,3.2)*s*1.5
    v=random.randint(105,205); tint=random.choice([(0,0,0),(10,6,-4),(-5,-3,2),(14,10,4)])
    c=tuple(int(np.clip(v+t,0,255)) for t in tint)
    nv=random.randint(4,6); ang=sorted(random.uniform(0,6.283) for _ in range(nv))
    gd.polygon([(x+r*random.uniform(.6,1.1)*np.cos(a),y+0.6*r*random.uniform(.6,1.1)*np.sin(a)) for a in ang],fill=c,outline=tuple(max(0,k-45) for k in c))
grav=grav.filter(ImageFilter.GaussianBlur(0.5))
sh=np.random.rand(H//40+1,W//40+1); sh=np.asarray(Image.fromarray((sh*255).astype('uint8')).resize((W,H),Image.BICUBIC)).astype(float)/255
grav=Image.fromarray(np.clip(np.asarray(grav)*(0.85+0.25*sh[...,None]),0,255).astype('uint8'))
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
        col=(158+sh,82+sh,62+sh) if k%2==0 else (148+sh,76+sh,58+sh)
        d.polygon([tuple(q) for q in p],fill=col,outline=(90,55,45))
        # top highlight
        d.line([tuple(seg[0]),tuple(seg[1])],fill=(190,120,95),width=max(1,int(2*s)))
        pos=b; k+=1
edging(I,+1,26)   # slope side
edging(O,-1,75)   # road side (replaces curb)
out.save('mockup.jpg',quality=92)
