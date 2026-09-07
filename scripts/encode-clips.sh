#!/bin/bash
# Transcodes the curated FNH 9:16 clips into web-optimized mp4 + poster jpg.
ROOT="/Volumes/Macintosh HD II/AI/FNH WEB"; FF="$ROOT/tools/node_modules/ffmpeg-static/ffmpeg"; FP="$ROOT/tools/node_modules/ffprobe-static/bin/darwin/arm64/ffprobe"
SRC="/Volumes/Macintosh HD II/AI/FNH Studios"; OUT="$ROOT/site/assets/video"; mkdir -p "$OUT"
: > "$ROOT/scripts/clips-manifest.txt"
while IFS='|' read -r slug rel; do
  [ -z "$slug" ] && continue; in="$SRC/$rel"
  dur=$("$FP" -v error -show_entries format=duration -of csv=p=0 "$in" </dev/null)
  "$FF" -nostdin -v error -y -i "$in" -vf "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2,format=yuv420p" -c:v libx264 -crf 26 -preset medium -profile:v high -level 4.0 -movflags +faststart -c:a aac -b:a 96k -ac 2 "$OUT/$slug.mp4" </dev/null
  t=$(python3 -c "print($dur*0.4)")
  "$FF" -nostdin -v error -y -ss "$t" -i "$in" -frames:v 1 -vf "scale=540:960:force_original_aspect_ratio=decrease,pad=540:960:(ow-iw)/2:(oh-ih)/2" -q:v 4 "$OUT/$slug.jpg" </dev/null
  sz=$(stat -f%z "$OUT/$slug.mp4"); printf "%s\t%.1f\t%d\n" "$slug" "$dur" "$sz" >> "$ROOT/scripts/clips-manifest.txt"; echo "done $slug $((sz/1024)) KB"
done < "$ROOT/scripts/clips.txt"
echo ALLDONE
