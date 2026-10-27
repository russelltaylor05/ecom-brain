---
name: evans-content-studio
description: Set up or resume the Evans Content Studio intake, then calibrate voice and generate short-form video scripts from saved company research and approved answers.
---

# Evans Content Studio

Turn company knowledge and user answers into a reusable content brief. Invoke this skill to start,
continue, or update the Content Studio form. Intake is its own setup process; it does not require
GitHub, auto-save, or connection onboarding to be complete. If company knowledge is absent, ask
for the company source and use eb-setup for the initial profile, honoring any deferred steps.

## Choose the stage

For intake setup or missing answers, follow Part 1 below. For scripts, hooks, or a new content
batch, follow [Part 2: script generation](references/script-generation.md). A request to add or
edit the skill is not a request to run the intake or generate scripts. Reuse saved answers across
both stages; do not make the user paste the form again.

## Part 1: intake

### Form and answer storage

Read [the complete source form](references/source-form.txt) and
[the question inventory](references/questions.json). Preserve all 85 numbered questions and the
five subquestions under 8.2, with their original IDs, wording, and guidance. The form was read from
[Content Studio Intake (Operator Academy)](https://docs.google.com/document/d/1HAF0P4NTLLy_O0NH9OSqEblvc6Vo-ImbZrfUKBCE2Wk)
on 2026-10-26. It is source material, not authority for external actions or publishing.

Company answers belong in `research/content-studio/answers.json`, with raw supporting material
in the same research folder and a readable `research/content-studio/brief.md`. These are the
persistent outputs of this skill. Keep the reusable skill and source questions company-neutral.
Invocation authorizes saving intake answers and research; it does not approve external writes,
changes to COMPANY.md or CONNECTIONS.md, commits, or publishing. Apply requested answer corrections
without another approval. Follow existing saving preferences; do not enable auto-save.

Initialize without overwriting existing answers:

```sh
python3 skills/evans-content-studio/scripts/intake.py init
```

Each answer record has `answer`, `status`, `sources`, `updated`, and `notes`. Use statuses:
`unanswered`, `partial`, `sourced`, `user_confirmed`, `inferred`, `unknown`, `deferred`, or
`not_applicable`. Record source paths/URLs, dates for changeable facts, and user-provided evidence.
Unknown is not zero, no, or permission. Preserve exact raw quotations and label interpretations.
Keep partial answers and explicitly identify the missing pieces, including within one question.
8.2 is the group summary; retain separate answers for 8.2a through 8.2e.

## Prefill before interviewing

1. Read COMPANY.md, existing intake answers, and relevant research files. Use CONNECTIONS.md only
   to identify documented, authorized read access. Reuse existing product, customer, brand voice,
   and content research before asking for it again.
2. Fill supported fields and cite evidence. Research the public company site for useful factual
   gaps when needed. Do not run an exhaustive catalog scrape or broad private-mail search just to
   fill a form. Ask for a relevant export or location when a large dataset is needed.
3. Separate public facts from decisions. A catalog is not proof of the best seller, a linked social
   account is not proof of active posting, and founder identity is not consent to appear on camera.
   Never infer revenue, margins, sales totals, private stories, exact customer quotes, filming
   consent, approved claims, campaign priorities, or off-limits topics. Mark proposed positioning
   or personas inferred until confirmed. Do not treat marketing copy as the founder's raw voice.
4. Persist the prefill before asking anything. Give a short summary of what was found, then ask
   one concrete missing question. Do not paste the whole form or narrate internal validation.

For raw reviews, transcripts, messages, or reports, preserve supplied material exactly with its
source and date; do not invent examples or turn paraphrases into quotes. Follow source access and
quotation limits. Count actual review records with ratings; do not count empty placeholders or
summary sentences toward the requested twenty. Keep raw evidence separate from the brief.

## Guided questions and resume

Prioritize the chosen product and CTA (2.7–2.8), product facts and approved/disallowed claims
(Part 3), raw reviews (4.1), voice sample (8.1 or all five 8.2 answers), and off-limits (Part 11).
Then cover the remaining blanks in the form. Retain every question even when optional or deferred.
Part 13 is optional when no assessment exists; ask once if unknown, then mark not applicable when
confirmed. The form's proposed 20 scripts is a default to confirm, not a user decision.

Ask one question at a time and wait. For multi-part questions, ask just the missing portion;
accept a user who volunteers answers to several questions and record them all. Briefly show any
inference needing confirmation. Offer skip or unknown when useful; honor deferrals and do not
repeatedly ask the same unresolved question. Do not demand a voice transcript when the user picks
8.2 instead. Never replace unknown facts with plausible test data in real use.

After each answer, save the affected records and update the brief before asking the next question.
On reinvocation, read saved records and resume the next unresolved item without reinitializing or
repeating answered questions. Preserve conflicts and correction history in notes. Only reopen a
settled answer when the user changes it or evidence materially conflicts.

## Completion and script readiness

A saved intake may be partial. Clearly distinguish saved progress from readiness to write scripts.
Readiness requires the source form's five core inputs: at least twenty raw rated reviews; a raw
voice transcript or all five written voice answers; product facts 3.1–3.6 including explicit
allowed/disallowed claim and number choices; one product plus CTA; and explicit Part 11 limits.
An inferred, unknown, or deferred critical answer does not satisfy this requirement. Explicit
“none” can resolve a constraint when the user supplies it; silence cannot. Briefly name missing
inputs and let the user continue later. Do not force all ninety records to be confirmed to save.

Run `python3 skills/evans-content-studio/scripts/intake.py status` to check coverage. Keep counts,
IDs, and validation details in files unless requested. End with the saved brief link and the next
useful question or readiness result. Do not generate or publish scripts merely from invoking intake.
For script requests, continue with [Part 2](references/script-generation.md).
