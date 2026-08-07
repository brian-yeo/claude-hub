---
name: decision-log
description: Record a decision with its real context, the options considered, the actual reasoning, and what would change your mind — appended to personal/decisions/ with a review date. Use when the user makes or is weighing a consequential choice (architecture, tooling, vendor, hiring, commitments) or says "log this decision", "record this", "why did we choose X", "help me decide between", or revisits an old call.
---

# Decision Log

A decision record exists for one future moment: six months from now, when someone — probably you — asks *"why on earth did we do it this way?"* and the honest answer has been lost.

The whole value depends on **recording the real reason**. A sanitized record that lists three options and a tidy rationale is worse than no record, because it's confidently wrong about the past.

## Two modes

**DECIDE** — the choice is still open; help work through it, then log it.
**LOG** — the choice is made; capture it before the reasoning evaporates.

Also handle **REVISIT**: a past decision has come due or turned out badly.

---

## Mode: DECIDE

Work the problem before reaching for a template.

1. **What forces a decision now?** If nothing does, the best option is often to wait — and that's a decision worth logging too, with a date to revisit.
2. **What's actually being optimized for?** Speed, cost, reversibility, hiring, your own attention? Naming this usually settles the argument on its own.
3. **Generate a real third option.** Two options is nearly always a false binary, and the third is often "do neither yet" or "do the small version".
4. **Ask how reversible each one is.** A cheap, reversible choice deserves a fraction of the deliberation of a one-way door. Spending a week on a decision you could undo in an hour is itself a mistake.
5. **Steelman the one you don't like.** If you can't state the strongest case for the alternative, you haven't finished.
6. **Then recommend.** Give a clear recommendation with the reason, not a balanced survey. The user asked for help deciding.

---

## Entry format

Write to `personal/decisions/YYYY-MM-DD-<slug>.md` (create the directory if needed).

```markdown
# <Decision in a few words>
**Date:** <date> · **Status:** decided | provisional | superseded
**Reversibility:** easy | costly | one-way door

## The decision
One sentence. What we're doing.

## Context
What forced this now. The constraints that were real at the time — budget, deadline,
team size, what we already had. Write it for someone who wasn't there.

## Options considered
### <Option A> — chosen
The honest case for it.
### <Option B>
The honest case for it, and why it lost.
### <Option C>

## Why this one
The actual reason. If it was cost, say cost. If it was that nobody on the team knows
the alternative, say that. If it was politics, momentum, or a gut call, say that.

## What we're giving up
Every real decision costs something. If this section is empty, the options weren't real.

## What would change my mind
Concrete, checkable triggers: "if we pass 50k daily active users", "if the migration
takes more than two weeks", "if their pricing changes again". This is the part that
makes the record actionable later.

## Review on
<date>

## Outcome
*(left empty; filled in at review)*
```

## Rules

- **Record the unflattering reason.** "We picked it because we'd already started" is a legitimate and extremely common reason. Written down, it's a useful signal later. Dressed up as a technical argument, it will mislead someone.
- **Every entry gets a review date.** No exceptions. A decision with no review date is a decision nobody will ever revisit.
- **"What would change my mind" must be falsifiable.** "If it stops working well" is not a trigger. "If p99 goes over 500ms" is.
- **Never rewrite history.** When a decision is revisited, append an outcome and, if it changed, write a *new* entry that supersedes the old one and links back. The wrong turn is the most instructive part of the log.
- **Don't log trivia.** If it's cheap and reversible and nobody will ever ask, skip it. Logging everything is how a decision log dies.

## Mode: REVISIT

When a review date comes due or something goes wrong:

1. Read the original entry **before** forming a view — the point is to compare against what was actually predicted, not what you now remember predicting.
2. Did any "what would change my mind" trigger fire?
3. Fill in `## Outcome`: what happened, whether the reasoning held, and what was learned about *how the decision was made*, not just what was chosen.
4. If the decision is being reversed, write a new entry, set the old one's status to `superseded`, and link them in both directions.

Be fair to your past self: judge the decision by what was knowable at the time, not by how it turned out. A good call with a bad outcome is still a good call, and a lucky call is still a bad process.
