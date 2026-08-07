---
name: decision-log
description: Records a decision with its real context, the options considered, the actual reasoning, and what would change your mind — appended to personal/decisions/ with a review date. Use when the user makes or is weighing a consequential choice (architecture, tooling, vendor, hiring, commitments) or says "log this decision", "record this", "why did we choose X", "help me decide between", or revisits an old call.
---

# Decision Log

A decision record exists for one future moment: months from now, when someone — probably you — asks *why on earth did we do it this way*, and the honest answer has been lost.

## Standing rules

- **Record the real reason, including the unflattering one.** "We picked it because we'd already started" is legitimate and extremely common. Written down, it's a useful signal. Dressed up as a technical argument, it will mislead someone. A sanitized record is worse than none, because it's confidently wrong about the past.
- **Every entry gets a review date.** No exceptions. A decision with no review date is one nobody will revisit.
- **"What would change my mind" must be falsifiable.** "If it stops working well" is not a trigger. "If p99 goes over 500ms" is.
- **Never rewrite history.** Append outcomes; supersede with a new entry rather than editing the old one. The wrong turn is the most instructive part of the log.
- **Don't log trivia.** Cheap, reversible, and nobody will ever ask? Skip it. Logging everything is how a decision log dies.

## Modes

**DECIDE** (still open) · **LOG** (already made) · **REVISIT** (review date came due, or it went wrong)

---

## DECIDE

Work the problem before reaching for the template.

1. **What forces a decision now?** If nothing does, waiting is often the best option — and worth logging, with a date to revisit.
2. **What's actually being optimized for?** Speed, cost, reversibility, hiring, your own attention? Naming this usually settles the argument on its own.
3. **Generate a real third option.** Two options is nearly always a false binary; the third is often "do neither yet" or "do the small version".
4. **How reversible is each?** A cheap reversible choice deserves a fraction of the deliberation of a one-way door. Spending a week on a decision you could undo in an hour is itself a mistake.
5. **Steelman the one you don't like.** If you can't state the strongest case for the alternative, you haven't finished.
6. **Recommend.** A clear recommendation with the reason, not a balanced survey — the user asked for help deciding.

---

## Entry format

Write to `personal/decisions/YYYY-MM-DD-<slug>.md` (create the directory if needed).

```markdown
# <Decision in a few words>
**Date:** <date> · **Status:** decided | provisional | superseded
**Reversibility:** easy | costly | one-way door

## The decision
One sentence.

## Context
What forced this now. The constraints that were real at the time — budget, deadline,
team size, what already existed. Write it for someone who wasn't there.

## Options considered
### <Option A> — chosen
The honest case for it.
### <Option B>
The honest case, and why it lost.
### <Option C>

## Why this one
The actual reason. If it was cost, say cost. If nobody on the team knows the
alternative, say that. If it was politics, momentum, or a gut call, say that.

## What we're giving up
Every real decision costs something. An empty section means the options weren't real.

## What would change my mind
Concrete, checkable triggers. This is what makes the record actionable later.

## Review on
<date>

## Outcome
*(empty until reviewed)*
```

---

## REVISIT

1. **Read the original entry before forming a view.** The point is comparing against what was actually predicted, not what you now remember predicting.
2. Did any "what would change my mind" trigger fire?
3. Fill in `## Outcome`: what happened, whether the reasoning held, and what was learned about *how the decision was made* — not just what was chosen.
4. Reversing it? Write a new entry, mark the old one `superseded`, link both directions.

Judge the decision by what was knowable at the time, not by how it turned out. A good call with a bad outcome is still a good call; a lucky call is still a bad process.
