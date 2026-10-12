# AI stills, clips and voice

Use generated footage when the idea needs characters or places that code cannot draw. Everything
else - interface, numbers, captions, logos - stays in HTML where it is exact.

## Order

1. **Reference sheet** of each character from the project's own asset. Approve it.
2. **Scene stills**, each taking the sheet (or the previous approved still) as input. Read every one.
3. **Clips** from approved stills only. Read a contact sheet of every clip before using it.
4. One test clip first to learn the cost, then queue the rest in parallel.

## Keeping a character on model

- One character sentence and one style sentence, repeated word for word in every prompt.
- End still prompts with: no text, no letters, no logos, no watermark.
- Same set across shots: pass the approved shot first and say "exactly the same set, camera and scale".
- Edit from one prior still, not from a sheet, when a second copy of the character appears.
- A logo on a body is "a flat print that never changes". Say there are "exactly two arms".
- Defects in a clip almost always exist in its still. Fix the still.

## Clips

- One action per clip, "camera locked off", then the invariants.
- First-and-last-frame generation (empty set → character in place) makes a clean arrival; the last
  second often morphs. Cut it and cover the join with a flash.
- A clip that turns bad after N seconds: use the clean part, slow it with frame interpolation.
- Never let a clip invent text, a face on a card or a product screen. Reveal the real asset in HTML.
- A rejected prompt is usually wording. Soften the verb and retry before assuming a billing problem.

## Voice

- Stock or designed voices only. Never clone a real person's voice.
- Speech generated with the clip: quote the line, describe the voice, transcribe the result.
- Narration: generate each line separately so each can be timed and replaced.

## Real things first

Real inventory, real avatars, real card scans, the site's real icons and fonts beat anything
generated. Look in the repo and the public API before generating. When the repo has no deployed
URL, the site's JavaScript bundle usually names the API host.

## Likeness and endorsement

No generated likeness of a real person. A project's mascot may wear what its inspiration wears;
it may not be presented as that person. If the story needs "someone", use the mascot or hands.
