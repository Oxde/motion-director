# Patterns

Working snippets for the rules in `hyperframes.md`. Adapt, do not paste blindly.

## Composition skeleton

```html
<div id="root" data-composition-id="film" data-duration="18" data-width="1920" data-height="1080" data-fps="30">
  <video class="clip" data-start="0" data-duration="2.9" data-track-index="1" muted playsinline src="film/tap.mp4"></video>
  <div class="clip" id="ui" data-start="2.9" data-duration="2.1" data-track-index="1" data-layout-allow-overlap>…</div>
  <audio class="clip" data-start="0" data-duration="18" data-track-index="20" data-volume="1" src="assets/audio/mix.wav"></audio>
</div>
<script>
window.__timelines = window.__timelines || {};
const tl = gsap.timeline({paused:true});
window.__timelines["film"] = tl;                       // key === data-composition-id
const F=(el,from,to,t)=>tl.fromTo(el,from,{...to,immediateRender:false},t);
F("#card",{opacity:0,y:60},{opacity:1,y:0,duration:.4,ease:"expo.out"},2.95);   // destination carries opacity:1
tl.to("#card",{opacity:0,duration:.25},4.6); tl.set("#card",{opacity:0},4.9);   // exit ends before the clip does, then hard kill
tl.to({},{duration:18},0);                              // pins the timeline length
</script>
```

One mixed `mix.wav` on a single audio track is simpler than several `<audio>` clips and makes loudness measurable before render.

## Text that survives seeking

```js
const type=(sel,s,t,d)=>{const o={n:0}; tl.to(o,{n:s.length,duration:d,ease:"none",
  onUpdate:()=>{document.querySelector(sel).textContent=s.slice(0,Math.floor(o.n+1e-6));}},t);};
const n={v:0}; tl.to(n,{v:12.4,duration:1.1,onUpdate:()=>{bal.textContent="$"+n.v.toFixed(2);}},3.4);   // counter
const b={v:0}; tl.to(b,{v:1,duration:.02,onUpdate:()=>{btn.textContent=b.v>.5?"Posted":"Post";}},9.1); // label swap
```

## One `render(t)` for everything

For swarms, ASCII grids, particles: build elements once, then place every one from `t`.

```js
const P={t:0}; render(0);
tl.to(P,{t:D,duration:D,ease:"none",onUpdate:()=>render(P.t)},0);
// inside render: no Math.random(), no Date; use a seeded generator at init and hash(x,y,frame) for noise
const pop=(t,t0)=>{const d=t-t0; return d<0?0:d<.07?.45:d<.14?1.18:1;};   // stepped pop-in
const typed=(s,t,t0,cps=46)=>t<t0?"":s.slice(0,Math.floor((t-t0)*cps));
```

Several colours in a monospace grid: one `<pre>` per colour on the same cells, each with `data-layout-allow-overlap`.

## Overlays the checker accepts

A full-screen overlay `<div>` is read as an opaque layer over all text. Use pseudo-elements on the root:

```css
#root::before{content:"";position:absolute;inset:0;z-index:5;pointer-events:none;
  background:repeating-linear-gradient(0deg,rgba(0,0,0,.28) 0 2px,transparent 2px 4px)}      /* scanlines */
#root::after{content:"";position:absolute;inset:0;z-index:6;pointer-events:none;
  background:radial-gradient(ellipse 75% 70% at 50% 50%,transparent 60%,rgba(0,0,0,.65) 100%)} /* vignette */
```

## SVG

```js
gsap.set(group,{svgOrigin:"960 540"});      // not transformOrigin:"960px 540px"
// camera: wrap the world in a bare <g>, x = 960 - worldX*zoom, y = 540 - worldY*zoom
// undraw a line toward its start: strokeDashoffset 0 → +length
```

## ffmpeg traps

```bash
# stretch a clip: -t BEFORE -i (after it, the stretched output is truncated instead)
ffmpeg -t 2.9 -i clip.mp4 -vf "setpts=PTS*3.4/2.9,fps=30" -an out.mp4
# smooth slow-motion of the clean first half second
ffmpeg -t 0.52 -i clip.mp4 -vf "setpts=2.9*PTS,minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:vsbmc=1" -an out.mp4
# hold the last frame
ffmpeg -i clip.mp4 -vf "tpad=stop_mode=clone:stop_duration=0.6" out.mp4
# tighten VO pauses
ffmpeg -i line.mp3 -af "silenceremove=start_periods=1:start_threshold=-45dB:stop_periods=-1:stop_duration=0.3:stop_threshold=-45dB" line.wav
# loudness (needs the info log level; -v error hides it)
ffmpeg -hide_banner -i mix.wav -af loudnorm=print_format=json -f null -
# master: gain to target, then limit; re-measure the final mp4
ffmpeg -i mix_pre.wav -af "volume=${GAIN}dB,alimiter=limit=0.89:level=false" mix.wav
# exact odd-height still: the composition is 1200x676 (even), cropped to 675 after converting to RGB
ffmpeg -ss 0.5 -i raw.mp4 -frames:v 1 -vf "format=rgb24,crop=1200:675:0:0" card.png
```

zsh does not word-split unquoted variables: `for a in "x 0 4"; do set -- $a` passes one argument. Use a shell function with positional args.

## Mix recipe (numpy)

Synthesize SFX at the composition's cue times (blip, key click, thud, whoosh, riser, chime), load VO and bed with ffmpeg → float arrays, then:

```python
w=int(.15*SR); e=np.convolve(np.abs(vo),np.ones(w)/w,"same")           # voice envelope
duck=np.convolve(np.clip(e/.04,0,1),np.ones(int(.3*SR))/int(.3*SR),"same")
mix=bed*(1-.6*duck)*.3 + sfx*.4 + vo                                     # bed sits low; "music too loud" is the usual note
```

Find the bed's drop: RMS in 0.1s windows, pick the jump, set `OFF = drop_time - reveal_time`.

## Verifying without eyes or ears

```bash
python3 make.py            # writes out/proof/sheet.jpg and sheet-phone.jpg at every cue; read both
mlx_whisper out/film.mp4 --model mlx-community/whisper-base-mlx -f json --output-dir /tmp/wh   # compare segments with the script
ffprobe -v error -show_entries stream=codec_type,r_frame_rate,duration -of csv=p=0 out/film.mp4
```

The base Whisper model mishears brand names and slang ("YOLO calls" → "your locals"); judge timing and completeness, not spelling.

## Data-driven template (`make.py`)

1. `--latest` / `--id X` fetch the public API; `--data file.json` runs offline. API base from a flag or env var.
2. Validate: required fields present, status is the one that makes sense, colours match `#rrggbb`. Exit with the reason.
3. Download remote images into `assets/cache/` so the render never waits on a slow host.
4. `tpl.replace("__DATA__", json.dumps(data).replace("</","<\\/"))` → `index.html` in the same folder as the assets.
5. Synthesize SFX from constants shared with the template's timeline.
6. `hyperframes check`: stop only on `Check failed`, print warnings. Then render and master.
7. `.gitignore` the build outputs (`index.html`, `sfx.mp3`, `out/`, `assets/cache/`).

Finding a deployed backend when the repo has no URL: `curl` the site's JS bundle and grep for the API host.

## AI prompts that held a character

- Repeat one character lock and one style lock string in every still prompt; end with "No text, no letters, no logos, no watermark".
- Reference sheet first (front / three-quarter / side), then scene stills that take the sheet plus the brand asset as inputs.
- Image-to-video prompt: one action, "camera locked off", then the invariants ("keeps EXACTLY TWO arms", "the logo is a flat print that never changes").
- First+last-frame video (empty set → character in place) gives a clean materialize; expect a bad morph in the last second and cut it.
- Speech from the video model: put the line in quotes with a voice description, then transcribe to confirm it said it.
