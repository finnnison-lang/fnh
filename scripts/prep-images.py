# Copies and resizes the curated photos, design pieces, about images into site/assets.
import os, json
from PIL import Image, ImageOps
Image.MAX_IMAGE_PIXELS = None
ROOT = "/Volumes/Macintosh HD II/AI/FNH WEB/site/assets"
L = "/Volumes/Macintosh HD II/Lazi"
O = "/private/tmp/claude-501/-Volumes-Macintosh-HD-II-AI-FNH-WEB/b87477ba-bb7c-4d8d-b0c8-fb2e463af88d/scratchpad/oldimg"
H = "/private/tmp/claude-501/-Volumes-Macintosh-HD-II-AI-FNH-WEB/b87477ba-bb7c-4d8d-b0c8-fb2e463af88d/scratchpad/heic"
F = "/Volumes/Macintosh HD II/AI/FNH Studios"

photos = [
 ("blitzlicht", f"{L}/2023 S1/CP/BLITZLICHT/Final/CP_111_WS23_Finn-Hafemann_ BLITZLICHT.jpg", "studio"),
 ("rembrandt", f"{L}/2023 S1/CP/Dauerlicht Portrait/Final/CP_111_WS23_Finn-Hafemann_Dauerlicht-Rembrandt.jpg", "studio"),
 ("studio-01", f"{L}/2023 S1/CP/Freie Aufgabe Istock/CP_111_WS23_Finn-Hafemann_FREIE AUFGABE/CP_111_WS23_Finn-Hafemann_FREIE AUFGABE_03.jpg", "studio"),
 ("studio-02", f"{L}/2023 S1/CP/Freie Aufgabe Istock/CP_111_WS23_Finn-Hafemann_FREIE AUFGABE/CP_111_WS23_Finn-Hafemann_FREIE AUFGABE_05.jpg", "studio"),
 ("rimlight-01", f"{L}/2023 S1/CP/Rim Light/Final_/2T4A2259-Bearbeitet.jpg", "studio"),
 ("rimlight-02", f"{L}/2023 S1/CP/Rim Light/Final_/2T4A2293-Bearbeitet.jpg", "studio"),
 ("projection-01", f"{L}/2024 S2/FD/Freie Aufgabe Maite Portrait/Abgabe/FD_x2x_SS24_Finn-Hafemann_Freie_Aufgabe.jpg", "studio"),
 ("projection-02", f"{L}/2024 S2/FD/Freie Aufgabe Maite Portrait/Moodboard FA/8ca00711fa188c420a24badb16691efe.jpg", "studio"),
 ("interior-01", f"{L}/2023 S1/CP/_BTS B ROLL_/Final/2023-pi-interior-A-0066.jpg", "interior"),
 ("interior-02", f"{L}/2023 S1/CP/_BTS B ROLL_/Final/2023-pi-interior-A-0437.jpg", "interior"),
 ("interior-03", f"{L}/2023 S1/CP/_BTS B ROLL_/Final/2023-pi-interior-B-0523.jpg", "interior"),
 ("stilllife-01", f"{L}/2024 S2/FD/FD_x2x_SS24_Finn-Hafemann_Das geilste Bild des geilsten, leckersten Butterbrotes der Welt/H&M&F&H/FH ISTOCK/2T4A2655-Bearbeitet.jpg", "studio"),
 ("stilllife-02", f"{L}/2024 S2/FD/Freie Aufgabe Still Life/All/096A9691.JPG", "studio"),
 ("portrait-tattoo", f"{L}/2024 S2/FD/Martin & Finn Portraits/ALL/096A4390.JPG", "portrait"),
 ("fashion-01", f"{L}/2025 S4/GM/Werkschau BTS/Werkschau BTS JPG - Finn Hafemann /2T4A7574.jpg", "portrait"),
 ("fashion-02", f"{L}/2025 S4/GM/Werkschau BTS/Werkschau BTS JPG - Finn Hafemann /2T4A7606.jpg", "portrait"),
 ("fashion-03", f"{L}/2025 S4/GM/Werkschau BTS/Werkschau BTS JPG - Finn Hafemann /2T4A7655.jpg", "portrait"),
 ("uebersberg", f"{O}/2020-F_M-Übersberg-611.jpg", "portrait"),
 ("feuer", f"{O}/2020-Franz-Feuer-86.jpg", "portrait"),
 ("sunset-silhouette", f"{O}/2020-felix-max-Uuebersberg-475.jpg", "travel"),
 ("neon-01", f"{O}/2020-josip-15.07.2020-26.jpg", "portrait"),
 ("neon-02", f"{O}/2020-michel-15.07.2020-12.jpg", "portrait"),
 ("prag", f"{O}/2020-prag-501.jpg", "travel"),
 ("iceland-plane", f"{O}/2021-Canon-R5-Iceland-A-1221.jpg", "travel"),
 ("iceland-ice", f"{O}/2021-Canon-R5-Iceland-A-2350-Bearbeitet.jpg", "travel"),
 ("iceland-lava-01", f"{O}/2021-DJI-Mavic-Iceland-990.jpg", "aerial"),
 ("iceland-waterfall", f"{O}/2021-canon-r5-iceland-396.jpg", "travel"),
 ("iceland-lava-02", f"{O}/2021-dji-mavic-iceland-980.jpg", "aerial"),
 ("iceland-road", f"{O}/2021-mavic-iceland-491.jpg", "aerial"),
 ("seychelles-rocks", f"{O}/2021-seychellen-mavic3-1093.jpg", "aerial"),
 ("seychelles-bay", f"{O}/2021-seychellen-mavic3-227.jpg", "aerial"),
 ("vestrahorn", f"{O}/2022-Iceland-Canon-R5-A-807-Bearbeitet.jpg", "travel"),
 ("aurora", f"{O}/2022-Iceland-Canon-R5-F-465-Bearbeitet.jpg", "travel"),
 ("gym", f"{O}/Bodybuilding-Özgür03.jpg", "portrait"),
 ("blond", f"{O}/blond-girl.jpg", "portrait"),
 ("drone-01", f"{O}/drone-view-3.jpg", "aerial"),
 ("street-light", f"{O}/street-light-felix.jpg", "portrait"),
 ("subway-orange", f"{O}/subway-station-girl-11.jpg", "portrait"),
 ("subway-yellow", f"{O}/subway-station-girl-4.jpg", "portrait"),
]
design = [
 ("typo-light", f"{L}/2023 S1/CTGD/Bild Typhographie_/CTGD_111_WS23_Finn-Hafemann_Bild TypografieV2.jpg"),
 ("porsche", f"{L}/2023 S1/CTGD/iphone _ Autos/Porsche/porsche-model.png"),
 ("finnison-ci", f"{L}/2023 S1/GD/Briefpapier/OQ3A3K1 Kopie.jpg"),
 ("nature-one", f"{L}/2023 S1/GD/Plakat _ Anzeige/Abgabe/2Orange and Green Modern Futuristic Party Playlist Cover 2.jpg"),
 ("icons", f"{L}/2023 S1/GE/Goldener Schnitt 2.0/_db7490b9-f8e8-4ed6-aa3c-90a63f025406.jpeg"),
 ("duracell", f"{L}/2023 S1/KT/Duracell/Figur/_6b558a83-f02b-4e3c-850c-4bb74a65d13c Kopie.jpg"),
 ("wwf", f"{L}/2023 S1/KT/Werbung WWF_/Final/2 .jpg"),
 ("ayvo", f"{L}/2024 S2/CTGD/Ayvo/Logo Schachtel/Renderings: DM : AI/Ayvo 1.png"),
 ("ayvo-tube", f"{L}/2024 S2/CTGD/CTGD_222_SS24_Finn-Hafemann_Ayvo/Datein/Ayvo Tube Vorne.png"),
 ("freshy", f"{L}/2024 S2/CTGD/Freshy/Abgabe/CTGD_222_SS24_Finn-Hafemann_Freshy.png"),
 ("filmplakat", f"{L}/2024 S2/ST/PF/Final/JPGS/ST_222_SS24_Finn-Hafemann_Filmplakat.jpg"),
 ("buchcover", f"{L}/2025 S4/GE/Buchcover : Gegenstand/69a54d52-bd72-4d51-a3da-c87757ee1eaa Kopie.jpg"),
 ("schwamminator", f"{L}/2025 S4/GE/Schwam/GE_444_SS25_Finn-hafemann_ Schwamm_Mockup.png"),
 ("ellipse", f"{L}/2025 S5/GE/Ellipse/GE_444_SS25_Finn-hafemann_Ellipse, Kunst des Weglassens_I2.png"),
 ("lazi-kampagne", f"{L}/2025 S5/GE/GE_LAZI_Kampange/GE_555_WS25_Finn-Hafemann_Film_Codes.jpg"),
 ("last-exit", f"{L}/2025 S5/GE/Redesign/GE_555_SS25_Finn-hafemann_ Redesign_plakat-1.png"),
 ("cymatics", f"{L}/2025 S4/Werkschau/GM_SS25_Schülermotiv mit eigener Arbeit (Sneak Peak)1.jpg"),
]
about = [
 ("finn-portrait", f"{F}/01_brand/fnh-studios/master-refs/FNH-Master-m4.png"),
 ("finn-werkschau", f"{L}/2025 S4/Werkschau/GM_SS25_Werkschaushooting-2449-Portait-Finn-Hafemann.jpg"),
 ("finn-work-01", f"{H}/FullSizeRender 2.jpg"),
 ("finn-work-02", f"{H}/FullSizeRender.jpg"),
 ("finn-work-03", f"{H}/IMG_1286.jpg"),
 ("finn-work-04", f"{H}/IMG_1843.jpg"),
 ("finn-work-05", f"{H}/IMG_4149.jpg"),
]
def load(p):
    im = Image.open(p); im = ImageOps.exif_transpose(im)
    if im.mode in ("RGBA","LA","P"):
        bg = Image.new("RGB", im.size, (255,255,255)); im = im.convert("RGBA"); bg.paste(im, mask=im.split()[-1]); im = bg
    return im.convert("RGB")
def save(im, path, maxe, q=82):
    im = im.copy(); im.thumbnail((maxe, maxe), Image.LANCZOS); im.save(path, "JPEG", quality=q, optimize=True, progressive=True); return im.size
manifest = {"photo": [], "design": [], "about": []}
for slug, src, cat in photos:
    im = load(src); w,h = save(im, f"{ROOT}/photo/{slug}.jpg", 1800); save(im, f"{ROOT}/photo/{slug}-t.jpg", 900, 80)
    manifest["photo"].append({"slug": slug, "cat": cat, "w": w, "h": h}); print("photo", slug, w, h)
for slug, src in design:
    im = load(src); w,h = save(im, f"{ROOT}/design/{slug}.jpg", 1800); save(im, f"{ROOT}/design/{slug}-t.jpg", 1000, 82)
    manifest["design"].append({"slug": slug, "w": w, "h": h}); print("design", slug, w, h)
for slug, src in about:
    im = load(src); w,h = save(im, f"{ROOT}/img/{slug}.jpg", 1600, 84)
    manifest["about"].append({"slug": slug, "w": w, "h": h}); print("about", slug, w, h)
json.dump(manifest, open("/Volumes/Macintosh HD II/AI/FNH WEB/scripts/images-manifest.json","w"), indent=1)
print("IMAGES DONE")
