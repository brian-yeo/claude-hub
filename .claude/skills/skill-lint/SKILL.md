---
name: skill-lint
description: Checks Agent Skills against Anthropic's published authoring rules — frontmatter validity, description quality, body length, reference nesting, script portability, and spec compliance. Use when writing or editing a SKILL.md, before committing a skill, when a skill fails to trigger, when reviewing a skill from an untrusted source, or when the user says "lint my skills", "check this skill", "why isn't my skill firing", or "is this skill spec compliant".
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/lint.py *)
---

# Skill Lint

Mechanical checks first, judgement second. The script covers every rule that can be checked automatically; the rules that need reading are listed below and are your job.

## Run it

```bash
${CLAUDE_SKILL_DIR}/lint.py .claude/skills           # a directory of skills
${CLAUDE_SKILL_DIR}/lint.py .claude/skills/my-skill  # one skill
${CLAUDE_SKILL_DIR}/lint.py --portable .claude/skills
${CLAUDE_SKILL_DIR}/lint.py --evals evals .claude/skills
```

`--portable` promotes Claude Code-only frontmatter to an error. Use it for any skill that might be uploaded to claude.ai, used through the Skills API, or enabled for Cowork and cloud sessions — those paths accept only six fields (`name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`) and fail hard on anything else.

`--evals DIR` checks each skill has at least three evaluations in `DIR/<name>.json`, and that each one has a query and expected behaviors. It checks the count, not the quality.

`--strict` makes warnings fail, for CI. Exit status is 1 on any error.

## Fix loop

Run → fix → run again. Do not stop at the first clean-looking pass; fixing a frontmatter error often reveals a body error that was masked while parsing failed.

```
- [ ] Run the linter
- [ ] Fix every ERROR
- [ ] Triage each WARN: fix, or note why it stands
- [ ] Re-run until clean
- [ ] Do the judgement checks below
```

## What the errors mean

**`skill-dir`** — a bundled script is referenced by a bare relative path. That only resolves when the working directory happens to be the project root, so the skill breaks the moment it runs anywhere else. The fix is in the linter's own error message: it prints the exact skill-directory variable and the corrected path to use. Put that form in the body, and add an `allowed-tools` Bash rule using the same form so the script runs without a permission prompt.

> The error message is the reference here rather than this paragraph, because the variable is substituted wherever it appears in a skill body — including inside prose and code fences. Writing it literally here would render as *this* skill's directory and tell you to hardcode the wrong path.

**`nesting`** — a reference file links to another reference file. Claude often previews nested files with a partial read instead of reading them whole, so the information at the bottom is silently missed. Keep every reference one level deep from SKILL.md.

**`description`** — the description is the only thing loaded at startup and the only signal for whether the skill triggers at all. It must be third person, and it must say *when* to use the skill, not just what it does.

**`length`** — bodies over 500 lines should split into reference files. Skill content stays in context for the rest of the session once loaded, so body length is a recurring cost on every later turn, not a one-time one.

**`portability`** — a Claude Code-only field is present. Harmless on the filesystem, fatal when packaged.

## Judgement checks the script cannot make

After the linter is clean, read the skill and answer these:

- **Is the description specific enough to fire?** Would it beat a competing skill for an ambiguous request? Descriptions under-trigger far more often than they over-trigger, so lean toward more trigger phrases.
- **Does it assume Claude is competent?** Delete anything explaining what Claude already knows. Every retained line costs tokens on every subsequent turn.
- **Is the freedom level right?** Fragile, must-be-exact operations want a specific script. Context-dependent judgement wants prose. Mismatches show up as Claude either improvising where it shouldn't or asking permission where it should just act.
- **Are the examples concrete?** Abstract examples teach nothing.
- **Is terminology consistent?** One term per concept, throughout.
- **Are there too many options?** Give one default with an escape hatch, not a menu.
- **Would this survive a fresh session?** Claude Code never re-reads the file, so anything that must hold for the whole task has to read as a standing rule, not a step that scrolls past.

## Reviewing an untrusted skill

A skill directs Claude to run code and use tools. Before trusting one from outside:

- Read every bundled file, not just SKILL.md — scripts are executed without their contents entering context, so an unread script is genuinely unread.
- Look for network calls, credential reads, or file access that the stated purpose doesn't justify.
- Check `allowed-tools` for grants wider than the skill needs. A project skill can pre-approve tools for itself once you trust the workspace.
