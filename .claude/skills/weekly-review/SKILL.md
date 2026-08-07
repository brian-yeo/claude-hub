---
name: weekly-review
description: Builds an end-of-week review from evidence rather than memory — what actually shipped (from git history), what slipped, what's blocked, and next week's top three, written to a dated file in personal/reviews/. Use on a Friday, at the start of a week, or when the user says "weekly review", "what did I get done this week", "wrap up the week", "plan next week", or "where did the week go".
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/git-week.sh) Bash(${CLAUDE_SKILL_DIR}/git-week.sh *)
---

# Weekly Review

Memory reports the week you *felt* you had — usually the last two days plus whatever went wrong. Gather evidence first, judge second.

## Standing rules

- **Be accurate, not encouraging.** This document has an audience of one and is only useful if it's true. "Three of five days went to unplanned work and the top three didn't move" is the review doing its job.
- **Don't manufacture a lesson** from a week that was simply fine.
- **Three means three.**

## Checklist

```
- [ ] 1. Gather evidence (git + last week's review + goals)
- [ ] 2. Categorize the week
- [ ] 3. Confront last week's top three
- [ ] 4. Check goals for staleness
- [ ] 5. Set next week's top three
- [ ] 6. Write the file
```

## 1. Gather

```bash
${CLAUDE_SKILL_DIR}/git-week.sh -s ~/code    # every repo under a directory
${CLAUDE_SKILL_DIR}/git-week.sh              # just the current repo
${CLAUDE_SKILL_DIR}/git-week.sh -d 14 -a ''  # two weeks, all authors
```

Then read, if they exist: `personal/reviews/` (last week's, specifically its top three), `personal/goals.md`, `personal/decisions/` (anything whose review date has come due), `personal/notes/` (this week's action items).

Ask once, as a single open question, for what git can't see: meetings, decisions, conversations, reading, non-code work, anything that ate a day and left no commit.

## 2. Categorize

- **Shipped** — done, merged, in someone's hands. Not "basically done."
- **Progressed** — real movement, not finished. Say what's left.
- **Slipped** — planned, didn't happen. Why is the whole point.
- **Dropped** — no longer doing it. Decision or drift?
- **Unplanned** — ate real time, was on no list. If this is most of the week, that's the finding.

## 3. Confront last week's top three

Mark each done / partial / not started, then answer **why not**. The honest answers call for different responses:

| Why it missed | What that means |
|---|---|
| Never started | Was it real, or aspirational? |
| Blocked on someone | Was the block raised, and when? |
| Displaced by unplanned work | More important, or just louder? |
| Too big for a week | It was a project, not a task. Rescope it. |

Something on the list three weeks running gets a different plan or gets dropped. Say so directly.

## 4. Goals

Mark which goals in `personal/goals.md` moved. Anything with no movement for three weeks gets a forced decision: **recommit** (with a next action this week), **rescope**, or **drop**. A goal you're not working on quietly taxes every future review.

## 5. Next week's top three

Three. Each must be **specific** (observable from outside), **finishable this week** (or named as the finishable slice), and **concretely started** (first action doable in an hour).

If none connect to a goal, say so in a sentence — sometimes correct, sometimes a signal.

## 6. Write it

Save to `personal/reviews/YYYY-MM-DD.md` using the Friday's date. Create the directory if needed.

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
- <thing> — <roughly what it cost>

## Last week's top three
| Planned | Outcome | Why |
|---------|---------|-----|

## Goals
| Goal | Moved? | Note |
|------|--------|------|
Anything stale 3+ weeks: recommit / rescope / drop, and which one.

## Next week's top three
1.
2.
3.

## Watch out for
What will bite next week if ignored.
```
