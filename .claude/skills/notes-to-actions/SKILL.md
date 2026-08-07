---
name: notes-to-actions
description: Turns raw meeting or call notes into decisions, owned action items, open questions, and a ready-to-send follow-up. Use for messy notes from any meeting, call, standup, or interview, for a pasted transcript, or when the user says "clean up these notes", "what did we decide", "turn this into actions", "write up the meeting", or "who owns what".
---

# Notes → Actions

The value is in the separation: what was **decided**, what was **assigned**, and what is still **open** are three different things, and raw notes blur them together.

## Standing rules

- **Never invent an owner or a date.** Write `UNASSIGNED` / `NO DATE` and raise it in the follow-up. A fabricated owner is worse than a blank one — blanks get chased, fabrications get ignored until they're late.
- **Preserve specifics exactly.** Numbers, names, dates, versions, dollar figures, system names carry over verbatim. Don't round "$40–60k" into "around $50k".
- **Quote when the wording matters** — commitments, objections, anything contentious. If a note is ambiguous, say so rather than picking a reading.
- **Don't editorialize.** You're not summarizing what should have been decided.

## The distinction that matters

These read identically in notes and mean opposite things:

| Category | Meaning |
|---|---|
| **Decided** | A choice was made; someone can act on it |
| **Discussed** | Talked about, no conclusion |
| **Proposed** | One person's suggestion, not agreed |
| **Assumed** | Everyone acted as though it was settled, but nobody said so |

**Assumed** is the most valuable thing you can surface. Flag it as an assumption to confirm.

## Output

```markdown
# <meeting> — <date>
**Present:** <names, or UNKNOWN>

## In short
Two or three sentences. What was this for, where did it land?

## Decisions
| # | Decision | Decided by | Notes |
|---|----------|-----------|-------|
Only things actually settled.

## Actions
| Action | Owner | Due | Confidence |
|--------|-------|-----|-----------|
Confidence is **stated** (explicitly agreed) or **inferred** (read between the lines —
flag it for confirmation).
Each action starts with a verb and names a finishable thing. "Look into caching" is not
an action. "Benchmark Redis vs in-process cache for session lookup, report Thu" is.

## Open questions
| Question | Who can answer | Blocking? |
|----------|---------------|-----------|

## Assumptions to confirm
Taken as settled, never actually stated.

## Risks and flags
Anything that sounded like a problem in the making. One line each.

## Draft follow-up
Ready to send: what we decided, who owns what by when, what's still open. Short.
Ask directly about unassigned actions and unconfirmed assumptions rather than burying them.
```

## Then

Offer to save to `personal/notes/YYYY-MM-DD-<slug>.md`, and to carry the actions into `/weekly-review`. Say what you couldn't determine — a named gap is a gap that gets filled.
