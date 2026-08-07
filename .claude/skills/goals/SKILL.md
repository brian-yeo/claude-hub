---
name: goals
description: Maintains and checks in on goals in personal/goals.md — keeps them written so progress is observable, reviews what actually moved, and forces a decision on anything stale. Use when the user sets a new goal, asks "how am I tracking", "what are my goals", "am I making progress on X", wants to drop or rewrite a goal, or at the start of a month or quarter.
---

# Goals

Most goal lists fail two ways: the goals are too vague to tell whether they moved, and dead goals are never removed, so the list becomes something to avoid looking at. This exists to prevent both.

## Standing rules

- **Read `personal/goals.md` first.** Create it from the format below if missing.
- **Maximum five active goals.** A sixth requires dropping one — make the user choose rather than growing the list silently. Five you're advancing beats twelve you're vaguely intending.
- **Never delete a goal outright.** Move it to Achieved or Dropped. The pattern in what gets dropped is worth more than any single goal.
- **Be direct about stalled goals without nagging.** Name it once, offer the three options, accept the answer. The user isn't accountable to you — the file just has to be true.

## Modes

**SET** (add or rewrite) · **CHECK** (review progress) · **CLOSE** (finish or drop)

---

## SET

A goal goes on the list only with all three of these. Push back until it has them — this is the useful part, not bureaucracy.

**1. An observable signal.** Someone outside your head can tell whether it moved.

| Vague | Observable |
|---|---|
| Get better at Rust | Ship one Rust service to production |
| Be more consistent about writing | Publish something twice a month |
| Improve the deploy process | Deploy takes under 10 minutes, no manual steps |
| Read more | Finish one book a month, logged |

**2. A horizon.** A goal without an end date can't be missed, so it can't be evaluated.

**3. A next physical action** — the specific thing doable in the next hour. If you can't name it, the goal needs decomposing, not motivation.

**Separate goals from projects and maintenance.** "Renew the domain" is a task. "Keep the tests green" is the job. Goals change the state of the world if they succeed.

---

## CHECK

1. What moved since the last check? Ask for **evidence, not a feeling** — a commit, a published thing, a number. `/weekly-review` output is good input.
2. Update `Last moved` on anything that moved.
3. Apply the staleness rule.
4. Report plainly: what's advancing, what's stalled, what needs a decision today.

### Staleness rule

**No movement in three weeks → forced decision.** One of:

- **Recommit** — it still matters. Needs a next action *this week*, and a reason it stalled. "I'll try harder" is not a reason.
- **Rescope** — it matters but it's too big, or the world changed. Rewrite it smaller.
- **Drop** — it doesn't matter enough right now.

Dropping is a success. Do not let a stale goal sit with no decision — surface it every time until it's resolved. That persistence is the entire mechanism.

---

## CLOSE

**Achieved:** move to `## Achieved` with the date and what actually resulted. Ask whether it was worth the effort — the answer shapes the next goal.

**Dropped:** move to `## Dropped` with one honest line. "Lost interest", "wrong priority", "solved another way" are all fine.

---

## File format

`personal/goals.md`:

```markdown
# Goals
*Last reviewed: <date>*

## Active

### <Goal>
- **Signal:** how anyone can tell this moved
- **By:** <horizon>
- **Next action:** <the specific next thing>
- **Last moved:** <date> — <what happened>
- **Why:** what this is in service of

## Achieved
- **<goal>** — <date>. <what came of it>

## Dropped
- **<goal>** — <date>. <why, in one honest line>
```
