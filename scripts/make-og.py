# Generates the Open Graph image and favicons with the site typography.
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT="/Volumes/Macintosh HD II/AI/FNH WEB"; A=f"{ROOT}/site/assets"; FONTS=f"{ROOT}/tools/fonts"
BG=(6,8,13); INK=(238,241,246); AMBER=(255,160,40); MUTED=(138,147,166)
def syne(size):
    f=ImageFont.truetype(f"{FONTS}/Syne.ttf", size)
    try: f.set_variation_by_axes([800])
    except Exception: pass
    return f
mono=lambda s: ImageFont.truetype(f"{FONTS}/SpaceMono-Regular.ttf", s)
def grot(s):
    f=ImageFont.truetype(f"{FONTS}/SpaceGrotesk.ttf", s)
    try: f.set_variation_by_axes([500])
    except Exception: pass
    return f
# --- OG 1200x630
W,H=1200,630; im=Image.new("RGB",(W,H),BG)
glow=Image.new("RGB",(W,H),BG); g=ImageDraw.Draw(glow); g.ellipse([700,-200,1500,500],fill=(40,28,14)); glow=glow.filter(ImageFilter.GaussianBlur(160)); im=Image.blend(im,glow,0.9)
d=ImageDraw.Draw(im)
d.text((70,62),"FINN HAFEMANN  ·  STUTTGART",font=mono(22),fill=AMBER)
f=syne(200); d.text((58,120),"FNH",font=f,fill=INK); bb=d.textbbox((58,100),"FNH",font=f); d.rectangle([bb[2]+18,bb[3]-52,bb[2]+62,bb[3]-8],fill=AMBER)
d.text((70,410),"Film · Foto · AI · Design",font=grot(44),fill=INK)
d.text((70,478),"Echte Kamera trifft generative KI. Welten, die es nicht geben dürfte.",font=grot(24),fill=MUTED)
d.line([(70,560),(560,560)],fill=(40,46,60),width=2); d.text((70,572),"fnh · finnison.com",font=mono(18),fill=MUTED)
x=790
for slug in ["stuttgart-hbf-flut","gt3rs-regenrig","tokyo-tsunami"]:
    p=Image.open(f"{A}/video/{slug}.jpg").convert("RGB").resize((150,267)); mask=Image.new("L",p.size,0); ImageDraw.Draw(mask).rounded_rectangle([0,0,149,266],radius=12,fill=255)
    im.paste(p,(x,150),mask); x+=166
p=Image.open(f"{A}/img/finn-portrait.jpg").convert("RGB"); p=p.crop((0,0,p.width,int(p.width*1.78))).resize((150,267)); mask=Image.new("L",p.size,0); ImageDraw.Draw(mask).rounded_rectangle([0,0,149,266],radius=12,fill=255); im.paste(p,(x-166*3+0,430),mask) if False else None
im.save(f"{A}/img/og.jpg","JPEG",quality=88); print("og ok")
# --- favicons
def icon(size):
    ic=Image.new("RGBA",(size,size),(0,0,0,0)); dd=ImageDraw.Draw(ic); r=int(size*0.22); dd.rounded_rectangle([0,0,size-1,size-1],radius=r,fill=BG+(255,))
    fs=int(size*0.78); ff=syne(fs); bb=dd.textbbox((0,0),"F",font=ff); tw,th=bb[2]-bb[0],bb[3]-bb[1]; dd.text((size*0.14-bb[0],(size-th)/2-bb[1]-size*0.02),"F",font=ff,fill=INK)
    ds=int(size*0.2); dd.rounded_rectangle([size-ds-int(size*0.12),size-ds-int(size*0.14),size-int(size*0.12),size-int(size*0.14)],radius=int(ds*0.2),fill=AMBER+(255,)); return ic
for s,name in [(512,"icon-512.png"),(192,"icon-192.png"),(180,"apple-touch-icon.png"),(32,"favicon-32.png")]: icon(s).save(f"{ROOT}/site/{name}")
icon(64).save(f"{ROOT}/site/favicon.ico",sizes=[(16,16),(32,32),(48,48),(64,64)]); print("icons ok")
