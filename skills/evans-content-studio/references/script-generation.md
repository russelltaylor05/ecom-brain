# Part 2: script generation

Read [the complete script prompt](script-prompt.txt) before writing. It preserves the exact
copyable prompt supplied by the user on 2026-10-26. The surrounding social post is not part of
the prompt. Its examples and performance statistics are illustrative source claims, not verified
company evidence or numbers that may be used in a client's scripts.

Use the prompt's three stages with the saved intake rather than asking the user to paste a form.
The rules below adapt it to this workspace and resolve differences from the older form's writer
notes. Do not change the archived prompt to conceal these adaptations.

## Load the intake

Read COMPANY.md, research/content-studio/answers.json, brief.md, raw voice/review evidence, and any
prior calibration or performance notes. Check Part 1's readiness requirements. If a core input is
missing, ask for that input and save the answer; do not fabricate reviews, voice or claim approval.
The five written voice answers (8.2a–e) are a valid alternative to the transcript. Do not demand
both. An existing preference or quoted example is not consent to make new claims.

Use the user's current requested count, duration, formats, CTA choices and restrictions. The new
prompt's default for twenty scripts is 6 Unaware, 6 Problem Aware, 4 Solution Aware, 3 Product
Aware and 1 Most Aware, replacing the older form's four-per-level default. For another batch size,
propose a distribution totaling that count during calibration and honor any requested spread.
Do not silently substitute twenty for a smaller requested batch.

## Stage 1: calibrate and wait

Produce the prompt's six outputs: an evidence-based voice profile, three invented voice-test
sentences, customer avatars grounded in reviews, product and CTA, twelve numbered awareness-labeled
angles, and material gaps. Mark invented sample sentences as samples, not founder quotes. Do not
invent customer fears or identities when the review evidence does not support them.

Treat voice review as a creative question about the user's preferences. The user has already
requested scripts; they are reviewing the voice and direction, not granting tool permissions.
After showing the calibration, ask: “Do these samples sound like you, and are these the angles
you want?” End the message there and wait for their answer. Do not append a skill name, rule
quotation, explanation of why you are asking, or a reminder that drafting is paused. A link to
the calibration itself is useful; a link to internal instructions is not.

Save the calibration in research/content-studio/calibration.md with the batch preferences and
evidence. Do not draft scripts until the user confirms the voice and direction. A correction
alone is not confirmation: apply it, show the revision, and ask “Does this revised version fit?”
Then wait again. Save the actual confirmation and its scope. Silence and a previous unrelated
confirmation do not count; on resume, reuse it only for the unchanged calibration and scope.

## Stages 2 and 3: draft, check, deliver

After confirmation, write the requested batch using the prompt's full script structure: title,
awareness level, avatar, format, duration, hooks A/B/C (each with screen text and spoken line),
body, CTA, no-CTA alternate close, caption, shot list and explanation. If the user explicitly
requested only one ending, honor that preference and note it in the calibration. Every hook must
lead into the same body; each script must educate, demonstrate or inspire.

Check the batch before showing it, using all eight checks and the voice rules in the prompt.
Check duration against a plausible spoken read, not just word count: the prompt's 60–110 words
for thirty seconds is a drafting guide, not proof that a delivery fits. Respect the user's voice
and timing without forcing a rushed read. Review factual numbers separately from creative counts
such as script numbering, shot numbering and planned duration. Unsupported factual claims need
[FACT NEEDED] and must not be described as recording-ready. Never invent urgency, prices, results,
reviews, real customer stories, footage availability or consent to film people.

Save generated calibration previews, scripts and internal review output under a new
`tmp/content-studio/<batch-name>/` directory; do not overwrite prior batches. Keep the approved
calibration, intake updates, batch index and durable feedback in research/content-studio/.
The batch index should record output paths, intake/calibration used and any unresolved fact gaps.
If an ignored output file is missing on resume, say so instead of claiming it is still available.

Deliver a link to the scripts and a brief, honest note about the weakest scripts or missing
facts, as the prompt requests. Keep internal grading/checklists out of routine chat. Do not post,
message, schedule, create videos or change auto-save as part of writing scripts.

## Later performance feedback

When the user supplies performance data, preserve the actual metrics, dates, platform and hook
variant. Compare patterns without claiming causal proof from small samples. Save company-specific
lessons in research/content-studio/performance.md and use them for the next calibration. Do not
rewrite the reusable prompt or universal skill rules based on one company's results. Never treat
the source prompt's example view/comment counts as this company's performance.
