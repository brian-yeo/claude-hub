# Contributing

Anyone on the team can add new skills and agents via pull request.

## Adding a Skill

1. Create a new `.md` file in `skills/`
2. Use this format:

```markdown
# Skill: [Name]
**Purpose:** One-line description
**When to use:** When you'd reach for this

## Instructions

[The prompt/instructions to paste into Claude]

## Example Usage

[Optional — show sample input and expected output]
```

3. Open a PR with a short description
4. One approval required to merge

## Adding an Agent

1. Create a new folder in `agents/` with a descriptive name
2. Add `instructions.md` using this format:

```markdown
# Agent: [Name]
**Purpose:** What this agent does
**Best for:** Who should use it and when

## Custom Instructions

[Everything below here gets pasted into Claude Project custom instructions]

...
```

3. Add a `knowledge/` subfolder with any supporting files (docs, reference material, templates)
4. Open a PR with a short description
5. One approval required to merge

## Adding a Claude Code Skill

Skills in `.claude/skills/` are different from the copy-paste templates in `skills/` — Claude loads them automatically, so they follow the [Agent Skills](https://agentskills.io) format rather than the template format above.

1. Create `.claude/skills/<name>/SKILL.md` with `name` and `description` frontmatter
2. Write a description that says **what it does and when to use it**, with concrete trigger phrases — it's the only thing loaded at startup and the only reason the skill ever fires
3. Reference any bundled script as `${CLAUDE_SKILL_DIR}/<script>`, never a bare relative path, and add a matching `allowed-tools: Bash(${CLAUDE_SKILL_DIR}/<script> *)` rule
4. Add at least three evaluations to `evals/<name>.json` — see [`evals/README.md`](evals/README.md)
5. Run the linter until it's clean:

```bash
.claude/skills/skill-lint/lint.py --strict --evals evals .claude/skills
```

CI runs the same command on every PR. Or just ask Claude to `/skill-lint` your new skill, which also covers the judgement checks the script can't make.

## Updating Baseline

Changes to `baseline/` files affect everyone. When you update baseline files:

- Note it clearly in the PR description
- After merge, team members need to re-upload the changed files to their Claude Projects

## Tips

- Keep skills focused on one task. If it does multiple things, split it.
- Agent knowledge files should be concise. Claude Projects have a ~200K token knowledge limit.
- Test your skill or agent before submitting. Does Claude actually produce better output with it?
