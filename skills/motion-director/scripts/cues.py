#!/usr/bin/env python3
"""The one timeline. Read, print and move the times in a project's cues.json.

    cues.py show                      # the table: every scene and cue in order
    cues.py shift --from 7.6 --by 1.2 # move everything at or after 7.6s later by 1.2s (negative = earlier)
    cues.py scene <id> --dur 3.4      # change one scene's length and ripple everything after it
    cues.py check                     # scenes in order, no gaps or overlaps, cues inside the film

Run it in the project folder (or pass --file). make.py calls check on every build.
"""
import argparse, json, sys

def load(p):
    try: return json.load(open(p))
    except FileNotFoundError: sys.exit(f"{p} not found: run this in a project folder made by new_project.py, or pass --file")

def save(p, c):
    json.dump(c, open(p, "w"), indent=2); open(p, "a").write("\n")

def r(x): return round(x + 1e-9, 3)

def problems(c):
    out, prev_end = [], 0.0
    for s in c["scenes"]:
        if s["dur"] <= 0: out.append(f"scene {s['id']}: duration {s['dur']} is not positive")
        if abs(s["start"] - prev_end) > 0.0005: out.append(f"scene {s['id']} starts at {s['start']} but the previous scene ends at {r(prev_end)}")
        prev_end = s["start"] + s["dur"]
    if abs(prev_end - c["duration"]) > 0.0005: out.append(f"scenes end at {r(prev_end)} but duration is {c['duration']}")
    for k, v in c.get("cues", {}).items():
        if not 0 <= v["t"] <= c["duration"]: out.append(f"cue {k} at {v['t']} is outside 0..{c['duration']}")
    for v in c.get("voice", []):
        if not 0 <= v["t"] <= c["duration"]: out.append(f"voice {v['file']} at {v['t']} is outside the film")
    return out

def show(c):
    rows = [(s["start"], f"SCENE {s['id']}", f"{s['dur']}s  → {r(s['start']+s['dur'])}") for s in c["scenes"]]
    rows += [(v["t"], f"  cue {k}", v.get("sfx") if isinstance(v.get("sfx"), str) else (v.get("sfx") or {}).get("kind", "")) for k, v in c.get("cues", {}).items()]
    rows += [(v["t"], f"  voice {v['file']}", "") for v in c.get("voice", [])]
    for t, name, extra in sorted(rows, key=lambda x: (x[0], not x[1].startswith("SCENE"))): print(f"{t:7.3f}  {name:<28} {extra or ''}")
    print(f"{c['duration']:7.3f}  END  ({c['fps']} fps)")

def shift(c, frm, by):
    for s in c["scenes"]:
        if s["start"] >= frm - 1e-9: s["start"] = r(s["start"] + by)
        elif s["start"] + s["dur"] > frm + 1e-9: s["dur"] = r(s["dur"] + by)   # the scene the cut point sits in grows or shrinks
    for v in list(c.get("cues", {}).values()) + c.get("voice", []):
        if v["t"] >= frm - 1e-9: v["t"] = r(v["t"] + by)
    c["duration"] = r(c["duration"] + by)

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", default="cues.json"); sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("show"); sub.add_parser("check")
    sh = sub.add_parser("shift"); sh.add_argument("--from", dest="frm", type=float, required=True); sh.add_argument("--by", type=float, required=True)
    sc = sub.add_parser("scene"); sc.add_argument("id"); sc.add_argument("--dur", type=float, required=True)
    a = ap.parse_args(); c = load(a.file)
    if a.cmd == "shift": shift(c, a.frm, a.by)
    if a.cmd == "scene":
        m = [s for s in c["scenes"] if s["id"] == a.id]
        if not m: sys.exit(f"no scene {a.id!r}; scenes are {[s['id'] for s in c['scenes']]}")
        end = m[0]["start"] + m[0]["dur"]; shift(c, end, a.dur - m[0]["dur"]); m[0]["dur"] = r(a.dur)
    bad = problems(c)
    if a.cmd in ("shift", "scene"):
        if bad: sys.exit("not saved, the result would be inconsistent:\n  " + "\n  ".join(bad))
        save(a.file, c)
    show(c)
    if bad: sys.exit("\n" + "\n".join("✗ " + b for b in bad))

if __name__ == "__main__":
    main()
