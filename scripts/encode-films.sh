#!/bin/bash
# Encodes the real film work: full versions, muted preview loops and posters. Also process keyframes.
ROOT="/Volumes/Macintosh HD II/AI/FNH WEB"; FF="$ROOT/tools/node_modules/ffmpeg-static/ffmpeg"; L="/Volumes/Macintosh HD II/Lazi"; F="/Volumes/Macintosh HD II/AI/FNH Studios"
OUT="$ROOT/site/assets/film"; PR="$ROOT/site/assets/img/process"; mkdir -p "$OUT" "$PR"
enc(){ slug="$1"; in="$2"; w="$3"; pstart="$4"; poster="$5"
  "$FF" -nostdin -v error -y -i "$in" -vf "scale=$w:-2,format=yuv420p" -c:v libx264 -crf 26 -preset medium -profile:v high -movflags +faststart -c:a aac -b:a 128k -ac 2 "$OUT/$slug.mp4" </dev/null
  "$FF" -nostdin -v error -y -ss "$pstart" -t 8 -i "$in" -vf "scale=960:-2,fps=24,format=yuv420p" -c:v libx264 -crf 28 -preset medium -movflags +faststart -an "$OUT/$slug-preview.mp4" </dev/null
  "$FF" -nostdin -v error -y -ss "$poster" -i "$in" -frames:v 1 -vf "scale=1280:-2" -q:v 4 "$OUT/$slug.jpg" </dev/null
  echo "done $slug full=$(( $(stat -f%z "$OUT/$slug.mp4")/1024 ))KB preview=$(( $(stat -f%z "$OUT/$slug-preview.mp4")/1024 ))KB"; }
enc wuenschewagen "$L/2025 S3/CTFM/HiDrive/CTFM_333_SS24_Finn-Hafemann_Aufgabe_03_ASB.mp4" 1280 60 150
enc die-bank "$L/2024 S2/CP/Die Bank/Finale Abgabe/CP_222_SS24_Finn-Hafemann_Praxisaufgabe CP 7, Smartphone Filmmaking.mov" 1920 20 30
enc werbevideo "$L/2023 S1/CP/Werbevideo/Abgabe/CP_111_WS23_Finn-Hafemann_Werbevideo.mp4" 1920 10 32
enc basketball "$L/2026 S6/CTAE/HA_04_Hafemann_Finn/HA_04_Hafemann_Finn.mp4" 1920 3 9
enc parallax "$L/2024 S2/CTFD/2,5 D Paralax-Effekt/CTFD_222_SS24_Finn-Hafemann_2,5_D_Paralax-Effekt_V2.mp4" 1920 0 2.5
# process: keyframe vs final frame
"$FF" -nostdin -v error -y -i "$F/02_projekte/aktiv/2026-08-16_zug-lawine-modellberg/03_startbilder/kf_zug-lawine_v13_FINAL.png" -vf "scale=810:1440:force_original_aspect_ratio=increase,crop=810:1440" -q:v 4 "$PR/zug-keyframe.jpg" </dev/null
"$FF" -nostdin -v error -y -ss 7 -i "$F/ALLE-FINALEN-CLIPS/ZUG-LAWINE-MODELLBERG_12s_final.mp4" -frames:v 1 -vf "scale=810:1440:force_original_aspect_ratio=increase,crop=810:1440" -q:v 4 "$PR/zug-final.jpg" </dev/null
"$FF" -nostdin -v error -y -i "$F/02_projekte/aktiv/2026-08-29_katze-slapfight/03_startbilder/sb_slapfight_v8_9x16_1080x1920.png" -vf "scale=810:1440:force_original_aspect_ratio=increase,crop=810:1440" -q:v 4 "$PR/slap-keyframe.jpg" </dev/null
"$FF" -nostdin -v error -y -ss 6 -i "$F/ALLE-FINALEN-CLIPS/KATZE-SLAPFIGHT_10s_final.mp4" -frames:v 1 -vf "scale=810:1440:force_original_aspect_ratio=increase,crop=810:1440" -q:v 4 "$PR/slap-final.jpg" </dev/null
# werbevideo frames for naming
for p in 4 20 40 66; do "$FF" -nostdin -v error -y -ss $p -i "$L/2023 S1/CP/Werbevideo/Abgabe/CP_111_WS23_Finn-Hafemann_Werbevideo.mp4" -frames:v 1 -vf scale=480:-2 "/private/tmp/claude-501/-Volumes-Macintosh-HD-II-AI-FNH-WEB/b87477ba-bb7c-4d8d-b0c8-fb2e463af88d/scratchpad/werbe_$p.png" </dev/null; done
ls -la "$PR"; du -sh "$OUT"; echo "FILMS DONE"
