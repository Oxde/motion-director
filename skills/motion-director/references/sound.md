# Sound

Sound is cut to the same `cues.json` as the picture. `mix.py` in the project builds one
`assets/audio/mix.wav`; the page plays that single file.

## Layers

| Layer | Source | Level |
|---|---|---|
| Voice | Generated per line, pauses capped at 0.3 s, measured before any scene is timed | reference, 1.0 |
| Effects | Synthesized from `sfxlib.py`, one per cue that names an `sfx` | about 0.4 of voice |
| Music | A generated or supplied bed in `assets/audio/bed.*` | 0.3-0.45, ducked by 60% under voice |

"Music is too loud" is the most common note on any draft. Start lower than feels right.

## Voice first

1. Write the lines. Generate them. Cap pauses. Measure each with `ffprobe`.
2. Transcribe with word timestamps and cue visuals to the words that matter.
3. Only then set scene lengths in `cues.json`.
4. A line that is too long: speed it up to 1.15x, stretch the clip under it by up to 20%, rewrite
   it shorter, or lengthen the scene with `cues.py shift`. In that order.

## Music

- Ask for a genre that fits the product's world, and say "instrumental only" and a length.
- Change genre completely when asked to change the music; a variation reads as the same track.
- Find the drop by scanning loudness in short windows, then set `bed_offset` so it lands on the
  reveal. A bed whose energy arrives after the video ends makes the whole mix feel flat.
- Check length and energy before mixing: generated beds end early or run long.

## Effects that read

| Event | Effect |
|---|---|
| Text typing | one click per character at the typing speed |
| Element pops in | short pitched blip; rising pitch across a series |
| Something lands or stamps | low thud |
| Scene change | whoosh ending on the cut |
| Build-up to the moment | riser, then thud on the frame it lands |
| Success, reveal | three or four note chime |
| Failure | a recorded or generated sound, not a synthesized one: synthetic "sad" cues read as cheap |

## Mastering

Measure with `ffmpeg -hide_banner -i f -af loudnorm=print_format=json -f null -`. Bring the mix to
about -14 LUFS, limit, then measure the final MP4 again: encoding moves loudness and peak.

## Speech you cannot hear

You cannot listen. Transcribe every generated line and the final file. When a voice choice is
subjective, send short samples and let the person pick.
