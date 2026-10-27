---
name: eb-knowledge-updates
description: Propose root knowledge updates when work reveals new company facts, connections, or skills.
---

# Knowledge updates

At task completion, check whether durable discoveries are missing from or conflict with existing
knowledge. Read the relevant root files and subject-based research first. Skip minor details,
duplicates, and unsupported guesses.

- Company facts belong in COMPANY.md; supporting evidence and uncertainty belong in research/.
- Verified company accounts and access belong in CONNECTIONS.md. An available connector alone
  does not establish a company connection. Never record secrets.
- Reusable workflows belong in skills/; their index belongs in SKILLS.md.

For automatic SKILLS.md maintenance, follow
[eb-skill-authoring](../eb-skill-authoring/SKILL.md). The approval guidance below applies to
company and connection knowledge, not routine skill-index maintenance.

AGENTS.md owns the approval boundary for company and connection updates. Use its existing
authorization rather than adding another approval gate in this skill.

Present one decision at a time with the destination, exact proposed wording, and a short business
reason when useful. For example: `May I add "Every order includes free gift wrapping" to
COMPANY.md so future copy includes it?` Related edits may share one decision. Keep the question
focused on the proposed change; do not append skill links, instruction quotes, or internal-rule
explanations. Wait for the answer before presenting another proposal. Apply an explicitly
requested edit without asking for the same permission again.

After an authorized COMPANY.md edit, run:

```sh
python3 skills/eb-setup/scripts/setup_state.py record-profile
```

This refreshes the saved profile hash and preserves completed setup when its required inputs
remain valid. It does not complete unfinished setup. Do not rerun onboarding or reset answers
for an ordinary knowledge update.

Save supporting evidence and user decisions in the relevant research file under AGENTS.md's
shared knowledge rules. Record declined or deferred proposals there briefly. Do not repeat a
declined proposal without new evidence; revisit a deferred one only when relevant or requested.
Keep unresolved conflicts visible. Create no background watcher or separate proposal system.
