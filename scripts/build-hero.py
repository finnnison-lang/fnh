# Builds the hero loop: real Canon R5 shots (graded) alternating with triptychs of FNH AI clips.
import subprocess, os
ROOT="/Volumes/Macintosh HD II/AI/FNH WEB"; FF=f"{ROOT}/tools/node_modules/ffmpeg-static/ffmpeg"
DJI="/Volumes/Macintosh HD II/Lazi/2025 S3/FMP/DJI Care"; FNH="/Volumes/Macintosh HD II/AI/FNH Studios"
OUT=f"{ROOT}/site/assets/hero"; os.makedirs(OUT, exist_ok=True)
GRADE="eq=contrast=1.55:brightness=0.03:saturation=1.45:gamma=1.12,colorbalance=rs=-0.05:bs=0.08:rm=-0.02:bm=0.03:rh=0.04:bh=-0.04,unsharp=5:5:0.5"
SEG=2.6; D=0.5; FPS=30
real={"ctrl":(f"{DJI}/Final Footage/096A3635.MP4",3.0),"goggles":(f"{DJI}/Final Footage/096A3650.MP4",3.0),
      "flight":(f"{DJI}/Final Footage/096A3663.MP4",66.0),"men":(f"{DJI}/Final Footage/096A3647.MP4",3.0)}
ai={s:(f"{FNH}/{p}",4.0) for s,p in [l.strip().split("|") for l in open(f"{ROOT}/scripts/clips.txt") if l.strip()]}
def build(kind):
    if kind=="desktop":
        W,H=1920,1080
        seq=[("r","ctrl"),("t",["stuttgart-hbf-flut","tokyo-tsunami","reykjavik-vulkan"]),("r","goggles"),("t",["gt3rs-regenrig","weltrand","wolke-fangen"]),
             ("r","flight"),("t",["dubai-tsunami","achalm-ausbruch","zug-lawine-fpv"]),("r","men"),("t",["angkor-pov","paris-flut","bosch-meteorit"]),("r","ctrl")]
    else:
        W,H=1080,1920
        seq=[("r","ctrl"),("a","stuttgart-hbf-flut"),("r","goggles"),("a","gt3rs-regenrig"),("r","flight"),("a","tokyo-tsunami"),("r","men"),("a","wolke-fangen"),("r","ctrl")]
    inputs=[]; fc=[]; segs=[]; idx=0
    def add(path,start):
        nonlocal idx; inputs.extend(["-ss",str(start),"-t",str(SEG+0.3),"-i",path]); idx+=1; return idx-1
    for n,(k,v) in enumerate(seq):
        lab=f"s{n}"
        if k=="r":
            i=add(*real[v]); fc.append(f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},{GRADE},trim=duration={SEG},setpts=PTS-STARTPTS,format=yuv420p,setsar=1[{lab}]")
        elif k=="a":
            i=add(*ai[v]); fc.append(f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},trim=duration={SEG},setpts=PTS-STARTPTS,format=yuv420p,setsar=1[{lab}]")
        else:
            ids=[add(*ai[s]) for s in v]; pans=[]
            for j,i in enumerate(ids):
                fc.append(f"[{i}:v]scale=608:1080,crop=600:1080,fps={FPS},trim=duration={SEG},setpts=PTS-STARTPTS[p{n}{j}]"); pans.append(f"p{n}{j}")
            fc.append(f"color=c=0x06080d:s={W}x{H}:r={FPS}:d={SEG}[bg{n}]")
            fc.append(f"[bg{n}][{pans[0]}]overlay=20:0:shortest=1[o{n}a];[o{n}a][{pans[1]}]overlay=660:0:shortest=1[o{n}b];[o{n}b][{pans[2]}]overlay=1300:0:shortest=1,format=yuv420p,setsar=1[{lab}]")
        segs.append(lab)
    prev=segs[0]
    for n in range(1,len(segs)):
        off=round(n*(SEG-D),3); out=f"x{n}"; fc.append(f"[{prev}][{segs[n]}]xfade=transition=fade:duration={D}:offset={off}[{out}]"); prev=out
    loop_len=round((len(segs)-1)*(SEG-D),3)
    fc.append(f"[{prev}]trim=start={D}:end={round(D+loop_len,3)},setpts=PTS-STARTPTS,noise=alls=4:allf=t,vignette=PI/5,format=yuv420p[out]")
    crf="22" if kind=="desktop" else "26"
    cmd=[FF,"-nostdin","-v","error","-y",*inputs,"-filter_complex",";".join(fc),"-map","[out]","-c:v","libx264","-crf",crf,"-preset","slow","-profile:v","high","-g","60","-pix_fmt","yuv420p","-movflags","+faststart","-an",f"{OUT}/hero-{kind}.mp4"]
    print("building",kind,"loop",loop_len,"s"); r=subprocess.run(cmd,stdin=subprocess.DEVNULL,capture_output=True,text=True); print(r.stderr[-2000:] if r.returncode else "ok")
    subprocess.run([FF,"-nostdin","-v","error","-y","-i",f"{OUT}/hero-{kind}.mp4","-frames:v","1","-q:v","3",f"{OUT}/hero-{kind}.jpg"],stdin=subprocess.DEVNULL)
    print(kind,"size",os.path.getsize(f"{OUT}/hero-{kind}.mp4")//1024,"KB")
build("desktop"); build("mobile"); print("HERO DONE")
