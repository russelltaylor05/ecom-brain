# Company brain

Maintain company knowledge and reusable workflows. COMPANY.md identifies the company; do not infer
it from the starter repository owner or unrelated projects.

## Startup and saving

- Read [SOUL.md](SOUL.md), COMPANY.md, and SKILLS.md. Inspect `git status` and run the status
  command in [eb-setup](skills/eb-setup/SKILL.md).
- If setup is incomplete, automatically follow `skills/eb-setup`; resume saved progress.
  Handle unrelated explicit requests first; respect requests to skip or defer setup.
- Follow `skills/eb-auto-save` for synchronization and authorized saving. User instructions override
  preferences. No background jobs during setup.

## Shared knowledge

- When work reveals new company facts, connections, or skills, follow
  `skills/eb-knowledge-updates` to propose root-file updates and ask before applying them.
- All skills read and update shared findings, evidence, and decisions in `research/`. Reuse
  subject-based files; create them only when needed.
- Cite sources, date changeable claims, and distinguish facts, decisions, and hypotheses.
- Keep COMPANY.md concise. Setup writes the initial profile directly and summarizes findings and
  gaps. Propose later substantive updates for review; apply requested corrections.
  Preserve conflicting evidence and open questions.
- Read CONNECTIONS.md for access and verify company accounts. Never save credentials in tracked
  files or setup answers.

## Skills and corrections

- Follow `skills/eb-skill-authoring` when creating or updating skills; keep SKILLS.md current.
- Fix corrected work, then update its owning skill or script. Keep each rule in one place.
  Edit AGENTS.md only when explicitly requested.

## Writing and files

- Use clear, concise language. Wrap Markdown prose at 100 characters without breaking syntax.
- Use simplified technical English when writing internal documents and files.
- `skills/` holds portable workflows; `.agents/skills/` holds relative discovery links.
- Put drafts, logs, and generated output only in root `tmp/` (ignored by Git).
- `.brain/` holds local setup state and preferences (ignored by Git), never credentials.
