# v2 generator: assembles site/index.html from the template plus chapters, index rows, photos and design.
import json, html
ROOT="/Volumes/Macintosh HD II/AI/FNH WEB"; e=html.escape
man=json.load(open(f"{ROOT}/scripts/images-manifest.json")); dims={p["slug"]:(p["w"],p["h"]) for p in man["photo"]}; ddims={d["slug"]:(d["w"],d["h"]) for d in man["design"]}
# ---- chapters (slug, vertical, title DE, title EN, meta DE, meta EN, desc DE, desc EN)
chapters=[
 ("race",0,"Nürburgring 24h","Nürburgring 24h","AI Film · 2026 · 1:30","AI film · 2026 · 1:30","Ein Fahrer im FNH-Anzug, Boxengasse bei Nacht, Flutlicht, Regen und die Nordschleife. Drei Teile, komplett generiert.","A driver in the FNH suit, pit lane at night, floodlights, rain and the Nordschleife. Three parts, fully generated."),
 ("odyssai",0,"OdyssAI <span class=\"serif\">2028</span>","OdyssAI <span class=\"serif\">2028</span>","Abschlussfilm · 2026 · 8:00","Graduation film · 2026 · 8:00","Ein Abteilungsleiter baut die KI, die ihn ersetzt. Acht Minuten, fast vollständig generiert, geschnitten wie ein Kinofilm. Hier der Trailer.","A department head builds the AI that replaces him. Eight minutes, almost entirely generated, cut like a feature. Trailer here."),
 ("iceland",0,"Island, <span class=\"serif\">Feuer und Eis</span>","Iceland, <span class=\"serif\">Fire and Ice</span>","Film · 2022 · 3:21","Film · 2022 · 3:21","Lava, Gletscher, Nordlicht. Gedreht mit Canon R5, Mavic 3 und FPV, geschnitten von Hand.","Lava, glaciers, aurora. Shot on Canon R5, Mavic 3 and FPV, cut by hand."),
 ("kuppelkino",1,"Kuppelkino <span class=\"serif\">Stuttgart</span>","Dome cinema <span class=\"serif\">Stuttgart</span>","AI Film · 2026 · 0:11","AI film · 2026 · 0:11","Die Welle zerlegt den Hauptbahnhof, der Turm kippt, die Leinwand splittert. 3,4 Millionen Aufrufe.","The wave takes the central station apart, the tower tips, the screen shatters. 3.4 million views."),
 ("redbull",1,"Oma und die <span class=\"serif\">Red-Bull-Wand</span>","Grandma and the <span class=\"serif\">Red Bull wall</span>","AI Film · 2026 · 0:15","AI film · 2026 · 0:15","Eine Überwachungskamera, ein Einkaufswagen, eine Wand aus Dosen. 4,3 Millionen Aufrufe.","A security camera, a shopping cart, a wall of cans. 4.3 million views."),
 ("cymatics",0,"Cymatics","Cymatics","Kurzfilm · 2025 · 4:33","Short film · 2025 · 4:33","Where sound meets vision. Wasser, Sand und Klang, gefilmt statt gerendert.","Where sound meets vision. Water, sand and sound, filmed rather than rendered."),
 ("singapur",1,"Studio <span class=\"serif\">Singapur</span>","Studio <span class=\"serif\">Singapore</span>","AI Film · 2026 · 0:12","AI film · 2026 · 0:12","Miniatur-Marina-Bay, FNH-Crew von hinten, Einschlag. 1,4 Millionen Aufrufe.","Miniature Marina Bay, FNH crew from behind, impact. 1.4 million views."),
 ("husky",1,"Husky, <span class=\"serif\">Wasserpistole</span>","Husky, <span class=\"serif\">water pistol</span>","AI Film · 2026 · 0:12","AI film · 2026 · 0:12","Vier Welpen, drei fallen brav um, der vierte macht eine Oper daraus. 737.000 Aufrufe.","Four puppies, three fall over obediently, the fourth turns it into an opera. 737,000 views."),
]
def plain(s): import re; return re.sub(r"<[^>]+>","",s)
CH=[]
for i,(s,v,tde,ten,mde,men,dde,den) in enumerate(chapters):
    media=(f'<div class="ch__bg" style="background-image:url(assets/work/{s}.jpg)"></div><div class="ch__frame"><img src="assets/work/{s}.jpg" alt="" width="720" height="1280" loading="lazy"><video muted loop playsinline preload="none" poster="assets/work/{s}.jpg"><source data-src="assets/work/{s}-loop.mp4" type="video/mp4"></video></div>' if v else
           f'<img src="assets/work/{s}.jpg" alt="" width="1280" height="720" loading="{"eager" if i==0 else "lazy"}"><video muted loop playsinline preload="none" poster="assets/work/{s}.jpg"><source data-src="assets/work/{s}-loop.mp4" type="video/mp4"></video>')
    CH.append(f'''<article class="ch {'ch--v' if v else 'ch--h'}" data-title="{e(plain(tde))}" data-title-en="{e(plain(ten))}">
  <div class="ch__media">{media}</div><div class="ch__shade"></div>
  <div class="ch__text">
    <div class="label"><span>( {i+1:02d} / {len(chapters):02d} )</span><span data-en="{e(men)}">{e(mde)}</span></div>
    <h2 class="ch__title" data-en="{e(ten)}">{tde}</h2>
    <p class="ch__desc" data-en="{e(den)}">{e(dde)}</p>
    <button class="ch__link" data-open-video="assets/work/{s}.mp4" data-poster="assets/work/{s}.jpg" data-vertical="{v}" data-title="{e(plain(tde))}" data-title-en="{e(plain(ten))}" data-cursor="PLAY" data-cursor-en="PLAY"><span data-en="Watch with sound">Mit Ton ansehen</span></button>
  </div>
</article>''')
CHAPTERS="\n".join(CH); BARS="".join('<i></i>' for _ in chapters)
# ---- index rows (slug, src, poster, vertical, cat, year, title, one-liner DE, EN)
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
ROWS="\n".join(f'''<div class="row" data-cat="{cat}" data-open-video="{src}" data-poster="{poster}" data-vertical="{v}" data-title="{e(t)}" data-cursor="PLAY" data-cursor-en="PLAY" tabindex="0" role="button">
  <span class="row__num">{i+1:02d}</span><span class="row__title">{e(t)}</span><span class="row__desc" data-en="{e(den)}">{e(dde)}</span><span class="row__cat" data-en="{'AI film' if cat=='ai' else 'Film'}">{'AI Film' if cat=='ai' else 'Film'}</span><span class="row__year">{y}</span>
</div>''' for i,(s,src,poster,v,cat,y,t,dde,den) in enumerate(rows))
# ---- photos (slug, caption DE, EN)
photos=[("iceland-lava-01","Island, 2021","Iceland, 2021"),("rimlight-01","Studio","Studio"),("subway-orange","U-Bahn","Subway"),("iceland-plane","Island, 2021","Iceland, 2021"),("projection-01","Projektion","Projection"),("seychelles-bay","Seychellen, 2021","Seychelles, 2021"),("portrait-tattoo","Porträt","Portrait"),("aurora","Island, 2022","Iceland, 2022"),("fashion-02","Werkschau, 2025","Werkschau, 2025"),("iceland-road","Island, 2021","Iceland, 2021"),("neon-02","Neon, 2020","Neon, 2020"),("vestrahorn","Island, 2022","Iceland, 2022"),("gym","Gym","Gym"),("seychelles-rocks","Seychellen, 2021","Seychelles, 2021"),("blitzlicht","Studio","Studio"),("iceland-waterfall","Island, 2021","Iceland, 2021"),("street-light","Nacht","Night"),("studio-01","Studio","Studio")]
PH=[]
for i,(s,cde,cen) in enumerate(photos):
    w,h=dims[s]; cls="pic--l" if w>=h else "pic--p"
    PH.append(f'''<figure class="pic {cls}" data-open-image="assets/photo/{s}.jpg" data-title="{e(cde)}" data-title-en="{e(cen)}" data-cursor="ÖFFNEN" data-cursor-en="OPEN" tabindex="0" role="button"><img src="assets/photo/{s}-t.jpg" alt="{e(cde)}" data-en-alt="{e(cen)}" loading="lazy" width="{w}" height="{h}"><figcaption><span data-en="{e(cen)}">{e(cde)}</span><span>{i+1:02d}</span></figcaption></figure>''')
PHOTOS="\n".join(PH)
design=[("ayvo","Ayvo","Packaging","Packaging"),("lazi-kampagne","LAZI Akademie","Kampagne","Campaign"),("cymatics","Cymatics","Plakat","Poster"),("finnison-ci","FINNISON","Corporate Design","Corporate design"),("freshy","Freshy","Packaging","Packaging"),("last-exit","Last Exit","Plakat-Redesign","Poster redesign"),("buchcover","Stimmen im Kopf","Buchcover","Book cover"),("nature-one","Nature One","Plakat, Konzept","Poster, concept"),("porsche","GT3 RS","Composite","Composite"),("wwf","WWF","Kampagne, Konzept","Campaign, concept")]
DESIGN="\n".join(f'''<figure class="dcard{' dcard--wide' if ddims[s][0]>ddims[s][1]*1.15 else ''}" data-open-image="assets/design/{s}.jpg" data-title="{e(t)}" data-cursor="ÖFFNEN" data-cursor-en="OPEN" tabindex="0" role="button" data-reveal><img src="assets/design/{s}-t.jpg" alt="{e(t)}, {e(kde)}" data-en-alt="{e(t)}, {e(ken)}" loading="lazy" width="{ddims[s][0]}" height="{ddims[s][1]}"><figcaption><b>{e(t)}</b><span data-en="{e(ken)}">{e(kde)}</span></figcaption></figure>''' for s,t,kde,ken in design)
tpl=open(f"{ROOT}/scripts/index.template.html",encoding="utf-8").read()
out=tpl.replace("{{CHAPTERS}}",CHAPTERS).replace("{{BARS}}",BARS).replace("{{ROWS}}",ROWS).replace("{{PHOTOS}}",PHOTOS).replace("{{DESIGN}}",DESIGN).replace("{{NROWS}}",str(len(rows)))
open(f"{ROOT}/site/index.html","w",encoding="utf-8").write(out); print("index.html",len(out),"bytes")
