---
name: digest
description: Compress a pile of links, docs, papers, threads, or a reading backlog into one briefing — the claims that matter, where the sources disagree, and what to actually do about it. Use when the user dumps several URLs or files, has a backlog to get through, or says "summarize these", "what's the takeaway", "read this for me", "catch me up on X", or "is this worth reading".
---

# Digest

Many sources in, one briefing out. A digest that just concatenates summaries has done nothing — the work is in **cross-reading**: what do these sources agree on, where do they conflict, and what does that mean for the person reading?

## Procedure

### 1. Read them properly

Fetch every source. If one can't be fetched — paywall, dead link, login — say so explicitly and carry on. Never summarize a source you couldn't actually read, and never infer its contents from its title or URL.

### 2. Grade each source before you use it

For each, note:
- **Date.** A confident 2023 claim about a fast-moving area may be simply wrong now.
- **Who's talking and what do they get out of it.** A vendor benchmark, a competitor's teardown, and an independent replication are three different things wearing the same clothes.
- **Evidence or assertion?** Measured, cited, or just stated?

This grading is what makes the digest worth more than the sources.

### 3. Cluster by claim, not by source

Reorganize around the questions the reader actually has. One theme may draw on five sources; one source may land in three themes. If your section headings are the source names, you haven't done this step.

### 4. Find the disagreements

The most useful part of any digest. Where sources conflict, **say so and characterize the conflict** — different data, different definitions, different time periods, different incentives?

Never average conflicting claims into a smooth consensus. "Reports vary between 20% and 80%" is honest and useful; "roughly half" is neither.

### 5. Make it actionable

Answer the question behind the question: what should the reader *do* or *decide* differently now?

## Output

```markdown
# Digest: <topic>
*<n> sources · <date range> · compiled <date>*

## Bottom line
Three sentences, maximum. If someone reads only this, what do they need?

## What's new or changed
Only if the reader is already familiar with the topic — what's different from the
prior understanding. Skip this section if it doesn't apply.

## Key claims
| Claim | Source | Evidence | Confidence |
|-------|--------|----------|-----------|
Confidence: **solid** (measured/replicated) · **plausible** (reasoned, unverified) ·
**contested** (sources disagree) · **marketing** (from a party with a stake).

## Where sources disagree
The conflict, who's on each side, and the most likely reason for it.

## What this means for you
The decisions or work this actually affects. If it affects nothing yet, say that —
"interesting, not actionable" is a legitimate and useful finding.

## Read in full / skip
| Source | Verdict | Why |
|--------|---------|-----|
Ranked. Be willing to say a source added nothing.

## Gaps
What none of these sources answered, and what would.
```

## Rules

- **Every claim carries its source.** No orphan assertions.
- **Don't launder marketing into fact.** A vendor's number stays attributed to the vendor.
- **Flag staleness.** If the best source is two years old in a fast area, that's a finding.
- **Don't pad.** A five-source digest that honestly has one real finding should be short.
- **Separate what a source says from whether it's right.** Where you think a source is wrong, say so in your own voice, marked as your assessment.

Offer to save to `personal/research/<topic>.md`.
