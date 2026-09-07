# Assembles site/index.html from the template plus the curated media lists.
import json, html
ROOT="/Volumes/Macintosh HD II/AI/FNH WEB"
man=json.load(open(f"{ROOT}/scripts/images-manifest.json"))
dims={p["slug"]:(p["w"],p["h"]) for p in man["photo"]}; ddims={d["slug"]:(d["w"],d["h"]) for d in man["design"]}
e=html.escape

# ---- reel wall (slug, DE, EN, seconds)
clips_meta={
 "stuttgart-hbf-flut":("Stuttgart Hbf, Flut","Stuttgart Central, flood"),"tokyo-tsunami":("Tokyo, Tsunami","Tokyo, tsunami"),
 "reykjavik-vulkan":("Reykjavík, Vulkan","Reykjavík, volcano"),"gt3rs-regenrig":("GT3 RS, Regen-Rig","GT3 RS, rain rig"),
 "gt3rs-drift":("GT3 RS, Drift","GT3 RS, drift"),"weltrand":("Flugzeugträger am Weltrand","Carrier at the edge of the world"),
 "wolke-fangen":("Wolke fangen, Schlossplatz","Catching a cloud, Schlossplatz"),"dubai-tsunami":("Dubai, Tsunami","Dubai, tsunami"),
 "achalm-ausbruch":("Achalm, Ausbruch","Achalm, eruption"),"zug-lawine-fpv":("Zug vs. Lawine, FPV","Train vs. avalanche, FPV"),
 "zug-lawine-set":("Zug vs. Lawine, am Set","Train vs. avalanche, on set"),"angkor-pov":("Angkor, Dschungel-POV","Angkor, jungle POV"),
 "paris-flut":("Paris, Flut","Paris, flood"),"bosch-meteorit":("Bosch-Parkhaus, Meteorit","Bosch car park, meteorite"),
 "london-sturmflut":("London, Sturmflut","London, storm surge"),"husky-wasserpistole":("Husky, Wasserpistole","Husky, water pistol"),
 "kakadu":("Kakadu vom Schrank","Cockatoo off the cupboard"),"katze-slapfight":("Katze, Slapfight","Cat slap fight"),
 "pesto-pyramide":("Pesto-Pyramide, CCTV","Pesto pyramid, CCTV"),
}
durs={l.split("\t")[0]:float(l.split("\t")[1]) for l in open(f"{ROOT}/scripts/clips-manifest.txt") if l.strip()}
cols=[["stuttgart-hbf-flut","husky-wasserpistole","gt3rs-regenrig","wolke-fangen","dubai-tsunami","kakadu","angkor-pov"],
      ["tokyo-tsunami","katze-slapfight","zug-lawine-fpv","reykjavik-vulkan","bosch-meteorit","pesto-pyramide"],
      ["weltrand","achalm-ausbruch","paris-flut","gt3rs-drift","london-sturmflut","zug-lawine-set"]]
wall=[]
for col in cols:
    items=[]
    for s in col:
        de,en=clips_meta[s]; d=durs[s]
        items.append(f'''<figure class="clip" data-src="assets/video/{s}.mp4" data-poster="assets/video/{s}.jpg" data-title="{e(de)}" data-title-en="{e(en)}" data-cursor="PLAY" tabindex="0" role="button">
  <img src="assets/video/{s}.jpg" alt="" loading="lazy" width="540" height="960">
  <video muted loop playsinline preload="none" poster="assets/video/{s}.jpg"><source src="assets/video/{s}.mp4" type="video/mp4"></video>
  <span class="clip__play" aria-hidden="true"></span>
  <figcaption class="clip__cap"><span data-en="{e(en)}">{e(de)}</span><small>{d:.0f} s</small></figcaption>
</figure>''')
    wall.append('<div class="wall__col">\n'+"\n".join(items)+'\n</div>')
WALL="\n".join(wall)

# ---- films
films=[
 ("wuenschewagen","Der Wünschewagen","Dokumentarfilm · 2024 · 4:07","Documentary · 2024 · 4:07",
  "Ein Film über den Wünschewagen, der schwerkranken Menschen einen letzten Wunsch erfüllt. Interviews, Fahrt, Stille.",
  "A film about the Wünschewagen, a van that grants seriously ill people one last wish. Interviews, the road, silence."),
 ("die-bank","Die Bank","Kurzfilm, Smartphone · 2024 · 1:36","Short film, smartphone · 2024 · 1:36",
  "Komplett auf dem Smartphone gedreht. Ein Mann, ein Wald, eine Bank.","Shot entirely on a smartphone. A man, a forest, a bench."),
 ("werbevideo","Silhouetten","Werbefilm, Studio · 2023 · 1:11","Commercial study, studio · 2023 · 1:11",
  "Gegenlicht, Wasser und ein Hund. Eine Studioarbeit über Umrisse statt Details.","Backlight, water and a dog. A studio piece about outlines instead of detail."),
 ("basketball","Basketball","3D-Tracking & Compositing · 2026 · 0:13","3D tracking & compositing · 2026 · 0:13",
  "Kamera-Tracking in After Effects, Typo im Raum verankert, gerendert auf echtes Footage.","Camera tracking in After Effects, type anchored in space, rendered onto real footage."),
 ("parallax","2.5D","Parallax-Animation · 2024 · 0:05","Parallax animation · 2024 · 0:05",
  "Ein Foto, in Ebenen zerlegt und wieder in Bewegung gesetzt.","One photo, cut into layers and set back in motion."),
]
FILMS="\n".join(f'''<article class="film-row" data-src="assets/film/{s}.mp4" data-poster="assets/film/{s}.jpg" data-title="{e(t)}" data-cursor="PLAY" data-cursor-en="PLAY" tabindex="0" role="button">
  <div class="film-row__text" data-reveal>
    <div class="film-row__num">0{i+1}</div>
    <h3 class="film-row__title">{e(t)}</h3>
    <div class="film-row__meta" data-en="{e(men)}">{e(mde)}</div>
    <p class="film-row__desc" data-en="{e(den)}">{e(dde)}</p>
  </div>
  <div class="film-row__media" data-filmreveal>
    <img src="assets/film/{s}.jpg" alt="" loading="lazy" width="1280" height="720">
    <video muted loop playsinline preload="none"><source src="assets/film/{s}-preview.mp4" type="video/mp4"></video>
    <span class="film-row__btn" data-en="Play with sound">Mit Ton abspielen</span>
  </div>
</article>''' for i,(s,t,mde,men,dde,den) in enumerate(films))

# ---- photos
cats={"portrait":("Porträt","Portrait"),"studio":("Studio","Studio"),"travel":("Reise","Travel"),"aerial":("Luftbild","Aerial"),"interior":("Interior","Interior")}
caps={
 "blitzlicht":("Blitzlicht-Porträt","Flash portrait"),"rembrandt":("Rembrandt-Licht","Rembrandt light"),"studio-01":("Studio-Porträt","Studio portrait"),"studio-02":("Studio-Porträt","Studio portrait"),
 "rimlight-01":("Rim Light","Rim light"),"rimlight-02":("Rim Light","Rim light"),"projection-01":("Projektion","Projection"),"projection-02":("Projektion","Projection"),
 "interior-01":("Interior, Architektur","Interior, architecture"),"interior-02":("Interior, Architektur","Interior, architecture"),"interior-03":("Interior, Architektur","Interior, architecture"),
 "stilllife-01":("Stillleben, Butterbrot","Still life, bread and butter"),"stilllife-02":("Stillleben","Still life"),"portrait-tattoo":("Porträt","Portrait"),
 "fashion-01":("Fashion, Werkschau","Fashion, Werkschau"),"fashion-02":("Fashion, Werkschau","Fashion, Werkschau"),"fashion-03":("Fashion, Werkschau","Fashion, Werkschau"),
 "uebersberg":("Übersberg","Übersberg"),"feuer":("Feuer","Fire"),"sunset-silhouette":("Sonnenuntergang","Sunset"),"neon-01":("Neon-Porträt","Neon portrait"),"neon-02":("Neon-Porträt","Neon portrait"),
 "prag":("Prag","Prague"),"iceland-plane":("Island, Flugzeugwrack","Iceland, plane wreck"),"iceland-ice":("Island, Eis","Iceland, ice"),"iceland-lava-01":("Island, Lava, Drohne","Iceland, lava, drone"),
 "iceland-waterfall":("Island, Wasserfall","Iceland, waterfall"),"iceland-lava-02":("Island, Lava, Drohne","Iceland, lava, drone"),"iceland-road":("Island, Straße, Drohne","Iceland, road, drone"),
 "seychelles-rocks":("Seychellen, Drohne","Seychelles, drone"),"seychelles-bay":("Seychellen, Drohne","Seychelles, drone"),"vestrahorn":("Island, Vestrahorn","Iceland, Vestrahorn"),
 "aurora":("Island, Nordlicht","Iceland, aurora"),"gym":("Gym, Schwarzweiß","Gym, black and white"),"blond":("Porträt","Portrait"),"drone-01":("Drohne, Luftbild","Drone, aerial"),
 "street-light":("Straßenlicht","Street light"),"subway-orange":("U-Bahn","Subway"),"subway-yellow":("U-Bahn","Subway"),
}
order=["iceland-lava-01","rimlight-01","subway-orange","portrait-tattoo","iceland-plane","projection-01","fashion-02","seychelles-bay","neon-02","interior-01","aurora","blitzlicht","gym","iceland-waterfall","studio-01","street-light","seychelles-rocks","fashion-01","rembrandt","iceland-ice","subway-yellow","interior-02","vestrahorn","rimlight-02","drone-01","stilllife-02","neon-01","iceland-road","fashion-03","prag","projection-02","sunset-silhouette","blond","interior-03","iceland-lava-02","studio-02","uebersberg","stilllife-01","feuer"]
catmap={p["slug"]:p["cat"] for p in man["photo"]}
import random; random.seed(7)
PH=[]
for s in order:
    w,h=dims[s]; tw=900; th=round(h*tw/w) if w>=h else 900; tw=900 if w>=h else round(w*900/h)
    de,en=caps[s]; cat=catmap[s]; speed=round(random.uniform(0.9,1.1),3)
    PH.append(f'''<figure class="ph" data-cat="{cat}" data-full="assets/photo/{s}.jpg" data-title="{e(de)}" data-title-en="{e(en)}" data-speed="{speed}" data-cursor="ÖFFNEN" data-cursor-en="OPEN" tabindex="0" role="button">
  <img src="assets/photo/{s}-t.jpg" alt="{e(de)}" data-en-alt="{e(en)}" loading="lazy" width="{tw}" height="{th}">
  <figcaption class="ph__cap"><span data-en="{e(en)}">{e(de)}</span><span data-en="{e(cats[cat][1])}">{e(cats[cat][0])}</span></figcaption>
</figure>''')
PHOTOS="\n".join(PH)

# ---- design
design=[("ayvo","Ayvo","Packaging","Packaging"),("lazi-kampagne","LAZI Akademie","Kampagne","Campaign"),("nature-one","Nature One","Plakat, Konzept","Poster, concept"),
 ("finnison-ci","FINNISON","Corporate Design","Corporate design"),("cymatics","Cymatics","Plakat","Poster"),("freshy","Freshy","Packaging","Packaging"),
 ("last-exit","Last Exit","Plakat-Redesign","Poster redesign"),("porsche","GT3 RS","Composite","Composite"),("buchcover","Stimmen im Kopf","Buchcover","Book cover"),
 ("wwf","WWF","Kampagne, Konzept","Campaign, concept"),("schwamminator","Schwamminator","Plakat, Konzept","Poster, concept"),("filmplakat","Between Hits and Heartache","Filmplakat","Film poster"),
 ("duracell","Duracell","Anzeige, Konzept","Ad, concept"),("ellipse","Kunst des Weglassens","Anzeige, Konzept","Ad, concept"),("ayvo-tube","Ayvo Tube","Packaging","Packaging"),
 ("typo-light","Bild & Typografie","Typografie","Typography"),("icons","Icon-Set","Goldener Schnitt","Golden ratio")]
DESIGN="\n".join(f'''<figure class="dcard{' dcard--wide' if ddims[s][0]>ddims[s][1]*1.15 else ''}" data-full="assets/design/{s}.jpg" data-title="{e(t)}" data-cursor="ÖFFNEN" data-cursor-en="OPEN" tabindex="0" role="button" data-reveal>
  <div class="dcard__inner"><img src="assets/design/{s}-t.jpg" alt="{e(t)}, {e(kde)}" data-en-alt="{e(t)}, {e(ken)}" loading="lazy" width="{ddims[s][0]}" height="{ddims[s][1]}"></div>
  <figcaption class="dcard__cap"><b>{e(t)}</b><span data-en="{e(ken)}">{e(kde)}</span></figcaption>
</figure>''' for s,t,kde,ken in design)

tpl=open(f"{ROOT}/scripts/index.template.html",encoding="utf-8").read()
out=tpl.replace("{{WALL}}",WALL).replace("{{FILMS}}",FILMS).replace("{{PHOTOS}}",PHOTOS).replace("{{DESIGN}}",DESIGN)
open(f"{ROOT}/site/index.html","w",encoding="utf-8").write(out); print("index.html",len(out),"bytes")
