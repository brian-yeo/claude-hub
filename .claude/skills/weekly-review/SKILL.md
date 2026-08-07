---
name: weekly-review
description: End-of-week review built from evidence rather than memory — what actually shipped (from git history), what slipped, what's blocked, and next week's top three, written to a dated file in personal/reviews/. Use on a Friday, at the start of a week, or when the user says "weekly review", "what did I get done this week", "wrap up the week", "plan next week", or "where did the week go".
---

# Weekly Review

Twenty minutes that make the next week better. The failure mode is writing it from memory — memory reliably reports the week you *felt* you had, which is usually the last two days plus whatever went wrong.

So: **gather evidence first, then judge.**

## Procedure

### 1. Gather

```bash
.claude/skills/weekly-review/git-week.sh -s ~/code        # or pass repo paths
.claude/skills/weekly-review/git-week.sh                  # just the current repo
```

Then read, if they exist:
- `personal/reviews/` — last week's review, specifically its top three
- `personal/goals.md` — what this was all supposed to be in service of
- `personal/decisions/` — anything with a review date that has come due
- `personal/notes/` — action items from this week's meetings

Ask the user for what git can't see: meetings, decisions, conversations, reading, non-code work, anything that ate a day and left no commit. Ask once, as a single open question — don't interrogate.

### 2. Categorize honestly

- **Shipped** — done, merged, in someone's hands. Not "basically done."
- **Progressed** — real movement, not finished. Say what's left.
- **Slipped** — planned, didn't happen. **Why** is the whole point.
- **Dropped** — no longer doing it. Was that a decision or a drift?
- **Unplanned** — took real time and wasn't on any list. If this is most of the week, that's the finding.

### 3. Confront last week's top three

Pull last week's top three and mark each one done / partial / not started. Then the question that gives this practice its value: **why not?**

The honest answers are usually one of these, and they call for different responses:
- Never actually started → was it real, or aspirational?
- Blocked on someone → was the block raised, and when?
- Displaced by unplanned work → was that work more important, or just louder?
- Too big to finish in a week → it was a project, not a task; rescope it

Do not let a repeated miss slide by unexamined two weeks running. If something has been on the list three weeks, it either gets a different plan or gets dropped. Say so.

### 4. Check the goals

Read `personal/goals.md` and mark which goals moved this week. Anything with no movement for **three weeks** gets a forced decision: recommit (with a next action this week), rescope, or drop. Don't leave zombies on the list — a goal you're not working on is a goal that's quietly taxing every review.

### 5. Set next week's top three

Three. Not five, not "and a few small things."

Each one must be:
- **Specific** — you can tell from outside whether it's done
- **Finishable this week** — if it isn't, name the finishable slice of it
- **Started concretely** — the first action is something you could do in an hour

If the three don't connect to any goal, that's worth a sentence — sometimes correct, sometimes a signal.

### 6. Write it

Save to `personal/reviews/YYYY-MM-DD.md` (the Friday's date). Create the directory if it doesn't exist.

```markdown
# Week of <date>

## Headline
One sentence. What was this week actually about?

## Shipped
- <thing> — <where it landed>

## Progressed
- <thing> — <what's left, what's next>

## Slipped
- <thing> — <why, honestly>

## Unplanned
- <thing> — <roughly how much it cost>

## Last week's top three
| Planned | Outcome | Why |
|---------|---------|-----|

## Goals
| Goal | Moved? | Note |
|------|--------|------|
Anything stale for 3+ weeks: recommit / rescope / drop — and which one.

## Next week's top three
1.
2.
3.

## Watch out for
Blockers, risks, anything that will bite next week if ignored.
```

## Tone

Be straight with the user. This document is only useful if it's accurate, and it has an audience of one — there's nothing to be gained by making the week look better than it was. A review that says "three of five days went to unplanned support work and the top three didn't move" is doing its job; a cheerful one that buries that is not.

Equally: don't manufacture a lesson from a week that was simply fine.
