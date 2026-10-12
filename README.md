# motion-director

An agent skill for promo videos that have an idea in them.

Most generated promos look alike: a question in bold, a feature list, a logo. This skill makes the
agent act as a director first. It reads the product, finds the world the product already has,
writes one idea from outside the category, gets it approved, and only then builds - on a single
timeline so picture and sound cannot drift.

```
world → idea → approval → cues → scenes → sound → proof
```

## What is inside

| Path | What |
|---|---|
| `skills/motion-director/SKILL.md` | The eight steps, the concept tests, the red flags |
| `references/concept.md` | How to find the idea: patterns that work, things that are not ideas |
| `references/review.md` | The nine-line review, scored from proof files |
| `references/hyperframes.md` + `hyperframes-patterns.md` | Renderer rules, checker fixes, working snippets |
| `references/ai-footage.md` | Stills, clips and voice when the idea needs characters |
| `references/sound.md` | Voice-first timing, music, effects, mastering |
| `scripts/new_project.py` | Scaffolds a project |
| `scripts/cues.py` | The one timeline: show, check, shift, resize a scene |
| `scripts/sfxlib.py` | Synthesized effects |
| `assets/template/` | `index.html`, `mix.py`, `make.py`, `brief.md`, `REVIEW.md` |

## Use

```bash
python3 skills/motion-director/scripts/new_project.py my-film --id my-film --duration 18
cd my-film
python3 cues.py show          # the timeline
python3 make.py               # sync → mix → check → render → master → out/proof/
python3 make.py --still 0.5   # a PNG instead of a film (banners, cards)
```

Needs Node 22+ (HyperFrames runs through `npx`), ffmpeg, and Python with numpy and Pillow.
A transcript is added to the proof when `mlx_whisper` or `whisper` is installed.

## Install

Claude Code:

```
/plugin marketplace add Oxde/motion-director
/plugin install motion-director
```

Or copy `skills/motion-director/` into `~/.claude/skills/`.

## Where it comes from

The rules are what survived making about fifteen launch videos, banners and data-driven cards and
having most first drafts sent back. The renderer is [HyperFrames](https://www.npmjs.com/package/hyperframes).

Three ideas are borrowed, as ideas, from [Mort1d/motion-graphics-skills](https://github.com/Mort1d/motion-graphics-skills):
one timeline shared by picture and sound, a phone-size readability check, and a scored review
before delivery. No code or text from that project is used here.

## License

MIT.
