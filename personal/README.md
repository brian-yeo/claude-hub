# personal/

Working files for the Claude Code skills in [`.claude/skills/`](../.claude/skills/). The skills read from here for context and write their output back here, so the state builds up over time instead of evaporating at the end of each session.

## Layout

| Path | Written by | What it holds |
|------|-----------|---------------|
| `voice.md` | `/draft` | How you write — used so drafts sound like you, not like an assistant |
| `goals.md` | `/goals` | Active goals with an observable signal and a next action |
| `reviews/` | `/weekly-review` | One dated file per week |
| `decisions/` | `/decision-log` | One file per decision, each with a review date |
| `notes/` | `/notes-to-actions` | Cleaned-up meeting notes with owned actions |
| `research/` | `/digest` | Briefings compiled from multiple sources |
| `repo-maps/` | `/repo-onboard` | Maps of codebases you've onboarded to |

Directories are created on first use — nothing to set up.

## Start here

1. `/goals` — set two or three goals. The skill will push back until each has a signal you can actually observe.
2. `/draft` — hand it 3–5 things you've written and ask it to build your voice profile. Everything `/draft` produces afterwards is meaningfully better for it.
3. `/weekly-review` on Friday. It reads your git history and last week's review, so the second one is more useful than the first, and the fifth is more useful again.

The compounding ones are `reviews/`, `decisions/`, and `goals.md` — they're worth more the longer they run, because each review compares against the last.

## A note on privacy

The repo README describes claude-hub as shared with a team. **If anyone else has access to this repo, anything committed under `personal/` is visible to them** — goals, decision reasoning, meeting notes, and drafts included.

Three reasonable options:

- **Keep it here** if the repo is effectively yours, or the content isn't sensitive.
- **Ignore it locally** — add `personal/` to `.gitignore`. Note the trade-off: nothing under it is backed up or synced, and it won't exist in a fresh clone or a cloud session.
- **Split it out** — keep `personal/` in a private repo and clone it alongside. Best of both, one more thing to manage.

Decide before the first commit that contains something you'd rather not share. The skills work the same either way.
