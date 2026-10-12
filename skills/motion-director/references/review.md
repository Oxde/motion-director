# Review

Score each line 1-10 from the proof files in `out/proof/`, not from memory of what you built.
Write the evidence next to the score. Below 8: fix it, or say in the hand-over that it is below 8.

| Line | 8 means |
|---|---|
| **Idea** | A stranger can say what the video is about in one sentence, and that sentence would not fit a competitor |
| **The moment** | There is one frame you would use as the thumbnail, and the video builds to it |
| **First second** | Something is already happening on frame one; it is not a title card or a question |
| **Phone size** | Every word in `sheet-phone.jpg` is readable at 360 px wide without zooming |
| **Motion** | No scene is a still with text sliding in; something changes state in each |
| **Variety and contrast** | No two scenes share a layout; at least one is quieter than the rest |
| **Accuracy** | Every number, name and claim is in the brief with a source; nothing implies an endorsement |
| **Sound** | Voice is clear over music; effects land on visible events; loudness near -14 LUFS, peak under -1 dBTP |
| **Length** | Nothing could be cut without losing the idea |

## How to look

1. `sheet.jpg`: one frame just after each cue. Check for overlap, cut-off text, empty thirds,
   elements that arrived early.
2. `sheet-phone.jpg`: the same frames at phone width. Small labels fail here first.
3. `transcript.txt` (when there is speech): compare with the script. Small speech models mishear
   brand names; judge completeness and timing.
4. `report.txt`: duration, fps, loudness, true peak.

## Saying what you did not do

End `REVIEW.md` with a "Not checked" list. Typical honest entries: nobody listened to the mix;
the live API path was not exercised; the contract address and URL are placeholders. A review
that claims more than the proof files show is worse than no review.
