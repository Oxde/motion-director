#!/usr/bin/env python3
"""Scaffold a video project: cues.json (the one timeline), index.html, mix.py, make.py, brief.md, REVIEW.md.

    new_project.py <folder> --id <composition-id> [--duration 18] [--size 1920x1080] [--fps 30]
"""
import argparse, json, os, re, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__)); TPL = os.path.join(HERE, "..", "assets", "template")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("folder"); ap.add_argument("--id", required=True)
    ap.add_argument("--duration", type=float, default=18.0); ap.add_argument("--size", default="1920x1080"); ap.add_argument("--fps", type=int, default=30)
    a = ap.parse_args()
    if not re.fullmatch(r"[a-z][a-z0-9-]*", a.id): sys.exit(f"--id {a.id!r}: lower-case letters, digits and hyphens only")
    m = re.fullmatch(r"(\d+)x(\d+)", a.size)
    if not m: sys.exit(f"--size {a.size!r}: use WIDTHxHEIGHT, e.g. 1920x1080 or 1080x1920")
    w, h = int(m[1]), int(m[2])
    if os.path.exists(a.folder) and os.listdir(a.folder): sys.exit(f"{a.folder} exists and is not empty")
    shutil.copytree(TPL, a.folder, dirs_exist_ok=True); shutil.copy(os.path.join(HERE, "sfxlib.py"), a.folder); shutil.copy(os.path.join(HERE, "cues.py"), a.folder)
    d = a.duration; hook, lock = round(d*.2, 2), round(d*.25, 2); body = round(d - hook - lock, 2)
    cues = {"id": a.id, "width": w, "height": h, "fps": a.fps, "duration": d, "bed": None, "bed_offset": 0.0, "bed_gain": 0.38,
            "scenes": [{"id": "hook", "start": 0.0, "dur": hook}, {"id": "moment", "start": hook, "dur": body}, {"id": "lockup", "start": round(hook+body, 2), "dur": lock}],
            "cues": {"open": {"t": 0.1, "sfx": "whoosh"}, "moment": {"t": round(hook+.3, 2), "sfx": {"kind": "thud", "gain": .9}},
                     "name": {"t": round(hook+body+.2, 2), "sfx": "chime"}},
            "voice": []}
    json.dump(cues, open(os.path.join(a.folder, "cues.json"), "w"), indent=2)
    p = os.path.join(a.folder, "index.html"); s = open(p).read().replace("__ID__", a.id).replace("__W__", str(w)).replace("__H__", str(h)).replace("__FPS__", str(a.fps)).replace("__DUR__", str(d))
    open(p, "w").write(s)
    print(f"{a.folder}: fill brief.md, then cues.json, then the scenes in index.html. Build with: python3 make.py")

if __name__ == "__main__":
    main()
