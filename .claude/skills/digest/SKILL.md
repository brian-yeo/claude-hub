---
name: digest
description: Compresses a pile of links, docs, papers, threads, or a reading backlog into one briefing — the claims that matter, where the sources disagree, and what to actually do about it. Use when the user dumps several URLs or files, has a backlog to get through, or says "summarize these", "what's the takeaway", "read this for me", "catch me up on X", or "is this worth reading".
---

# Digest

Many sources in, one briefing out. A digest that concatenates summaries has done nothing — the work is **cross-reading**: what do these sources agree on, where do they conflict, and what does that mean for the reader?

## Standing rules

- **Never summarize a source you couldn't actually read.** If it's paywalled, dead, or login-walled, say so and carry on. Never infer contents from a title or URL.
- **Every claim carries its source.** No orphan assertions.
- **Never average conflicting claims into a smooth consensus.** "Reports vary between 20% and 80%" is honest and useful; "roughly half" is neither.
- **Don't launder marketing into fact.** A vendor's number stays attributed to the vendor.
- **Separate what a source says from whether it's right.** Where you think a source is wrong, say so in your own voice, marked as your assessment.
- **Don't pad.** A five-source digest with one real finding should be short.

## Checklist

```
- [ ] 1. Read every source (note any that failed)
- [ ] 2. Grade each: date, author's stake, evidence vs assertion
- [ ] 3. Cluster by claim, not by source
- [ ] 4. Find and characterize the disagreements
- [ ] 5. Answer "so what"
```

## 2. Grade before you use

- **Date.** A confident claim from three years ago in a fast-moving area may simply be wrong now.
- **Who's talking and what do they get out of it.** A vendor benchmark, a competitor's teardown, and an independent replication are three different things wearing the same clothes.
- **Evidence or assertion?** Measured, cited, or just stated?

This grading is what makes the digest worth more than the sources.

## 3. Cluster by claim

Reorganize around the reader's questions. One theme may draw on five sources; one source may land in three themes. **If your section headings are the source names, this step didn't happen.**

## 4. Disagreements

The most useful part. Where sources conflict, characterize the conflict: different data, definitions, time periods, or incentives?

## Output

```markdown
# Digest: <topic>
*<n> sources · <date range> · compiled <date>*

## Bottom line
Three sentences maximum. If someone reads only this, what do they need?

## What's new or changed
Only when the reader already knows the topic. Skip otherwise.

## Key claims
| Claim | Source | Evidence | Confidence |
|-------|--------|----------|-----------|
Confidence: **solid** (measured/replicated) · **plausible** (reasoned, unverified) ·
**contested** (sources disagree) · **marketing** (from a party with a stake).

## Where sources disagree
The conflict, who's on each side, the most likely reason.

## What this means for you
The decisions or work this affects. "Interesting, not actionable" is a legitimate finding.

## Read in full / skip
| Source | Verdict | Why |
|--------|---------|-----|
Ranked. Be willing to say a source added nothing.

## Gaps
What none of these answered, and what would.
```

Offer to save to `personal/research/<topic>.md`.
