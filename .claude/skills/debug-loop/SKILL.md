---
name: debug-loop
description: Disciplined debugging for a bug that has already survived a first attempt — forces a reliable reproduction, a written hypothesis log, and bisection instead of speculative edits. Use when stuck on a bug, when a fix didn't take, for flaky or intermittent failures, for "works locally, fails in CI", or when the user says "still broken", "I've tried everything", "why is this happening", "it only fails sometimes", or is on their third attempt at the same fix.
---

# Debug Loop

For bugs that resisted the obvious fix. The failure mode this exists to prevent is **speculative editing**: changing plausible-looking code, re-running, and hoping. That converts a debugging problem into a debugging problem *plus* a diff full of unrelated changes.

## The rule

**No code change until there is a written hypothesis and a way to prove it wrong.**

If you can't say what you expect to happen and why, you're guessing. Guessing is allowed — but write the guess down first, so a wrong guess teaches you something instead of vanishing.

## Procedure

### 0. Stop and take inventory

Before touching anything:
- What is the exact observed behavior? Error text verbatim, exit code, stack trace — not a paraphrase.
- What was expected instead, and what says so — a test, a spec, a user's report?
- What's already been tried, and what exactly happened each time? Attempts that "didn't work" often contain the answer; "no change at all" and "different error" mean very different things.
- When did it last work? Is that verified or assumed?

### 1. Get a reliable reproduction

This is the step people skip and the one that decides everything. **If you can't reproduce it on demand, making it reproducible IS the task** — do not proceed to fixing.

Drive the repro toward: one command, runs in seconds, fails every time.

For intermittent failures, the variable you're missing is usually one of:
- **Ordering** — test pollution, shared fixtures, global state left behind by another test
- **Timing** — races, timeouts, retries, anything with a sleep near it
- **Randomness** — unseeded RNG, hash iteration order, generated IDs
- **Environment** — versions, locale, timezone, CPU count, available memory, filesystem case sensitivity
- **Data** — a specific row, an empty collection, a unicode or very long value
- **Network** — real calls where there should be fakes

Force each one: run the failing test alone vs. in suite, pin the seed, freeze the clock, run in CI's container locally. When the failure rate changes, you've found the variable.

### 2. Keep a hypothesis log

Maintain this table in the conversation, updating it as you go. It is the deliverable of a hard debugging session even if you never find the bug.

| # | Hypothesis | If true, I'd see… | Test | Result |
|---|-----------|-------------------|------|--------|
| 1 | | | | ✗ ruled out |
| 2 | | | | ✓ supported |

A hypothesis with no falsifiable prediction is not a hypothesis. "Something's wrong with the cache" is a topic; "the cache returns a stale value because the key omits the tenant id, so two tenants collide — I'd see tenant B's data under tenant A's key" is a hypothesis.

### 3. Bisect — in space and in time

**In space:** cut the system in half and find which half holds the bug. Check the value at the midpoint of the pipeline. Is it correct there? Half the search space is gone. Repeat. Four bisections through a 16-stage pipeline beats reading all 16.

**In time:** if it used to work, `git bisect run <command>` finds the commit mechanically. This is nearly always faster than reasoning about which change was responsible, and it is *certain* where reasoning is not.

### 4. Instrument rather than guess

Add logging, asserts, or a breakpoint that **distinguishes between the surviving hypotheses**. Logging that would look the same under either hypothesis is wasted.

Log the actual values — types, lengths, ids, `None`/`null`/`undefined` — not just "got here". "Got here" only ever answers a question you could have answered by reading.

Remove instrumentation before shipping (`/ship-check` will catch what you forget).

### 5. Confirm the mechanism before fixing

You must be able to state the causal chain: *this input, through this path, produces this state, which causes this symptom.* Every link verified, none assumed.

If a change makes the symptom disappear but you can't explain why, **you have not fixed it** — you've moved it. That is how a bug comes back next quarter as someone else's problem. Say so plainly rather than declaring victory.

### 6. Fix, then prove it

- Write a test that **fails before the fix and passes after**. Run it both ways; don't assume the "before" fails.
- Fix the cause, not the symptom. A null check that silences a crash is a symptom fix if the real question is why the value was null.
- Check the blast radius: does the same bug class exist elsewhere? Grep for the pattern. A wrong cache key in one place is usually wrong in three.

### 7. Close the loop

Briefly: what the cause was, why it took what it took to find, and what would have caught it sooner — a test, a type, an assert, a log line, a lint rule. If the answer is "nothing", say that too.

## Signs you're flailing

Stop and restart at step 1 if you notice any of these:

- Three changes in a row that didn't move the symptom
- You can't say what you expect the next run to print
- You're re-reading the same file hoping it will look different
- The diff has grown changes unrelated to the bug
- You've started changing things to "see what happens" — that's fine, but it means you're at step 1, not step 5
- You're about to add a retry, a sleep, or a broad `try/except` and call it fixed
