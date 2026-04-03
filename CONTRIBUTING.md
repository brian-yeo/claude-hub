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

## Updating Baseline

Changes to `baseline/` files affect everyone. When you update baseline files:

- Note it clearly in the PR description
- After merge, team members need to re-upload the changed files to their Claude Projects

## Tips

- Keep skills focused on one task. If it does multiple things, split it.
- Agent knowledge files should be concise. Claude Projects have a ~200K token knowledge limit.
- Test your skill or agent before submitting. Does Claude actually produce better output with it?
