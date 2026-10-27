# Brain Skeleton

A small, company-agnostic workspace for an AI agent to maintain company knowledge and project
skills. Bring your own coding agent with file and terminal access. Public web access helps build
the company profile; manual setup works without it. Git and Python 3.9+ are the only local tools
required. No paid API, business integration, or background service is required.

## Start here

1. Create your own repository from these files (or a GitHub template), then clone your copy.
   If you cloned the starter directly, point `origin` at your own repository before enabling push.
2. Open the folder in your coding agent.
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
