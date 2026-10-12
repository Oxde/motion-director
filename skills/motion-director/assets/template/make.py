#!/usr/bin/env python3
"""Build the film from cues.json: sync the page → mix the sound → check → render → master → proof.

    python3 make.py              # everything; the film lands in out/<id>.mp4, the proof in out/proof/
    python3 make.py --check      # sync, mix and run the checker only
    python3 make.py --still 0.5  # one PNG at that second instead of a film (banners, cards)
"""
import argparse, json, os, re, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); HF = ["npx", "-y", "hyperframes@0.8.33"]

def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=HERE, **kw)
    if r.returncode != 0: sys.exit(f"$ {' '.join(cmd[:5])} …\n{r.stdout[-2500:]}\n{r.stderr[-2500:]}")
    return r.stdout + r.stderr

def need_node():
    v = subprocess.run(["node", "-v"], capture_output=True, text=True).stdout.strip()
    if not v or int(v.lstrip("v").split(".")[0]) < 22:
        sys.exit(f"HyperFrames needs Node 22+, found {v or 'none'}. Put a Node 22 bin directory first on PATH and run again.")

def sync(c):
    """cues.json → cues.js and every data-start / data-duration in index.html."""
    bad = subprocess.run([sys.executable, "cues.py", "check"], capture_output=True, text=True, cwd=HERE)
    if bad.returncode != 0: sys.exit(bad.stdout[-1500:] + bad.stderr[-1500:])
    open(os.path.join(HERE, "cues.js"), "w").write("window.CUES = " + json.dumps(c).replace("</", "<\\/") + ";\n")
    p = os.path.join(HERE, "index.html"); html = open(p).read(); scenes = {s["id"]: s for s in c["scenes"]}; seen = set()
    def attr(tag, name, val):
        return re.sub(rf'{name}="[^"]*"', f'{name}="{val}"', tag) if re.search(rf'{name}="', tag) else tag[:-1] + f' {name}="{val}">'
    def fix(m):
        tag = m.group(0); sid = re.search(r'data-scene="([^"]+)"', tag).group(1)
        if sid not in scenes: sys.exit(f'index.html uses data-scene="{sid}" but cues.json has scenes {list(scenes)}')
        seen.add(sid); return attr(attr(tag, "data-start", scenes[sid]["start"]), "data-duration", scenes[sid]["dur"])
    html = re.sub(r'<[a-zA-Z][^<>]*data-scene="[^"]+"[^<>]*>', fix, html)
    def root(m):
        t = m.group(0)
        for k, v in (("data-duration", c["duration"]), ("data-width", c["width"]), ("data-height", c["height"]), ("data-fps", c["fps"])): t = attr(t, k, v)
        return t
    html, n = re.subn(r'<[a-zA-Z][^<>]*data-composition-id="[^"]+"[^<>]*>', root, html)
    if n != 1: sys.exit(f"index.html must have exactly one element with data-composition-id, found {n}")
    html = re.sub(r'<audio[^<>]*id="mix"[^<>]*>', lambda m: attr(attr(m.group(0), "data-start", 0), "data-duration", c["duration"]), html)
    missing = set(scenes) - seen
    if missing: print(f"note: no element uses scene(s) {sorted(missing)}")
    open(p, "w").write(html)

def check():
    for attempt in (1, 2):
        out = subprocess.run(HF + ["check"], capture_output=True, text=True, cwd=HERE); text = out.stdout + out.stderr
        flagged = [l for l in text.splitlines() if "✗" in l]
        if "Check failed" not in text:
            if flagged: print("\n".join(flagged))
            print("check: passed"); return
        if attempt == 1 and flagged and all("AudioContext" in l for l in flagged): continue   # flaky audio device in the check browser
        sys.exit("\n".join(flagged) + "\ncheck failed: fixes are in the skill's references/hyperframes.md")

def frame(src, t, dest, width=None):
    vf = ["-vf", f"scale={width}:-2"] if width else []
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", src, "-frames:v", "1", *vf, dest], check=True, cwd=HERE)

def proof(c, film):
    from PIL import Image, ImageDraw
    d = os.path.join(HERE, "out", "proof"); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    times = sorted({round(min(c["duration"] - .05, x), 2) for x in [s["start"] + .4 for s in c["scenes"]] + [s["start"] + s["dur"] - .15 for s in c["scenes"]] + [v["t"] + .3 for v in c.get("cues", {}).values()]})
    for name, width, cols in (("sheet.jpg", 640, 4), ("sheet-phone.jpg", 360, 3)):
        tiles = []
        for t in times:
            f = os.path.join(d, "f.jpg"); frame(film, t, f, width); im = Image.open(f).convert("RGB"); ImageDraw.Draw(im).text((6, 6), f"{t}s", fill="red"); tiles.append(im)
        w, h = tiles[0].size; rows = -(-len(tiles) // cols); sheet = Image.new("RGB", (w * cols, h * rows))
        for i, im in enumerate(tiles): sheet.paste(im, ((i % cols) * w, (i // cols) * h))
        sheet.save(os.path.join(d, name), quality=88); os.remove(os.path.join(d, "f.jpg"))
    probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,r_frame_rate,duration", "-of", "csv=p=0", film], capture_output=True, text=True, cwd=HERE).stdout
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", film, "-af", "loudnorm=print_format=json", "-f", "null", "-"], capture_output=True, text=True, cwd=HERE).stderr
    j = json.loads(re.search(r"\{[^{}]*\}", err, re.S).group())
    rep = [f"file: {film}", probe.strip(), f"loudness: {j['input_i']} LUFS (target about -14)", f"true peak: {j['input_tp']} dBTP (must be under -1)", f"frames sampled: {times}"]
    if c.get("voice"):
        tool = shutil.which("mlx_whisper") or shutil.which("whisper")
        if not tool: rep.append("transcript: NOT MADE, no mlx_whisper or whisper on PATH. The speech is unverified.")
        else:
            args = [tool, film, "--output-dir", d, "-f" if "mlx" in tool else "--output_format", "txt"] + (["--model", "mlx-community/whisper-base-mlx"] if "mlx" in tool else ["--model", "base"])
            subprocess.run(args, capture_output=True, text=True, cwd=HERE)
            got = [f for f in os.listdir(d) if f.endswith(".txt") and f != "report.txt"]
            if got: os.replace(os.path.join(d, got[0]), os.path.join(d, "transcript.txt")); rep.append("transcript: out/proof/transcript.txt (compare with the script)")
            else: rep.append("transcript: NOT MADE, the transcriber produced no file. The speech is unverified.")
    open(os.path.join(d, "report.txt"), "w").write("\n".join(rep) + "\n"); print("\n".join(rep)); print("proof: out/proof/  → read sheet.jpg and sheet-phone.jpg, then fill REVIEW.md")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--check", action="store_true"); ap.add_argument("--still", type=float); a = ap.parse_args()
    need_node(); c = json.load(open(os.path.join(HERE, "cues.json"))); sync(c)
    print(run([sys.executable, "mix.py"]).strip()); check()
    if a.check: return
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True); raw = os.path.join("out", "raw.mp4")
    run(HF + ["render", "-o", raw, "-q", "high", "-f", str(c["fps"])])
    if a.still is not None:
        dest = os.path.join("out", f"{c['id']}.png")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a.still), "-i", raw, "-frames:v", "1", "-vf", f"format=rgb24,crop={c['width']}:{c['height']}:0:0", dest], check=True, cwd=HERE)
        os.remove(os.path.join(HERE, raw)); print("→", dest); return
    film = os.path.join("out", f"{c['id']}.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-c:v", "libx264", "-crf", "18", "-preset", "slow", "-pix_fmt", "yuv420p", "-af", "alimiter=limit=0.89:level=false", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", film], check=True, cwd=HERE)
    os.remove(os.path.join(HERE, raw)); print("→", film, f"({os.path.getsize(os.path.join(HERE, film))/1e6:.1f} MB)"); proof(c, film)

if __name__ == "__main__":
    main()
