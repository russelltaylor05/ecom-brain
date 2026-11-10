---
name: eb-vibe-editing
description: Set up Vibe Editing and render local captioned vertical clips without API keys, using supplied word timestamps and cuts.
---

# Vibe Editing

Use the pinned [Vibe Editing project](https://github.com/maddexritter-rgb/vibe-editing)
through this local adapter. Read [references/setup.md](references/setup.md) for dependencies,
onboarding differences, supported input files, and the boundaries of the smoke test.

Run commands from the company workspace root. Resolve the script relative to this skill if the
host opened it through a discovery link. Keep runtime files and generated media in root `tmp/`.

```sh
python3 skills/eb-vibe-editing/scripts/vibe.py setup
tmp/vibe-editing/.venv/bin/python skills/eb-vibe-editing/scripts/vibe.py doctor
tmp/vibe-editing/.venv/bin/python skills/eb-vibe-editing/scripts/vibe.py smoke
```

Setup downloads the pinned source and installs Pillow and FFmpeg in a private environment. It does
not run upstream setup, onboarding, credential loaders, or live editorial access. No external API
keys are needed. Do not ask for keys when the user chooses local mode. Do not interpret a local
doctor pass or synthetic smoke pass as a complete production onboarding pass.

For a real edit, read relevant shared `research/` files and existing brand decisions first. Reuse
the user's chosen brand and ask one missing question at a time only when needed. Default to the
bundled Montserrat style for a technical test; a test fixture is not a company brand decision.
Use a local video with audio, explicit cuts, and reviewed word timestamps relative to the CUT
timeline. The agent can supply caption emphasis. Automatic transcription and face tracking are
outside this local mode. Inspect the framing and captions before calling a real edit complete.

```sh
tmp/vibe-editing/.venv/bin/python skills/eb-vibe-editing/scripts/vibe.py render \
  --project tmp/my-clip
```

Use the smoke project's `manifest.json`, `10_WORK/cuts.json`, `words.json`, and `style.json` as
the working input example. Preserve its `pipeline: eb-local` value. The render engine keeps stage
caches and emits an MP4 and contract under `20_DELIVER/v1/`. Update a caption or cut source and
render again to rebuild dependent stages. Reports and setup progress stay in `tmp/`.

Keep AssemblyAI, Gemini, Groq, remote editorial access, and publishing/delivery marked skipped.
For a later request that needs those services, explain the missing capability and follow the
upstream connection guide only for the selected service. Never reuse bundled credentials or
machine credentials discovered by upstream helpers. Save durable company findings through the
shared knowledge workflow, not inside this skill or its runtime checkout.
