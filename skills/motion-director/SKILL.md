---
name: motion-director
description: Use when asked for a promo, launch video, teaser, explainer, reel, banner or "video for my project" that will be code-rendered (HTML + GSAP, HyperFrames), with or without AI clips, voice and music - especially when the first idea is a hook question, a feature list and a logo lockup, when a draft came back "generic", "boring", "slop" or "not it", or when a voice line, scene or cue has to move and picture and sound must stay in sync.
---

# Motion Director

A video is remembered for its idea and forgiven for its polish, never the other way round. This
skill makes you find the idea first, get it approved, then build it so it cannot drift.

**The order is the skill: world → idea → approval → cues → scenes → sound → proof.**
Building scenes before the idea is approved is the failure this skill exists to stop.

## 1. Read the product before you invent anything

Open the repo or site. Write down, with the file you took each from:

- the mechanic in one sentence (what happens, to whom, with what money or data)
- real copy: tagline, button labels, the words the product uses for itself
- palette, fonts, logo, mascot, UI components, any motion the product already has
- numbers, each with its source (config default, docs, live API)

Nothing reaches the screen that is not on this list or supplied by the user. Placeholders
(`<CA>`, `<site>`) stay visible placeholders and are reported at the end.

If all you have is a description: work from it, say that is all you read, and ask for the repo or
site in the approval message. If two spellings of the name appear, ask which is right.

## 2. Find the world

The look is not chosen from a menu. It is whatever this product already is: its terminal, its
pixel font, its mascot, its cards, its chat feed. If the product has no world at all (no logo, no
UI, no character), say so and make one small original thing for it - a character built from its
icon, a single object that carries the story - before reaching for a "clean SaaS" default.

## 3. One idea, from outside the category

Write three concepts, each as one line: **"It's <something from outside> for <the product's truth>."**
Outside means a film scene, a genre, a character's want, a physical metaphor, the product's own
mechanic acted out by characters. Then pick one and say why the other two lost.

A concept passes only if all three hold:

| Test | Fails when |
|---|---|
| Outside the category | all three options are motion-graphics devices (kinetic type, terminal, tile grid) |
| Not reusable | the same video would work for a competitor with the name swapped |
| Shows the mechanic | it talks about the product instead of showing the thing happen |

See `references/concept.md` for the patterns that have worked and the ones that never do.

## 4. Script it for the frame

One table: time, what happens, on-screen text, sound. Rules that survived real feedback:

- 15-20 seconds unless told otherwise. People ask for shorter far more often than longer.
- One moment the video exists for. Everything else sets it up or pays it off.
- Energy must change: at least one scene quiet enough that the moment lands.
- No list longer than 3 seconds. Nine tiles one per beat is a list, not a scene. When the product
  is "N things", show the count and the result at once, or three of them and "and six more";
  never read all N out.
- One short line of text per scene. If the picture already says it, cut the words.
- Every scene has an event: something spawns, breaks, fills, is rejected, changes state.
- If the product has no tagline, offer three end-card lines and mark your pick (`references/concept.md`, Slogans).

## 5. Stop for approval

Send the chosen concept, the script table, the music direction in one line (a genre chosen for
the idea's feeling, not for "promo"), and what you invented. If you made a new character or the
video uses AI footage, the reference sheet comes next: after the concept is approved, before any
scene. Then wait. Skip the wait only if the user has already said to go ahead. A wrong idea
caught here costs a message; caught after render it costs the whole build.

## 6. Build so it cannot drift

```bash
python3 <skill>/scripts/new_project.py <folder> --id <name> --duration 18
```

- `cues.json` is the only place a time is written. The page reads it (`window.CUES`), the mix
  reads it, `make.py` rewrites every `data-start` from it.
- Move things with `scripts/cues.py shift`, never by hand. Voice first: generate lines, measure
  them, then set scene lengths.
- Real assets beat generated ones; generated ones beat drawn-from-memory.
- Technical rules and every checker fix: `references/hyperframes.md`.
- AI stills, clips and voice: `references/ai-footage.md`. Sound: `references/sound.md`.

## 7. Prove it, then score it

`python3 make.py` renders and writes `out/proof/`: a sheet at every cue, the same sheet at
phone width (360 px), loudness, duration and - if there is speech - a transcript. Read all of it.
Then fill `REVIEW.md` using `references/review.md`. Ship only when every line is 8 or more,
or say plainly which line is not and why.

## 8. Hand over

Say what the video shows, what on screen is invented, what is missing (URL, CA, handle), what
it cost, and what you did not check. Then expect notes: "too long", "music too loud", "not that
line". Fix the note you were given, re-prove, re-send. Do not defend the draft.

## Red flags - stop and go back to step 3

- The first second is a question in bold type
- A scene exists to "list the features"
- You picked colours before reading the product
- All three concepts could be storyboards for any other tool
- You are writing scene code and nobody has seen the idea
- A real person, company or endorsement appears that the project does not have

## Honesty that is not optional

"Powered by X's models", never "by X". No cloned voices or generated likenesses of real people.
Claims like "infinite", "24/7", "every $N" are checked against config before they are animated.
Third-party interfaces are drawn in the project's own style and named in text only.
