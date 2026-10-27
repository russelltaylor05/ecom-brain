# Brain Skeleton

## What this project is

A workspace that gives your AI agent company knowledge and reusable workflows in files you own.
Start with your company URL, and your agent will research the business and guide you through setup.

## Create your company workspace

1. Choose where you want to keep your company workspace and create an empty folder there.
2. Open that folder as a project in your coding agent, then start a new chat in it.
3. Paste this prompt:

```text
Download https://github.com/russelltaylor05/ecom-brain into this project folder, without
creating a nested folder. If it contains existing files, ask before proceeding.
Read AGENTS.md and follow skills/eb-setup/SKILL.md to set up my company.
```

Your agent will ask for your company URL and guide you through setup. Auto-save starts off.

Already cloned the repository? Open your chosen clone as a project and say:
**Read AGENTS.md and resume this project.**

## What is included

- [AGENTS.md](AGENTS.md): project behavior and startup instructions.
- [COMPANY.md](COMPANY.md): your sourced company profile.
- [CONNECTIONS.md](CONNECTIONS.md): verified services and access methods.
- [SKILLS.md](SKILLS.md): setup, Git saving, and skill-maintenance workflows.
- `research/`: shared company knowledge, evidence, and decisions that all skills read and update;
  created when there is substantive material to save. COMPANY.md holds the concise overview.
- `tmp/`: ignored drafts and output.
- `.brain/setup.json`: ignored, machine-local setup answers and saving preferences.

A fresh clone resumes the saved checklist and preserves existing company content. Automatic commits and
pushes are opt-in on each machine. They run while an agent works; there is no hourly background job.
Business-specific skills, integrations, and scheduled routines can be added later.

## Check the project

```sh
python3 skills/eb-skill-authoring/scripts/check-skills.py
python3 skills/eb-setup/scripts/setup_state.py status
```
