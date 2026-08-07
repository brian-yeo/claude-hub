---
name: notes-to-actions
description: Turn raw meeting or call notes into decisions, owned action items, open questions, and a ready-to-send follow-up. Use for messy notes from any meeting, call, standup, or interview, for a pasted transcript, or when the user says "clean up these notes", "what did we decide", "turn this into actions", "write up the meeting", or "who owns what".
---

# Notes → Actions

Raw notes into something that survives the week. The value is entirely in the separation: what was **decided**, what was **assigned**, and what is still **open** are three different things, and notes blur them together.

## Rules

**Never invent an owner or a date.** If the notes don't say who or when, write `UNASSIGNED` / `NO DATE` and put it in the follow-up as a question. A fabricated owner is worse than a blank one — blanks get chased, fabrications get ignored until they're late.

**Distinguish decided from discussed.** These read the same in notes and mean opposite things:
- *decided* — a choice was made and someone can act on it
- *discussed* — talked about, no conclusion
- *proposed* — one person's suggestion, not agreed
- *assumed* — everyone acted like it was settled but nobody said so

That last one is the most valuable thing you can surface. Flag it as an assumption to confirm.

**Preserve specifics exactly.** Numbers, names, dates, versions, dollar figures, and system names carry over verbatim. Don't round, don't paraphrase, don't tidy a "$40–60k" into "around $50k".

**Quote when the wording matters.** For commitments, objections, and anything contentious, quote the note verbatim rather than smoothing it. If a note is ambiguous, say it's ambiguous instead of picking a reading.

**Don't editorialize.** You're not summarizing what should have been decided.

## Output

```markdown
# <meeting> — <date>
**Present:** <names, or UNKNOWN>

## In short
Two or three sentences. What was this for, and where did it land?

## Decisions
| # | Decision | Decided by | Notes |
|---|----------|-----------|-------|
Only things actually settled.

## Actions
| Action | Owner | Due | Confidence |
|--------|-------|-----|-----------|
Confidence = **stated** (explicitly agreed in the notes) or **inferred** (you read it
between the lines — flag it so it gets confirmed).
Each action starts with a verb and names a finishable thing.
"Look into caching" is not an action. "Benchmark Redis vs in-process cache for the
session lookup, report by Thu" is.

## Open questions
| Question | Who can answer | Blocking? |
|----------|---------------|-----------|

## Assumptions to confirm
Things everyone seemed to take as settled that were never actually stated.

## Risks and flags
Anything that sounded like a problem in the making. One line each.

## Draft follow-up
A message ready to send to attendees: what we decided, who owns what by when, what's
still open. Short. If there are unassigned actions or unconfirmed assumptions, ask about
them directly in the message rather than burying them.
```

## Then

Offer to save it to `personal/notes/YYYY-MM-DD-<slug>.md`, and to feed the actions into `/weekly-review` at the end of the week. Say what you couldn't determine — a gap you name is a gap that gets filled.
