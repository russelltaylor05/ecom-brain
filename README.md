# Brain Skeleton

## What this project is

A workspace that gives your AI agent company knowledge and reusable workflows in files you own.
Start with your company URL, and your agent will research the business and guide you through setup.

## Copy-and-paste install

Copy this prompt into your coding agent:

```text
Download https://github.com/russelltaylor05/ecom-brain into a new local folder for my company.
Use a Git clone and choose an unused folder; do not overwrite an existing project.
Remove the starter's origin remote so this copy cannot push back to the template repository.
After downloading, open the new project in a fresh agent context if your environment supports
it. Otherwise continue in the current context with the new folder as your working directory;
do not claim the context was reset. In either case, read the downloaded project's AGENTS.md
and the startup files it references before beginning setup. Follow those project instructions
and skills/eb-setup/SKILL.md. Ask me one question at a time and wait for my answer.
Keep auto-save off unless I explicitly enable it and we verify a repository I control.
Finish by showing me the local
project path and how to reopen it.
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
