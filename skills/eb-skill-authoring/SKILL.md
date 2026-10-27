---
name: eb-skill-authoring
description: Add or maintain portable project skills, their index, and discovery links.
---

# Skill authoring

Keep each capability in `skills/<name>/SKILL.md` with YAML `name` and `description`. Use lowercase
letters, digits, and single hyphens, at most 64 characters. Prefix every packaged project skill
name with `eb-`, including its directory, frontmatter name, index label, and discovery link.
The user-named `evans-content-studio` is an explicit exception; preserve that name. Explain when the skill applies and
include only guidance that helps carry out that capability.

Add scripts, tests, references, or assets only when needed. Link supporting files from the skill.
Keep generated files under root tmp/. All skills must follow AGENTS.md's shared company knowledge
rules: read relevant `research/` files before company-specific work and save durable findings,
evidence, and decisions there. Update existing subject-based files rather than keeping skill-local
copies. Keep COMPANY.md as the concise sourced overview and connection details in CONNECTIONS.md;
do not embed company knowledge in reusable skill instructions. Create research files only when needed.

List the skill once in SKILLS.md and add a relative discovery link:
`.agents/skills/<name>` → `../../skills/<name>`. Do not install skills globally during setup.
Hosts that do not follow links can use SKILLS.md directly.

Maintain SKILLS.md automatically when adding, changing, renaming, or removing a project skill.
Index maintenance is part of the skill work and needs no separate approval. Keep entries accurate
and remove obsolete or duplicate entries. This authorization covers the skill index, not changes
to company facts or connections.

Run `python3 skills/eb-skill-authoring/scripts/check-skills.py` after changes, then exercise changed
scripts with meaningful behavior checks. The checker validates names, frontmatter, index entries,
and discovery targets; it does not prove the workflow is correct.
