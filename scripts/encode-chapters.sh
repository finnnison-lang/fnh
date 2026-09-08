#!/bin/bash
# Journey chapters: short muted loops (for the scroll journey) + full versions with sound (lightbox) + posters.
ROOT="/Volumes/Macintosh HD II/AI/FNH WEB"; FF="$ROOT/tools/node_modules/ffmpeg-static/ffmpeg"; FP="$ROOT/tools/node_modules/ffprobe-static/bin/darwin/arm64/ffprobe"
P="/Volumes/Macintosh HD II/AI/FNH Studios/02_projekte"; A="/Volumes/Macintosh HD II/AI/Abschlussarbeit-Finn"; V="/Volumes/Macintosh HD II/Videos"
OUT="$ROOT/site/assets/work"; mkdir -p "$OUT"
loop(){ slug=$1; in=$2; ss=$3; dur=$4; size=$5; "$FF" -nostdin -v error -y -ss "$ss" -t "$dur" -i "$in" -vf "scale=$size:force_original_aspect_ratio=increase,crop=$size,fps=30,format=yuv420p" -c:v libx264 -crf 26 -preset slow -profile:v high -g 60 -movflags +faststart -an "$OUT/$slug-loop.mp4" </dev/null; echo "loop $slug $(( $(stat -f%z "$OUT/$slug-loop.mp4")/1024 ))KB"; }
full(){ slug=$1; in=$2; w=$3; crf=$4; "$FF" -nostdin -v error -y -i "$in" -vf "scale=$w:-2,format=yuv420p" -c:v libx264 -crf "$crf" -preset medium -profile:v high -movflags +faststart -c:a aac -b:a 128k -ac 2 "$OUT/$slug.mp4" </dev/null; echo "full $slug $(( $(stat -f%z "$OUT/$slug.mp4")/1024 ))KB"; }
poster(){ slug=$1; in=$2; ss=$3; size=$4; "$FF" -nostdin -v error -y -ss "$ss" -i "$in" -frames:v 1 -vf "scale=$size:force_original_aspect_ratio=increase,crop=$size" -q:v 3 "$OUT/$slug.jpg" </dev/null; }
# 1 Nürburgring 24h (three 30 s parts)
R="$P/aktiv/2026-09-03_daytona-nachtrennen/04_renders"; loop race "$R/teil1_render1.mp4" 3 12 1280:720; poster race "$R/teil1_render1.mp4" 9 1280:720
printf "file '%s'\nfile '%s'\nfile '%s'\n" "$R/teil1_render1.mp4" "$R/teil2_v7_render1.mp4" "$R/Teil3.mp4" > "$ROOT/tools/race-concat.txt"
"$FF" -nostdin -v error -y -f concat -safe 0 -i "$ROOT/tools/race-concat.txt" -vf "scale=1280:-2,format=yuv420p" -c:v libx264 -crf 25 -preset medium -profile:v high -movflags +faststart -c:a aac -b:a 128k -ac 2 "$OUT/race.mp4" </dev/null; echo "full race $(( $(stat -f%z "$OUT/race.mp4")/1024 ))KB"
# 2 OdyssAI 2028 (trailer)
T="$A/08_Render/Trailer/OdyssAI-2028-Trailer.mp4"; loop odyssai "$T" 38 12 1280:720; poster odyssai "$T" 48 1280:720; full odyssai "$T" 1920 25
# 3 Iceland
I="$V/2022/2022-Iceland-Video/Iceland.mp4"; loop iceland "$I" 140 12 1280:720; poster iceland "$I" 145 1280:720; full iceland "$I" 1280 27
# 4 Kuppelkino (vertical)
K="$P/archiv/2026-07-22_wand-bricht-arena/05_final/FNH-Studios_Wand-Bricht-Turm-Durchbruch_9x16.mp4"; loop kuppelkino "$K" 0 11.3 720:1280; poster kuppelkino "$K" 5 720:1280; full kuppelkino "$K" 1080 26
# 5 Red Bull Oma (vertical)
RB="$P/aktiv/2026-08-21_redbull-turm-cctv/04_renders/render_v3_dreamina.mp4"; loop redbull "$RB" 0 15 720:1280; poster redbull "$RB" 6 720:1280; full redbull "$RB" 720 26
# 6 Cymatics
C="$V/2025/Cymatic/CYMATICS MOV/CYMATICS-FHD-FINN_HAFEMANN.mov"; loop cymatics "$C" 236 12 1280:720; poster cymatics "$C" 240 1280:720; full cymatics "$C" 1280 27
# 7 Singapur (vertical)
S="$P/archiv/2026-07-16_singapur-erdbeben/05_final/FNH-Studios-Singapur-Erdbeben-9x16.mp4"; loop singapur "$S" 0 12 720:1280; poster singapur "$S" 6 720:1280; full singapur "$S" 1080 26
# 8 Husky (vertical) from original
H="$P/aktiv/2026-08-23_wasserpistole-letztes-drama/05_final/FNH-Studios_Husky-Wasserpistole_9x16.mp4"; loop husky "$H" 0 12 720:1280; poster husky "$H" 8 720:1280; full husky "$H" 1080 26
# index extras
FL="$P/archiv/2026-08-08_studio-cdg-antonov/05_final/FNH-Studios_Studio-Flughafen_9x16.mp4"; [ -f "$FL" ] || FL="$P/aktiv/2026-08-08_studio-cdg-antonov/05_final/FNH-Studios_Studio-Flughafen_9x16.mp4"; poster flughafen "$FL" 6 540:960; full flughafen "$FL" 720 26
FT="$P/archiv/2026-07-22_falltraum-fernsehturm/05_final/FNH-Studios_Falltraum-Fernsehturm_9x16.mp4"; poster falltraum "$FT" 4 540:960; full falltraum "$FT" 720 26
A8="$P/archiv/2026-08-02_a8-bosch-parkhaus-real/05_final/FNH-Studios_A8-Notlandung_9x16_ohne schild.mp4"; poster a8 "$A8" 5 540:960; full a8 "$A8" 720 26
D1="$P/archiv/2026-07-20_dispatch-001-cold-start/05_final/FNH-Studios_DISPATCH-001-Tot-Akzeptiert_9x16.mp4"; poster dispatch "$D1" 6 540:960; full dispatch "$D1" 720 26
du -sh "$OUT"; echo CHAPTERS DONE
