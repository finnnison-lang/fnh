# v3 generator: template + copy.json + media lists -> site/index.html
import json, html, re
ROOT="/Volumes/Macintosh HD II/AI/FNH WEB"; e=html.escape
C=json.load(open(f"{ROOT}/scripts/copy.json")); man=json.load(open(f"{ROOT}/scripts/images-manifest.json"))
dims={p["slug"]:(p["w"],p["h"]) for p in man["photo"]}; ddims={d["slug"]:(d["w"],d["h"]) for d in man["design"]}
def T(key, tag="span", cls=""): de,en=C[key]; c=f' class="{cls}"' if cls else ""; return f'<{tag}{c} data-en="{e(en)}">{e(de)}</{tag}>'
# featured tiles: slug, vertical, title, one-liner DE/EN, meta DE/EN
tiles=[
 ("race",0,"Nürburgring 24h","Nachtrennen im FNH-Anzug","Night race in the FNH suit","AI Film · 2026","AI film · 2026"),
 ("kuppelkino",1,"Kuppelkino Stuttgart","3,4 Millionen Aufrufe","3.4 million views","AI Film · 2026","AI film · 2026"),
 ("odyssai",0,"OdyssAI 2028","Abschlussfilm, acht Minuten","Graduation film, eight minutes","Film · 2026","Film · 2026"),
 ("redbull",1,"Oma und die Red-Bull-Wand","4,3 Millionen Aufrufe","4.3 million views","AI Film · 2026","AI film · 2026"),
 ("iceland",0,"Island, Feuer und Eis","Drohne, R5 und ein Vulkan","Drone, R5 and a volcano","Film · 2022","Film · 2022"),
 ("husky",1,"Husky, Wasserpistole","737.000 Aufrufe","737,000 views","AI Film · 2026","AI film · 2026"),
 ("cymatics",0,"Cymatics","Where sound meets vision","Where sound meets vision","Kurzfilm · 2025","Short film · 2025"),
 ("singapur",1,"Studio Singapur","1,4 Millionen Aufrufe","1.4 million views","AI Film · 2026","AI film · 2026"),
]
def tile(i,t):
    s,v,title,dde,den,mde,men=t
    return f'''<figure class="tile {'tile--v' if v else 'tile--h'} t{i+1}" data-anim data-open-video="assets/work/{s}.mp4" data-poster="assets/work/{s}.jpg" data-vertical="{v}" data-title="{e(title)}" data-cursor="PLAY" data-cursor-en="PLAY" data-speed="{[1.06,0.9,1.02,0.86,1.08,0.92,1.04,0.88][i]}" tabindex="0" role="button">
  <div class="tile__media"><img src="assets/work/{s}.jpg" alt="{e(title)}" loading="lazy" width="{720 if v else 1280}" height="{1280 if v else 720}"><video muted loop playsinline preload="none"><source data-src="assets/work/{s}-loop.mp4" type="video/mp4"></video></div>
  <figcaption class="tile__cap"><span class="lbl">{i+1:02d}</span><span><b>{e(title)}</b><br><span data-en="{e(den)}">{e(dde)}</span></span><span class="mono" data-en="{e(men)}">{e(mde)}</span></figcaption>
</figure>'''
G1="\n".join(tile(i,t) for i,t in enumerate(tiles[:4])); G2="\n".join(tile(i+4,t) for i,t in enumerate(tiles[4:]))
rows=[
 ("race","assets/work/race.mp4","assets/work/race.jpg",0,"ai","2026","Nürburgring 24h","Nachtrennen im FNH-Anzug, drei Teile","Night race in the FNH suit, three parts"),
 ("odyssai","assets/work/odyssai.mp4","assets/work/odyssai.jpg",0,"film","2026","OdyssAI 2028","Abschlussfilm, Trailer","Graduation film, trailer"),
 ("iceland","assets/work/iceland.mp4","assets/work/iceland.jpg",0,"film","2022","Island, Feuer und Eis","Drohne, R5 und ein Vulkan","Drone, R5 and a volcano"),
 ("redbull","assets/work/redbull.mp4","assets/work/redbull.jpg",1,"ai","2026","Oma und die Red-Bull-Wand","CCTV, 4,3 Millionen Aufrufe","CCTV, 4.3 million views"),
 ("kuppelkino","assets/work/kuppelkino.mp4","assets/work/kuppelkino.jpg",1,"ai","2026","Kuppelkino Stuttgart","Die Leinwand splittert, 3,4 Millionen","The screen shatters, 3.4 million"),
 ("singapur","assets/work/singapur.mp4","assets/work/singapur.jpg",1,"ai","2026","Studio Singapur","Miniatur-Marina-Bay, 1,4 Millionen","Miniature Marina Bay, 1.4 million"),
 ("cymatics","assets/work/cymatics.mp4","assets/work/cymatics.jpg",0,"film","2025","Cymatics","Where sound meets vision","Where sound meets vision"),
 ("husky","assets/work/husky.mp4","assets/work/husky.jpg",1,"ai","2026","Husky, Wasserpistole","Der vierte Welpe macht eine Oper daraus","The fourth puppy turns it into an opera"),
 ("stuttgart-hbf-flut","assets/video/stuttgart-hbf-flut.mp4","assets/video/stuttgart-hbf-flut.jpg",1,"ai","2026","Studio Stuttgart Hbf","Miniatur, Gleise, Flut","Miniature, tracks, flood"),
 ("flughafen","assets/work/flughafen.mp4","assets/work/flughafen.jpg",1,"ai","2026","Studio Flughafen","Antonov, Meteore, Megafon","Antonov, meteors, megaphone"),
 ("katze-menschenkette","assets/video/katze-menschenkette.mp4","assets/video/katze-menschenkette.jpg",1,"ai","2026","Katze, Menschenkette","Rettung vom Bäckereifenster","Rescue from the bakery window"),
 ("falltraum","assets/work/falltraum.mp4","assets/work/falltraum.jpg",1,"ai","2026","Falltraum Fernsehturm","Vom Turm ins Bett","From the tower into bed"),
 ("a8","assets/work/a8.mp4","assets/work/a8.jpg",1,"ai","2026","A8 Notlandung","Real × KI unter dem Bosch-Parkhaus","Real × AI under the Bosch car park"),
 ("weltrand","assets/video/weltrand.mp4","assets/video/weltrand.jpg",1,"ai","2026","Flugzeugträger am Weltrand","Wasser, das aufhört","Water that just ends"),
 ("dispatch","assets/work/dispatch.mp4","assets/work/dispatch.jpg",1,"ai","2026","Dispatch 001","Der Regiestuhl im Sandsturm","The director's chair in the sandstorm"),
 ("reykjavik-vulkan","assets/video/reykjavik-vulkan.mp4","assets/video/reykjavik-vulkan.jpg",1,"ai","2026","Studio Reykjavík","Vulkan über der Miniaturstadt","Volcano over the miniature city"),
 ("tokyo-tsunami","assets/video/tokyo-tsunami.mp4","assets/video/tokyo-tsunami.jpg",1,"ai","2026","Studio Tokyo","Tsunami, Tower, Crew","Tsunami, tower, crew"),
 ("gt3rs-regenrig","assets/video/gt3rs-regenrig.mp4","assets/video/gt3rs-regenrig.jpg",1,"ai","2026","GT3 RS, Regen-Rig","Greenscreen, RT XX 818","Green screen, RT XX 818"),
 ("zug-lawine-fpv","assets/video/zug-lawine-fpv.mp4","assets/video/zug-lawine-fpv.jpg",1,"ai","2026","Zug vs. Lawine","FPV durch den Kunstschnee","FPV through the fake snow"),
 ("katze-slapfight","assets/video/katze-slapfight.mp4","assets/video/katze-slapfight.jpg",1,"ai","2026","Katze, Slapfight","Katze gegen Strongman","Cat versus strongman"),
 ("kakadu","assets/video/kakadu.mp4","assets/video/kakadu.jpg",1,"ai","2026","Kakadu vom Schrank","Fünfzehn Sekunden Verhandlung","Fifteen seconds of negotiation"),
 ("pesto-pyramide","assets/video/pesto-pyramide.mp4","assets/video/pesto-pyramide.jpg",1,"ai","2026","Pesto-Pyramide","CCTV im Supermarkt","CCTV in the supermarket"),
 ("dubai-tsunami","assets/video/dubai-tsunami.mp4","assets/video/dubai-tsunami.jpg",1,"ai","2026","Studio Dubai","Tsunami trifft Burj","Tsunami meets the Burj"),
 ("paris-flut","assets/video/paris-flut.mp4","assets/video/paris-flut.jpg",1,"ai","2026","Studio Paris","Flut unter dem Eiffelturm","Flood under the Eiffel Tower"),
 ("london-sturmflut","assets/video/london-sturmflut.mp4","assets/video/london-sturmflut.jpg",1,"ai","2026","Studio London","Sturmflut an der Themse","Storm surge on the Thames"),
 ("wolke-fangen","assets/video/wolke-fangen.mp4","assets/video/wolke-fangen.jpg",1,"ai","2026","Wolke fangen","Schlossplatz, ein Beutel, eine Wolke","Schlossplatz, a bag, a cloud"),
 ("angkor-pov","assets/video/angkor-pov.mp4","assets/video/angkor-pov.jpg",1,"ai","2026","Angkor POV","Dschungel, Regen, Statue","Jungle, rain, statue"),
 ("bosch-meteorit","assets/video/bosch-meteorit.mp4","assets/video/bosch-meteorit.jpg",1,"ai","2026","Bosch-Parkhaus, Meteorit","Einschlag über der A8","Impact over the A8"),
 ("wuenschewagen","assets/film/wuenschewagen.mp4","assets/film/wuenschewagen.jpg",0,"film","2024","Der Wünschewagen","Dokumentarfilm, 4:07","Documentary, 4:07"),
 ("die-bank","assets/film/die-bank.mp4","assets/film/die-bank.jpg",0,"film","2024","Die Bank","Kurzfilm, komplett auf dem Smartphone","Short film, shot entirely on a phone"),
 ("basketball","assets/film/basketball.mp4","assets/film/basketball.jpg",0,"film","2026","Basketball","3D-Tracking und Compositing","3D tracking and compositing"),
]
ROWS="\n".join(f'''<div class="row" data-anim data-cat="{cat}" data-open-video="{src}" data-poster="{poster}" data-vertical="{v}" data-title="{e(t)}" data-cursor="PLAY" data-cursor-en="PLAY" tabindex="0" role="button"><span class="row__num">{i+1:02d}</span><span class="row__title">{e(t)}</span><span class="row__desc" data-en="{e(den)}">{e(dde)}</span><span class="row__cat" data-en="{'AI film' if cat=='ai' else 'Film'}">{'AI Film' if cat=='ai' else 'Film'}</span><span class="row__year">{y}</span></div>''' for i,(s,src,poster,v,cat,y,t,dde,den) in enumerate(rows))
photos=[("iceland-lava-01","Island, 2021","Iceland, 2021"),("rimlight-01","Rim Light, Studio","Rim light, studio"),("subway-orange","U-Bahn, Stuttgart","Subway, Stuttgart"),("iceland-plane","Island, 2021","Iceland, 2021"),("projection-01","Projektion, Studio","Projection, studio"),("seychelles-bay","Seychellen, 2021, Mavic 3","Seychelles, 2021, Mavic 3"),("aurora","Island, 2022","Iceland, 2022"),("studio-portrait","Nachtporträt","Night portrait"),("fashion-02","Fashion, Werkschau 2025","Fashion, Werkschau 2025"),("vestrahorn","Island, 2022","Iceland, 2022"),("neon-02","Neon, Prag 2020","Neon, Prague 2020"),("iceland-road","Island, 2021, Mavic 3","Iceland, 2021, Mavic 3")]
speeds=[1.05,0.9,1.08,0.95,1.1,0.88,1.03,0.92,1.06,0.9,1.04,0.94]
PHOTOS="\n".join(f'''<figure class="pic p{i+1}" data-anim data-open-image="assets/photo/{s}.jpg" data-title="{e(cde)}" data-title-en="{e(cen)}" data-cursor="ÖFFNEN" data-cursor-en="OPEN" data-speed="{speeds[i]}" tabindex="0" role="button"><img src="assets/photo/{s}-t.jpg" alt="{e(cde)}" data-en-alt="{e(cen)}" loading="lazy" width="{dims[s][0]}" height="{dims[s][1]}"><figcaption><span data-en="{e(cen)}">{e(cde)}</span><span>{i+1:02d}</span></figcaption></figure>''' for i,(s,cde,cen) in enumerate(photos))
design=[("ayvo","Ayvo","Packaging","Packaging"),("lazi-kampagne","LAZI Akademie","Kampagne","Campaign"),("cymatics","Cymatics","Plakat","Poster"),("freshy","Freshy","Packaging","Packaging"),("last-exit","Last Exit","Plakat","Poster")]
DESIGN="\n".join(f'''<figure class="dcard" data-open-image="assets/design/{s}.jpg" data-title="{e(t)}" data-cursor="ÖFFNEN" data-cursor-en="OPEN" tabindex="0" role="button" data-reveal><img src="assets/design/{s}-t.jpg" alt="{e(t)}, {e(kde)}" data-en-alt="{e(t)}, {e(ken)}" loading="lazy" width="{ddims[s][0]}" height="{ddims[s][1]}"><figcaption><b>{e(t)}</b><span data-en="{e(ken)}">{e(kde)}</span></figcaption></figure>''' for s,t,kde,ken in design)
tpl=open(f"{ROOT}/scripts/index.template.html",encoding="utf-8").read()
tpl=re.sub(r"\{\{C:([a-z0-9_]+)\|b\}\}", lambda m: T(m.group(1), "b"), tpl)
tpl=re.sub(r"\{\{C:([a-z0-9_]+)\}\}", lambda m: T(m.group(1)), tpl)
tpl=re.sub(r"\{\{CDE:([a-z0-9_]+)\}\}", lambda m: e(C[m.group(1)][0]), tpl)
tpl=re.sub(r"\{\{CEN:([a-z0-9_]+)\}\}", lambda m: e(C[m.group(1)][1]), tpl)
logo=open(f"{ROOT}/site/assets/img/fnh-logo.svg").read().replace('<svg ','<svg focusable="false" ',1)
out=tpl.replace("{{LOGO}}",logo).replace("{{TILES1}}",G1).replace("{{TILES2}}",G2).replace("{{ROWS}}",ROWS).replace("{{NROWS}}",str(len(rows))).replace("{{PHOTOS}}",PHOTOS).replace("{{DESIGN}}",DESIGN)
open(f"{ROOT}/site/index.html","w",encoding="utf-8").write(out); print("index.html",len(out),"bytes")
