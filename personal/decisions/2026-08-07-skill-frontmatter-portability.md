# Keep skill frontmatter inside the Agent Skills spec
**Date:** 2026-08-07 · **Status:** decided
**Reversibility:** easy

*Written by `/decision-log` as its own worked example. Delete it if you don't want it in your log — the format is what matters, not this entry.*

## The decision

The skills in `.claude/skills/` use only the six frontmatter fields the Agent Skills spec allows (`name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`), even though Claude Code accepts about twenty.

## Context

Claude Code reads a much larger frontmatter set than the portable spec: `context: fork`, `model`, `effort`, `disable-model-invocation`, `argument-hint`, `paths`, `when_to_use` and more. They work on the filesystem and several are genuinely useful here.

The constraint is on the other end. claude.ai uploads, the Skills API, and enabling a personal skill for Cowork and cloud sessions all validate against the six-field spec and **fail with a hard error** on any extra key, rather than ignoring it. So the choice was between richer behavior now and the option to move these skills elsewhere later.

This repo is a shared hub whose stated primary platform is claude.ai Projects, which made the portability side heavier than it would be for a private project.

## Options considered

### Six spec fields only — chosen
Works everywhere without modification. Loses some Claude Code-specific behavior.

### Use whatever Claude Code accepts
`context: fork` would run `digest` and `repo-onboard` in a forked subagent, keeping their heavy file and web reading out of the main conversation's context — a real win for exactly the two skills that read the most. `argument-hint` would improve autocomplete. Both are lost if the skill ever needs to leave Claude Code, and the failure is a packaging error rather than a graceful degradation.

### Split: portable core, Claude Code-only variants
Rejected as premature. Two copies of nine skills to keep in sync, to solve a problem nobody has yet.

## Why this one

Honestly: reversibility, not conviction. Adding a field later is a one-line edit. Discovering at upload time that nine skills need rewriting is a bad afternoon. When one option is cheap to undo and the other isn't, the cheap one wins without needing to be right.

The `allowed-tools` field turned out to be in the spec, which removed most of the cost — that's what pre-approves the bundled scripts, and it was the field most worth having.

## What we're giving up

Real: forked context for `digest` and `repo-onboard`. Those two read the most and would benefit most from running in their own context, and today they don't.

## What would change my mind

- `digest` or `repo-onboard` visibly crowding the context window in normal use → add `context: fork` to those two specifically and accept they become Claude Code-only
- A concrete plan to upload these to claude.ai or use them in a Routine → decision confirmed, no change
- Six months with no attempt to use them outside Claude Code → the portability was worth nothing; take the Claude Code features

## Review on

2026-11-07

## Outcome

*(empty until reviewed)*
