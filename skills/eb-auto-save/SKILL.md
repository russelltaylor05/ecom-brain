---
name: eb-auto-save
description: Synchronize this workspace at session start and commit and push completed work when explicitly requested or enabled in local saving preferences.
---

# Auto-save

Run the setup status command in [eb-setup](../eb-setup/SKILL.md) and read `.brain/setup.json` if present. Missing,
incomplete, or invalid state means automatic saving is off. Explicit requests to commit or push
authorize that requested action independently. Automatic saving requires status to report
`complete: true`, both `auto_commit` and `auto_push` true, and a verified GitHub push destination.
Local-only settings mean automatic saving is off. Before an automatic commit, verify the confirmed
destination and push access. If a push fails, preserve the local commit and report the failure;
stop automatic saving until access is restored. Never silently fall back to local-only saving.
This skill does not enable or change saving preferences.

## Startup synchronization

Inspect status, current branch, upstream, and remotes. If origin exists, fetch it. On failure,
report the issue and continue local work when possible. With a clean worktree, fast-forward only
to the configured upstream (`git merge --ff-only @{upstream}`). If there is no upstream, local
work, or divergence, leave the checkout intact and report it. Never reset, automatically stash,
rebase, or resolve ambiguous conflicts as part of startup.

## Commit completed work

When a commit is authorized, review the diff and select only files belonging to the current task.
Preserve other sessions' changes, including staged changes; do not commit if their ownership is
unclear. Check ignored paths and new files for secrets. Exclude secrets, local setup state,
generated output, and unrelated work. Save logical finished work at task completion, not every
file edit. No changes means no commit.

Review the staged diff before committing. Use a short imperative subject and a body when the
reason is not obvious. Record attribution with Git trailers:

```text
Agent: <agent name>
Requested-by: <user name or routine identifier>
Tool: <agent host or tool>
```

Use `--trailer` arguments or a message file with actual newlines. Keep personal and customer data
out of messages. Use the existing Git identity; ask the user to configure one if it is missing.
Verify the resulting commit and status.

## Push authorized work

For automatic pushes, verify the current branch and the single origin push URL exactly match the
confirmed `branch` and `remote_url` in local setup state. A mismatch disables automatic push until
the user confirms the new destination. For an explicit push request, use the destination the user
authorized; clarify if it is ambiguous. Fetch before pushing; if the remote branch has commits
absent locally, stop and report rather than rewriting history. Use an explicit destination:
`git push origin HEAD:refs/heads/<confirmed-branch>`. Never force-push.

Do not modify Git identity or credentials. A failed commit or push remains pending; report the
failure and preserve local work. Report local commit and remote push separately. This workflow
runs within active agent sessions and creates no background service.
