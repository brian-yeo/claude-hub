---
name: goals
description: Maintain and check in on goals in personal/goals.md — write them so progress is observable, review what actually moved, and force a decision on anything stale. Use when the user sets a new goal, asks "how am I tracking", "what are my goals", "am I making progress on X", wants to drop or rewrite a goal, or at the start of a month or quarter.
---

# Goals

Keeps `personal/goals.md` honest. Most goal lists fail the same two ways: the goals are written so vaguely that nobody can tell whether they moved, and dead goals are never removed, so the list becomes something to avoid looking at.

This skill exists to prevent both.

## Modes

**SET** — add or rewrite a goal · **CHECK** — review progress · **CLOSE** — finish or drop one

Always read `personal/goals.md` first. If it doesn't exist, create it from the structure below.

---

## Mode: SET

A goal goes on the list only if it has all three of these. Push back until it does — this is the useful part of the skill, not bureaucracy.

**1. An observable signal.** Someone outside your head can tell whether it moved.

| Vague | Observable |
|---|---|
| Get better at Rust | Ship one Rust service to production |
| Be more consistent about writing | Publish something twice a month |
| Improve the deploy process | Deploy takes under 10 minutes, no manual steps |
| Read more | Finish one book a month, logged |

**2. A horizon.** When does this stop being current? A goal without an end date can't be missed, so it can't be evaluated.

**3. A next physical action.** The specific thing you could do in the next hour. If you can't name it, the goal isn't ready — it needs decomposing, not motivation.

**Cap the list at five active goals.** Adding a sixth means dropping one; make the user choose rather than silently growing the list. Five things you're actually advancing beats twelve you're vaguely intending.

Separate **goals** from **projects** and **maintenance**. "Renew the domain" isn't a goal, it's a task. "Keep the tests green" isn't a goal, it's the job. Goals are things that change the state of the world if they succeed.

---

## Mode: CHECK

1. For each goal: what moved since the last check? Ask for evidence, not a feeling — a commit, a published thing, a number. `/weekly-review` output is good input here.
2. Update `Last moved` on anything that moved.
3. Apply the staleness rule below.
4. Report plainly: what's advancing, what's stalled, what needs a decision today.

### The staleness rule

**No movement in three weeks → the goal gets a forced decision.** One of:

- **Recommit** — it still matters. Then it needs a next action *this week*, and a reason it stalled. "I'll try harder" doesn't count as a reason.
- **Rescope** — it matters but it's too big or the world changed. Rewrite it smaller.
- **Drop** — it doesn't matter enough right now. Move it to `## Dropped` with one line on why.

Dropping is a success, not a failure. A list of five live goals is worth more than a list of twelve where seven are dead and everyone knows it.

Do not let the user leave a stale goal in place with no decision. Surface it every time until it's resolved — that persistence is the entire mechanism.

---

## Mode: CLOSE

**Achieved:** move to `## Achieved` with the date and what actually resulted. Ask whether the result was worth the effort — the answer shapes the next goal.

**Dropped:** move to `## Dropped` with one honest line. "Lost interest", "wrong priority", "solved another way" are all fine. Never delete a goal outright; the pattern in what you drop is worth more than any single goal.

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

## Tone

Be direct about stalled goals without being a nag about it. Name it once, clearly, offer the three options, and accept the answer. The user isn't accountable to you — the file just has to be true.
