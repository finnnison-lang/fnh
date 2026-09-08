# Hero v2: montage of the strongest 16:9 work (race, OdyssAI, Iceland, Cymatics), seamless loop, desktop + mobile.
import subprocess, os
ROOT="/Volumes/Macintosh HD II/AI/FNH WEB"; FF=f"{ROOT}/tools/node_modules/ffmpeg-static/ffmpeg"
P="/Volumes/Macintosh HD II/AI/FNH Studios/02_projekte"; A="/Volumes/Macintosh HD II/AI/Abschlussarbeit-Finn"; V="/Volumes/Macintosh HD II/Videos"
OUT=f"{ROOT}/site/assets/hero"; os.makedirs(OUT, exist_ok=True)
R=f"{P}/aktiv/2026-09-03_daytona-nachtrennen/04_renders"; T=f"{A}/08_Render/Trailer/OdyssAI-2028-Trailer.mp4"; I=f"{V}/2022/2022-Iceland-Video/Iceland.mp4"; C=f"{V}/2025/Cymatic/CYMATICS MOV/CYMATICS-FHD-FINN_HAFEMANN.mov"
seq=[(f"{R}/teil1_render1.mp4",4.0),(T,10.0),(I,144.0),(f"{R}/teil1_render1.mp4",19.0),(C,239.0),(T,46.0),(f"{R}/teil2_v7_render1.mp4",8.0),(I,60.0),(f"{R}/teil1_render1.mp4",4.0)]
SEG=2.8; D=0.6; FPS=30
def build(kind):
    W,H=(1920,1080) if kind=="desktop" else (1080,1920)
    inputs=[]; fc=[]; segs=[]
    for n,(path,start) in enumerate(seq):
        inputs.extend(["-ss",str(start),"-t",str(SEG+0.3),"-i",path]); lab=f"s{n}"
        fc.append(f"[{n}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},trim=duration={SEG},setpts=PTS-STARTPTS,format=yuv420p,setsar=1[{lab}]"); segs.append(lab)
    prev=segs[0]
    for n in range(1,len(segs)):
        off=round(n*(SEG-D),3); out=f"x{n}"; fc.append(f"[{prev}][{segs[n]}]xfade=transition=fade:duration={D}:offset={off}[{out}]"); prev=out
    loop_len=round((len(segs)-1)*(SEG-D),3)
    fc.append(f"[{prev}]trim=start={D}:end={round(D+loop_len,3)},setpts=PTS-STARTPTS,eq=saturation=0.92:contrast=1.04,format=yuv420p[out]")
    crf="24" if kind=="desktop" else "27"; scale=[] if kind=="desktop" else []
    cmd=[FF,"-nostdin","-v","error","-y",*inputs,"-filter_complex",";".join(fc),"-map","[out]","-c:v","libx264","-crf",crf,"-preset","slow","-profile:v","high","-g","60","-pix_fmt","yuv420p","-movflags","+faststart","-an",f"{OUT}/hero-{kind}.mp4"]
    r=subprocess.run(cmd,stdin=subprocess.DEVNULL,capture_output=True,text=True); print(kind, "loop", loop_len, r.stderr[-1500:] if r.returncode else "ok")
    subprocess.run([FF,"-nostdin","-v","error","-y","-i",f"{OUT}/hero-{kind}.mp4","-frames:v","1","-q:v","3",f"{OUT}/hero-{kind}.jpg"],stdin=subprocess.DEVNULL)
    print(kind,"size",os.path.getsize(f"{OUT}/hero-{kind}.mp4")//1024,"KB")
build("desktop")
# mobile at 720x1280 for weight
import shutil
build("mobile")
subprocess.run([FF,"-nostdin","-v","error","-y","-i",f"{OUT}/hero-mobile.mp4","-vf","scale=720:1280","-c:v","libx264","-crf","28","-preset","slow","-g","60","-pix_fmt","yuv420p","-movflags","+faststart","-an",f"{OUT}/hero-mobile-small.mp4"],stdin=subprocess.DEVNULL)
os.replace(f"{OUT}/hero-mobile-small.mp4", f"{OUT}/hero-mobile.mp4"); print("mobile final", os.path.getsize(f"{OUT}/hero-mobile.mp4")//1024, "KB"); print("HERO2 DONE")
