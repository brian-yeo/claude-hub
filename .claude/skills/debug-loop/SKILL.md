---
name: debug-loop
description: Applies disciplined debugging to a bug that has already survived a first attempt — forces a reliable reproduction, a written hypothesis log, and bisection instead of speculative edits. Use when stuck on a bug, when a fix didn't take, for flaky or intermittent failures, for "works locally, fails in CI", or when the user says "still broken", "I've tried everything", "why is this happening", "it only fails sometimes", or is on a third attempt at the same fix.
---

# Debug Loop

For bugs that resisted the obvious fix. The failure mode this prevents is **speculative editing**: changing plausible-looking code, re-running, and hoping. That turns a debugging problem into a debugging problem plus a diff full of unrelated changes.

## Standing rules

These hold for the entire session, not just the step they appear under:

- **No code change until there is a written hypothesis and a way to prove it wrong.** Guessing is allowed — write the guess down first, so a wrong guess teaches something instead of vanishing.
- **A symptom that disappears without an explanation is not fixed, it's moved.** Say so plainly rather than declaring victory.
- **Log actual values** — types, lengths, ids, null/undefined — not "got here". "Got here" only answers a question you could have answered by reading.

## Checklist

```
- [ ] 1. Inventory: exact symptom, what's been tried, when it last worked
- [ ] 2. Reliable reproduction
- [ ] 3. Hypothesis log started
- [ ] 4. Bisect — space and time
- [ ] 5. Instrument to distinguish hypotheses
- [ ] 6. Mechanism confirmed end to end
- [ ] 7. Fix + a test that fails before and passes after
- [ ] 8. Blast radius checked
```

## 1. Inventory

- Exact observed behavior — error text verbatim, exit code, stack trace. Not a paraphrase.
- What was expected, and what says so — a test, a spec, a report?
- What's been tried, and what happened each time. "No change at all" and "different error" mean very different things, and attempts that "didn't work" often contain the answer.
- When did it last work? Verified, or assumed?

## 2. Reproduce

The step people skip and the one that decides everything. **If you can't reproduce on demand, making it reproducible IS the task.** Do not proceed to fixing.

Drive toward: one command, seconds to run, fails every time.

For intermittent failures the missing variable is usually one of:

| Variable | How to force it |
|---|---|
| Ordering | Run the test alone vs. in suite; look for shared fixtures and global state |
| Timing | Races, timeouts, retries — anything with a sleep near it |
| Randomness | Pin the seed; unseeded RNG, hash order, generated ids |
| Environment | Versions, locale, timezone, CPU count, memory, filesystem case sensitivity |
| Data | A specific row, an empty collection, unicode, a very long value |
| Network | Real calls where there should be fakes |

When the failure rate changes, you've found it.

## 3. Hypothesis log

Maintain this in the conversation. It's the deliverable of a hard session even if the bug isn't found.

| # | Hypothesis | If true, I'd see… | Test | Result |
|---|-----------|-------------------|------|--------|
| 1 | | | | ✗ ruled out |
| 2 | | | | ✓ supported |

A hypothesis needs a falsifiable prediction. "Something's wrong with the cache" is a topic. "The cache key omits the tenant id, so two tenants collide — I'd see tenant B's data under tenant A's key" is a hypothesis.

## 4. Bisect

**Space:** check the value at the midpoint of the pipeline. Correct there? Half the search space is gone. Repeat. Four bisections through sixteen stages beats reading all sixteen.

**Time:** if it used to work, `git bisect run <command>` finds the commit mechanically. Faster than reasoning about which change did it, and *certain* where reasoning isn't.

## 5. Instrument

Add logging, asserts, or a breakpoint that **distinguishes between surviving hypotheses**. Instrumentation that looks the same under either hypothesis is wasted.

Remove it before shipping — `/ship-check` catches what you forget.

## 6. Confirm the mechanism

State the causal chain: this input, through this path, produces this state, which causes this symptom. Every link verified, none assumed.

## 7. Fix and prove it

- Write a test that **fails before and passes after**. Run it both ways; don't assume the "before" fails.
- Fix the cause. A null check that silences a crash is a symptom fix if the real question is why the value was null.

## 8. Blast radius

Does this bug class exist elsewhere? Grep for the pattern — a wrong cache key in one place is usually wrong in three.

Then close: what the cause was, and what would have caught it sooner — a test, a type, an assert, a lint rule. If the answer is "nothing", say that.

## Signs you're flailing

Stop and restart at step 2 if any of these are true:

- Three changes in a row that didn't move the symptom
- You can't say what you expect the next run to print
- You're re-reading the same file hoping it looks different
- The diff has grown changes unrelated to the bug
- You're changing things "to see what happens" — fine, but that's step 2, not step 6
- You're about to add a retry, a sleep, or a broad `try/except` and call it fixed
