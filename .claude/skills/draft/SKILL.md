---
name: draft
description: Write a first draft or ruthlessly tighten an existing one, in the user's own voice as recorded in personal/voice.md. Use for emails, messages, posts, docs, proposals, announcements, and README copy, or when the user says "draft this", "write this up", "make this tighter", "cut this down", "does this sound like me", or hands over something wordy.
---

# Draft

Three modes. Work out which one applies from what the user gave you; ask only if it's genuinely unclear.

| They gave you | Mode |
|---|---|
| An intent, an audience, some points | **DRAFT** |
| Existing text that's too long or too soft | **TIGHTEN** |
| Samples of their own writing | **BUILD VOICE** |

## Always: load the voice first

Read `personal/voice.md` before writing a word. It holds how this person actually writes — sentence length, formality, what they never say, how they open and close.

If it doesn't exist, say so once and offer BUILD VOICE. Then write in a plain, direct register rather than guessing at a personality.

---

## Mode: DRAFT

Before writing, get these four straight. Ask only for what you genuinely can't infer — one round of questions, not an interrogation:

1. **Audience** — who reads this, and what do they already know?
2. **The ask** — what do you want them to do or decide? (If nothing, is this needed at all?)
3. **Register** — where does this sit between a Slack message and a signed document?
4. **Constraint** — length, format, anything that must or must not appear.

Then:

- **Lead with the point.** The first sentence carries the news or the ask. Context comes after, and only what's load-bearing.
- **One idea per paragraph.** If a paragraph needs "also", it's two paragraphs.
- **Concrete over abstract.** Names, numbers, dates, systems. "Significant improvement" says nothing; "cut p99 from 1.8s to 400ms" says it.
- **Make the ask explicit and singular.** Who does what by when. A message with three asks usually gets zero done.
- **Close with the next step**, not a pleasantry.

Deliver the draft, then a two-line note on the choices you made that the user might want to reverse.

---

## Mode: TIGHTEN

Cut hard. Most drafts lose 30–50% with no loss of meaning, and read stronger for it.

**Cut on sight:**
- Throat-clearing openers — "I wanted to reach out about", "Just circling back", "I hope this finds you well", "As you may know"
- Hedges stacked on hedges — "I think it might possibly be worth maybe considering"
- Meta-commentary — "In this section we will discuss", "It's worth noting that"
- Nominalizations — "make a decision" → "decide"; "provide assistance" → "help"
- Adverbs propping up weak verbs — "very quickly" → "fast"; "really important" → name the stake
- Passive voice hiding the actor — unless the actor genuinely doesn't matter
- Any sentence that restates the previous one with different words

**Do not cut:**
- Real uncertainty. If something is genuinely a guess, it stays hedged — false confidence is a worse sin than a wasted word.
- The specifics. Cutting "reduced latency 4x on the checkout path" to "improved performance" is not tightening, it's deleting the content.
- Warmth that's doing a job. A hard message with every softener stripped out reads as a threat.

**The rule:** never change what a sentence means to make it shorter. If a cut would, keep it and flag the bloat instead.

**Output:**
1. The tightened text
2. `<original> → <new> words`
3. What you cut and why — grouped by reason, not line by line
4. Anything you left alone that looks cuttable but isn't, with the reason
5. For the two or three highest-stakes sentences, an alternative phrasing to choose from

---

## Mode: BUILD VOICE

From 3–5 real samples the user wrote — emails, messages, docs, posts — extract a voice profile and write it to `personal/voice.md`.

Look for what's actually *characteristic*, not what's merely present:

- Sentence length and rhythm. Uniform, or varied with short punches?
- Openings and closings — what do they habitually do?
- Formality, and whether it shifts by audience
- Contractions, first person, questions to the reader, humor
- Punctuation habits — em dashes, semicolons, exclamation marks, lists
- Words they reach for repeatedly, and words they conspicuously never use
- How they deliver bad news, disagree, and say no

Quote real examples for each observation — a profile of adjectives is useless, a profile with three of their actual sentences under each point is not.

Write the profile, show it, and ask what's wrong with it. People recognize their own voice better than they can describe it, so the first pass is a draft to react to.
