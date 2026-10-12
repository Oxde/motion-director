"""Synthesized sound effects, one function per kind. Each returns a mono float array at SR."""
import numpy as np
SR = 44100
_rng = np.random.default_rng(7)
_t = lambda d: np.arange(int(d * SR)) / SR

def blip(f=880.0, d=.1):
    t = _t(d); return np.sin(2*np.pi*f*t*(1+.5*np.exp(-t*40))) * np.minimum(1, t/.003) * np.exp(-t/(d/3))

def key(d=.02):
    t = _t(d); return _rng.standard_normal(len(t)) * np.exp(-t*380) * .5

def thud(d=.45):
    t = _t(d); return np.sin(2*np.pi*(46+90*np.exp(-t*28))*t) * np.exp(-t*8)

def whoosh(d=.45):
    n = _rng.standard_normal(int(d*SR)); k = np.cumsum(n); k -= np.convolve(k, np.ones(40)/40, "same")
    return k/(np.abs(k).max()+1e-9) * np.sin(np.pi*_t(d)/d)**2

def riser(d=1.2):
    t = _t(d); sweep = np.sin(2*np.pi*np.cumsum(200+1400*(t/d)**2)/SR) * (t/d)**2 * .5
    return sweep + whoosh(d) * (t/d) * .6

def chime(notes=(1568, 1976, 2349, 3136), d=1.2):
    t = _t(d); out = np.zeros(len(t))
    for i, f in enumerate(notes):
        o = int(i*.055*SR); out[o:] += np.sin(2*np.pi*f*t[:len(t)-o]) * np.exp(-t[:len(t)-o]*3.2) * .3
    return out

def typing(chars, cps):
    """One click per character at `cps` characters a second."""
    out = np.zeros(int((chars/cps + .05) * SR)); k = key()
    for i in range(chars):
        o = int(i/cps*SR); out[o:o+len(k)] += k[:len(out)-o]
    return out

KINDS = {"blip": blip, "key": key, "thud": thud, "whoosh": whoosh, "riser": riser, "chime": chime}

def make(spec):
    """spec is a kind name, or {"kind": ..., plus that function's arguments, "gain": g}."""
    if isinstance(spec, str): spec = {"kind": spec}
    spec = dict(spec); kind = spec.pop("kind"); gain = spec.pop("gain", 1.0)
    if kind == "typing": return typing(spec["chars"], spec["cps"]) * gain
    if kind not in KINDS: raise SystemExit(f"unknown sfx kind {kind!r}; known: {sorted(KINDS)+['typing']}")
    return KINDS[kind](**spec) * gain
