# Brain Skeleton

## What this project is

A workspace that gives your AI agent company knowledge and reusable workflows in files you own.
Start with your company URL, and your agent will research the business and guide you through setup.

## Copy-and-paste install

Copy this prompt into your coding agent:

```text
Clone https://github.com/russelltaylor05/ecom-brain into a new, unused local folder.
Work inside it, read AGENTS.md, and follow skills/eb-setup/SKILL.md to set up my company.
```

## Start here

1. Create your own repository from these files (or a GitHub template), then clone your copy.
   If you cloned the starter directly, point `origin` at your own repository before enabling push.
2. Open the folder in your coding agent, preferably in a fresh session. Read its AGENTS.md and
   the startup files it references before beginning setup; a new session is optional.
3. Follow [project setup](skills/eb-setup/SKILL.md). Agents that read AGENTS.md start it
   automatically. To start or resume, say: **Read skills/eb-setup/SKILL.md and set up this project.**

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
