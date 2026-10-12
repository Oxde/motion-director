#!/usr/bin/env python3
"""Voice + effects + music, all placed from cues.json → assets/audio/mix.wav at about -14 LUFS.

Effects: every cue with an "sfx" (a kind name, or {"kind", args, "gain"}; kinds are in sfxlib.py).
Voice:   cues.json "voice": [{"file": "vo/n1.wav", "t": 0.3}]
Music:   cues.json "bed": "assets/audio/bed.mp3", "bed_offset" seconds into the bed, "bed_gain".
"""
import json, os, re, subprocess, sys, wave
import numpy as np
import sfxlib
HERE = os.path.dirname(os.path.abspath(__file__)); SR = sfxlib.SR

def load(path):
    if not os.path.exists(path): sys.exit(f"audio file not found: {path}")
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)

def loudness(path):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "loudnorm=print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = re.search(r"\{[^{}]*\}", err, re.S)
    if not m: sys.exit(f"could not measure loudness of {path}:\n{err[-600:]}")
    j = json.loads(m.group()); return float(j["input_i"]), float(j["input_tp"])

def main():
    c = json.load(open(os.path.join(HERE, "cues.json"))); D = c["duration"]; N = int(SR * D)
    def put(buf, x, t, g=1.0):
        i = int(t * SR)
        if i >= N: return
        x = x[:N - i]; buf[i:i + len(x)] += x * g
    sfx = np.zeros(N); vo = np.zeros(N); bed = np.zeros(N)
    for name, cue in c.get("cues", {}).items():
        if cue.get("sfx"): put(sfx, sfxlib.make(cue["sfx"]), cue["t"])
    for v in c.get("voice", []):
        x = load(os.path.join(HERE, v["file"])); put(vo, x / (np.abs(x).max() + 1e-9) * .9, v["t"], v.get("gain", 1.0))
    if c.get("bed"):
        b = load(os.path.join(HERE, c["bed"])); s = int(np.argmax(np.abs(b) > .01)) + int(c.get("bed_offset", 0) * SR)
        b = b[s:s + N]
        if len(b) < N * .98: print(f"warning: music covers {len(b)/SR:.1f}s of a {D}s film from offset {c.get('bed_offset',0)}s")
        bed[:len(b)] = b
    t = np.arange(N) / SR
    w = int(.15 * SR); env = np.convolve(np.abs(vo), np.ones(w) / w, "same")
    duck = np.convolve(np.clip(env / .04, 0, 1), np.ones(int(.3 * SR)) / int(.3 * SR), "same")
    bed *= (1 - .6 * duck) * np.clip((D - t) / 1.0, 0, 1) * np.minimum(1, t / .05) * c.get("bed_gain", .38)
    mix = bed + sfx * .4 + vo
    if np.abs(mix).max() < 1e-6: sys.exit("the mix is silent: cues.json has no sfx, voice or bed")
    mix = mix / np.abs(mix).max() * .9
    os.makedirs(os.path.join(HERE, "assets", "audio"), exist_ok=True)
    pre = os.path.join(HERE, "assets", "audio", "mix_pre.wav"); dst = os.path.join(HERE, "assets", "audio", "mix.wav")
    with wave.open(pre, "wb") as f:
        f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes((np.stack([mix, mix], 1) * 32767).astype(np.int16).tobytes())
    lufs, _ = loudness(pre)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", pre, "-af", f"volume={-14 - lufs:.2f}dB,alimiter=limit=0.89:level=false", dst], check=True)
    os.remove(pre); lufs, tp = loudness(dst); print(f"mix: {D}s, {lufs:.1f} LUFS, true peak {tp:.1f} dBTP")

if __name__ == "__main__":
    main()
