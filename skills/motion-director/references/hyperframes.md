# HyperFrames: rules and fixes

Every frame must be a pure function of time. The renderer seeks to arbitrary frames; anything that
depends on what played before will be wrong in the final file.

Render: `npx hyperframes@0.8.33 check` then `render -o out.mp4 -q high -f 30|60`. Needs Node 22.

## Setup that fails first

| Symptom | Cause | Fix |
|---|---|---|
| `hyperframes` errors on start | Node < 22 | put a Node 22+ `bin` directory first on `PATH` (with nvm: `nvm use 22`) |
| `ModuleNotFoundError: numpy` | the Python on PATH has no numpy/Pillow | run the scripts with one that does (`pip install numpy pillow`) |
| Asset 404 in render | `../` paths | assets must sit under the composition folder; build templates in place |
| "more than one composition" | two root HTML files | keep ONE root `index.html`; templates go in `src/` |
| `audio_src_not_found` | mix not built yet | run the mix script before `check` |
| `console_error: AudioContext…` | flaky audio device in the check browser | transient: re-run; confirm the render has audio with `ffprobe` + loudnorm |

## Checker and seek rules

| Symptom / lint | Fix |
|---|---|
| Nothing animates | `window.__timelines["<id>"]` key must equal root `data-composition-id` |
| Element visible before its cue | CSS `opacity:0` + `fromTo` with `immediateRender:false`, destination must include `opacity:1` |
| `gsap_exit_missing_hard_kill` | the exit tween must END at least ~0.05s before its parent `.clip` ends, then `tl.set(el,{opacity:0}, t)` at a time still inside that clip |
| Text wrong after seek (typing, counters, label swaps) | proxy tween + `onUpdate` writing `textContent`. Never `tl.call()`; `tl.call(..) \|\| tl.set(..)` never runs the right side |
| `content_overlap` on intentional layers | `data-layout-allow-overlap` on EACH overlapping child, not just the clip |
| `text_occluded` under a vignette/scanline div | move overlays to `#root::before/::after`; flicker via `filter:brightness()` |
| `gsap_non_transform_motion` | animate `x/y`, not `left/top` |
| Contrast failures at a cut timestamp | transition-frame false positive; real ones persist across samples |
| Nested `<video>` in a UI frame is black | give it `class="clip"` + its own `data-start` (absolute composition time, same as its parent), `data-duration` and a `data-track-index` no other element uses; size it with an id selector |
| SVG group jumps or vanishes | never px `transformOrigin` on a `<g>` that has `transform`; use `svgOrigin` + bare wrapper `<g>` |
| Global `svg{}` rule blew up icons | scope it: `#stage>svg` |
| Odd-height PNG comes out 1px short | set the composition one pixel taller (675 → 676), grab with `-vf format=rgb24,crop=W:H:0:0` |

Many moving parts (swarms, ASCII, particles)? Drive everything from one `render(t)` and a single
proxy tween. See `hyperframes-patterns.md`.

## Time lives in cues.json

`window.CUES` holds `scenes` and `cues`. Read every tween time from it: `const c=CUES.cues; F("#logo",{…},{…},c.logo.t)`.
Elements that belong to a scene carry `data-scene="<id>"`; `make.py` rewrites their `data-start` and
`data-duration` from `cues.json` on every build, so never edit those attributes by hand.

## API quirks

| Symptom | Cause / fix |
|---|---|
| KIE upload returns 404 | uploads go to `kieai.redpandaai.co/api/file-base64-upload`, not `api.kie.ai`; files expire after 3 days |
| KIE `KeyError: resultUrls` on a finished video | image models return `{resultUrls}`, veo returns `{data:{result_urls}}`; handle both shapes when reading the result |
| KIE task `fail` with "Internal Error" on every voice model | their TTS was down for days; fall back to another provider for those lines and say so |
| Cost unknown | read `creditsConsumed` on the first finished task before queueing the rest |
| fal call returns 403 on a prompt | content filter, not balance; reword and retry |
| Image inputs | KIE needs public URLs (upload first); fal accepts data URIs |

Working snippets: `hyperframes-patterns.md`.
