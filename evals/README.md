# Evaluations

Three evaluations per skill, in the structure Anthropic documents for Agent Skills. They exist so a change to a skill can be judged rather than guessed at.

## Why these exist

Editing a skill feels productive and is nearly impossible to assess by reading. A longer skill isn't a better one — skill content stays in context for the rest of the session once loaded, so every added line is a recurring cost paid on every later turn. Without a baseline, "I improved the skill" means "I changed the skill".

Each evaluation targets a **specific way Claude gets the task wrong without the skill**, not a generic happy path. `ship-check`'s first case plants a secret because the failure being prevented is treating a committed credential as an ordinary finding. `digest`'s first case uses conflicting sources because the failure being prevented is averaging them into a false consensus.

## Format

```json
{
  "skills": ["ship-check"],
  "query": "I'm ready to push this branch, can you check it?",
  "files": ["a branch containing a hardcoded API key"],
  "expected_behavior": [
    "Leads the report with the exposed credential rather than burying it in a list",
    "States that removing it from the working tree is insufficient once committed"
  ]
}
```

`files` describes the fixture the case needs. Several are prose descriptions rather than paths — build the fixture to match when you run that case. `.claude/skills/ship-check/scan.sh` and `git-week.sh` both have shell fixtures that are quick to recreate; the rest are a scratch git repo and a few files.

## Running them

There is no built-in runner for skill evaluations, so this is deliberate manual work rather than a command:

1. **Baseline.** New session, skill disabled or renamed out of the way. Run the query. Record what happens against each `expected_behavior` line.
2. **With the skill.** Fresh session, skill enabled, same query. Record again.
3. **Compare.** A behavior that passes in both was never the skill's contribution — the skill isn't earning that line. A behavior that fails in both is a gap in the skill.
4. **Change one thing.** Re-run only the cases that failed.

Step 3 is the one worth the trouble. It regularly shows that a section of a skill is pure token cost, because the model already did that part unprompted.

## Keeping them honest

- **Write the evaluation before the fix.** If a skill misbehaves in real use, add a case that reproduces it *first*, then edit the skill. Otherwise you're describing the fix you already made.
- **Expected behaviors must be observable.** "Handles the task well" can't be scored. "Runs the suite and reports actual output" can.
- **Test across models if the skill will run on more than one.** Haiku generally needs more explicit guidance than Opus, and a skill tuned only against the strongest model tends to under-specify.

`skill-lint` enforces the count, not the quality:

```bash
.claude/skills/skill-lint/lint.py --evals evals .claude/skills
```
