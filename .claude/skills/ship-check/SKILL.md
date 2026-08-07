---
name: ship-check
description: Pre-push self-review of a branch — catches scope creep, debug leftovers, committed secrets, missing tests, and weak commit messages before anyone else sees the diff. Use before pushing or opening a PR, or when the user says "ship it", "ready to push", "check my branch", "clean this up before I commit", "anything I'm forgetting", or is about to hand work to a reviewer.
---

# Ship Check

The last look before other people see your work. This is **hygiene, not bug-hunting** — the question isn't "is this correct", it's "would any of this embarrass me in review, or cost someone a round-trip".

Related but different, don't duplicate them:
- `/code-review` — hunts for defects and correctness problems
- `/simplify` — quality and reuse cleanups
- `/security-review` — a real security review of the change

## Procedure

### 1. Establish what "the change" is

Ask the user for the branch's intent in one sentence if it isn't already clear. You need it — most of this check is measuring the diff against that sentence.

### 2. Run the scanner

```bash
.claude/skills/ship-check/scan.sh          # or: scan.sh <base-ref>
```

It diffs the merge-base with the default branch against the working tree, so it covers committed, staged, and unstaged changes together. Every finding comes back as `file:line  |  content`.

The scanner is dumb on purpose. It finds candidates; **you triage**. Do not report its output back verbatim as if it were a verdict, and do not "fix" findings mechanically.

### 3. Triage each finding

For every hit, decide: **real problem**, **intentional**, or **false positive**. Read the surrounding code before deciding — a `console.log` in a CLI tool's output path is the feature.

Judgement calls the scanner can't make:
- `TODO` — fine if it's tracked and explains itself; not fine if it's a note-to-self about something unfinished in *this* change
- Hardcoded credential hits — check whether it's a real secret, a test fixture, or a variable named `password` holding nothing
- `.only` / `.skip` on tests — almost always accidental, occasionally deliberate and documented
- Large files and build output — sometimes genuinely committed on purpose

**If a real secret is in the diff, stop and say so first.** Note that removing it from the working tree isn't enough if it's already in a commit — the history needs rewriting and the credential needs rotating, because it must be treated as compromised the moment it's pushed.

### 4. Scope check — the one the scanner can't do

Read the diff yourself and hold every hunk against the branch's stated intent. Flag anything that doesn't serve it:

- Drive-by refactors, renames, and reformatting mixed into a feature change
- Config, lockfile, or formatting churn nobody asked for
- Files touched for no visible reason
- Two unrelated changes that should be two branches

Unrelated changes aren't wrong, they're *expensive* — they hide the real change from the reviewer. Offer to split them out.

### 5. Test check

- New behavior with no test covering it?
- Changed behavior where the tests didn't change at all? That's either a missing test or a test that was never checking the thing.
- Any test that was weakened, deleted, or skipped to make the branch pass?
- Do the tests actually run? Run them. Report real output — never assert a suite passes without having seen it pass.

### 6. Commit hygiene

- Does each message say **why**, not just what? The diff already shows what.
- `wip` / `fix` / `more` chains → offer to squash into a message that explains the change.
- Is there anything in the history you'd rather a reviewer not walk through commit by commit?

### 7. Report

Give a verdict and a short fix list, ordered by what would actually block a push:

```markdown
## Ship check: <branch>
**Intent:** <the one-sentence intent>
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

Then offer to fix the blocking items. Don't fix them silently as part of the check — the user asked for a review, and a review that quietly rewrites the thing being reviewed isn't one.
