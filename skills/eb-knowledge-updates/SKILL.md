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

Ask one question at a time across the conversation. Wait for the answer before asking another;
keep unrelated proposals for later. Related edits may share one yes/no approval when they form
one clear decision. Show the destinations, exact proposed wording, and why the edits matter.
Guide the user as through a simple form: give only the context needed to decide, ask a concise
question, and wait for their answer or explicit deferral before continuing the proposal. Do not
narrate internal deliberation or repeat the justification in progress updates or the final response.
Batch already-authorized work without asking again. A likely yes or silence is not approval.
Follow AGENTS.md for root knowledge updates. An explicit request for an edit
counts as approval; discovering information or creating a skill alone does not.
Keep any proposal concise and wait for the user's decision.

Save supporting evidence and user decisions in the relevant research file under AGENTS.md's
shared knowledge rules. Record declined or deferred proposals there briefly. Do not repeat a
declined proposal without new evidence; revisit a deferred one only when relevant or requested.
Keep unresolved conflicts visible. Create no background watcher or separate proposal system.
