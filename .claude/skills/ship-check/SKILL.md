---
name: ship-check
description: Reviews a branch before it is pushed — catches scope creep, debug leftovers, committed secrets, missing tests, and weak commit messages before anyone else sees the diff. Use before pushing or opening a PR, or when the user says "ship it", "ready to push", "check my branch", "clean this up before I commit", "anything I'm forgetting", or is about to hand work to a reviewer.
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scan.sh) Bash(${CLAUDE_SKILL_DIR}/scan.sh *)
---

# Ship Check

Hygiene, not bug-hunting. The question is not "is this correct" but "would any of this embarrass me in review, or cost someone a round-trip".

Adjacent skills, don't duplicate them: `/code-review` hunts defects, `/simplify` does quality cleanups, `/security-review` does a real security pass.

## Standing rules

These hold for the whole check, not just the step they appear under:

- **The scanner finds candidates; you triage.** Never report its output verbatim as a verdict.
- **Never fix findings silently.** The user asked for a review. A review that quietly rewrites the thing under review isn't one.
- **Never claim a test suite passes without having run it and seen it pass.**

## Checklist

```
- [ ] 1. Get the branch's intent in one sentence
- [ ] 2. Run the scanner
- [ ] 3. Triage each finding: real / intentional / false positive
- [ ] 4. Scope check every hunk against the intent
- [ ] 5. Test check
- [ ] 6. Commit hygiene
- [ ] 7. Verdict + fix list
```

## 1. Intent

Ask for it if it isn't clear. Most of this check measures the diff against that one sentence, so guessing it wastes the whole pass.

## 2. Scan

```bash
${CLAUDE_SKILL_DIR}/scan.sh              # base defaults to origin/HEAD
${CLAUDE_SKILL_DIR}/scan.sh <base-ref>
```

Covers committed, staged, and unstaged changes together. Findings come back as `file:line  |  content`.

## 3. Triage

For every hit: **real problem**, **intentional**, or **false positive**. Read the surrounding code before deciding — a `console.log` on a CLI's output path is the feature.

Calls the scanner can't make:

| Finding | The judgement |
|---|---|
| `TODO` | Fine if tracked and self-explanatory. Not fine if it's about something unfinished in *this* change. |
| Hardcoded credential | Real secret, test fixture, or a variable named `password` holding nothing? |
| `.only` / `.skip` | Almost always accidental. Occasionally deliberate and documented. |
| Large file / build output | Sometimes genuinely committed on purpose. |
| Debug statement | Is this the program's output, or a leftover? |

**If a real secret is in the diff, stop and lead with that.** Removing it from the working tree is not enough once it's in a commit: the history needs rewriting and the credential must be rotated, because it is compromised the moment it's pushed.

## 4. Scope

Hold every hunk against the intent. Flag drive-by refactors, renames, reformatting, config and lockfile churn, and files touched for no visible reason.

Unrelated changes aren't wrong — they're expensive, because they hide the real change from the reviewer. Offer to split them out.

## 5. Tests

- New behavior with no test covering it?
- Changed behavior where tests didn't change at all? Either a missing test, or a test that was never checking the thing.
- Any test weakened, deleted, or skipped to make the branch pass?
- Run them. Report real output.

## 6. Commits

- Does each message say **why**? The diff already shows what.
- `wip` / `fix` / `more` chains → offer to squash into one message that explains the change.
- Anything in the history a reviewer shouldn't have to walk through commit by commit?

## 7. Verdict

```markdown
## Ship check: <branch>
**Intent:** <one sentence>
**Verdict:** ready / fix first / don't push

### Blocking
- <thing> — `file:line` — why it blocks

### Worth fixing
- <thing> — `file:line`

### Noted, no action
- <finding> — why it's fine

### Scope
<in scope / these N hunks belong on a separate branch>

### Tests
<what you ran, what happened>
```

Then offer to fix the blocking items. After fixing, **re-run the scanner** — a fix can introduce a new finding, and the clean run is the evidence that the branch is actually ready.
