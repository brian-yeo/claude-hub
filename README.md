# Claude Hub

Shared Claude knowledge, skills, and agent blueprints for the leadership team.

## Quick Start

1. **Clone this repo**
2. **Set up your baseline** — create a Claude Project on claude.ai, upload all files from `baseline/` as project knowledge
3. **Add agents** — for each agent you want, create a new Claude Project:
   - Paste its `instructions.md` as the project's custom instructions
   - Upload files from its `knowledge/` folder + all `baseline/` files as project knowledge
4. **Use skills** — copy a skill's instructions into any Claude conversation when you need it
5. **Stay current** — `git pull` regularly to get new skills, agents, and knowledge updates

## Structure

```
baseline/       Company-wide context — upload to every Claude Project
skills/         Task-specific prompt templates — copy-paste into conversations
agents/         Full Claude Project blueprints — instructions + knowledge files

.claude/skills/ Claude Code skills — run automatically inside a Claude Code session
personal/       Working files those skills read and write (goals, reviews, decisions)
```

The top three are for **claude.ai Projects** — you copy or upload them by hand. The bottom two are for **Claude Code** — Claude picks them up on its own. See [Claude Code skills](#claude-code-skills) below.

## Baseline

These files give Claude context about who we are and how we operate. Upload all of them as knowledge files to every Claude Project you create.

| File | What it covers |
|------|---------------|
| `company-overview.md` | MSP identity, services, clients, org structure, vendors |
| `communication-style.md` | Tone and formatting for client-facing vs internal |
| `processes.md` | Ticketing, escalations, onboarding, change management |

## Skills

Single-file prompt templates. Open the file, copy the instructions, paste into Claude.

| Skill | Purpose |
|-------|---------|
| `ticket-triage.md` | Prioritize and categorize incoming tickets |
| `client-qbr-prep.md` | Prep quarterly business review content |
| `vendor-evaluation.md` | Evaluate an IT vendor or tool |
| `sow-drafting.md` | Draft a statement of work |
| `incident-postmortem.md` | Structure a post-incident review |

## Agents

Full Claude Project configs. Each folder contains `instructions.md` (custom instructions) and a `knowledge/` folder (files to upload).

| Agent | Purpose |
|-------|---------|
| `service-desk-advisor` | Escalation guidance, troubleshooting, documentation |
| `sales-engineer` | Scoping, proposals, solution design |
| `security-reviewer` | Policy review, risk assessment, compliance |
| `client-strategist` | Account planning, upsell identification, retention |

## Claude Code skills

Everything above is for claude.ai Projects — you copy a template into a conversation, or upload knowledge files by hand. The skills in `.claude/skills/` are different: they only apply in **Claude Code**, and Claude loads them itself when the work matches. You don't paste anything.

Two ways to use one:

- **Just work.** Say "get me up to speed on this repo" and `repo-onboard` loads on its own. Each skill's description lists the phrasings that trigger it.
- **Call it by name** — `/ship-check`, `/weekly-review` — when you want a specific one.

They're personal working tools rather than company templates, and they carry no MSP or company-specific assumptions, so they're useful in any repo you open this hub alongside.

| Skill | What it does |
|-------|-------------|
| `repo-onboard` | Map an unfamiliar codebase: how to run it, its entry points, one traced request path, where a change belongs |
| `ship-check` | Pre-push review — scope creep, debug leftovers, committed secrets, weak commit messages |
| `debug-loop` | Disciplined debugging once the obvious fix has failed: reproduce, hypothesis log, bisect |
| `notes-to-actions` | Raw meeting notes into decisions, owned actions, open questions, and a follow-up draft |
| `digest` | A pile of links or docs into one briefing — what's claimed, where sources disagree, what to do |
| `draft` | Write or tighten anything, in your voice as recorded in `personal/voice.md` |
| `weekly-review` | Friday review built from git history rather than memory, written to `personal/reviews/` |
| `decision-log` | Record a decision with its real reasoning and what would change your mind |
| `goals` | Keep goals observable, and force a decision on anything that's gone stale |
| `skill-lint` | Check any skill against Anthropic's published authoring rules |

Three ship with scripts that do the mechanical part before Claude reasons about the result. All are read-only:

```bash
.claude/skills/ship-check/scan.sh                   # scan the branch diff for problems
.claude/skills/weekly-review/git-week.sh -s ~/code  # what you committed this week, all repos
.claude/skills/skill-lint/lint.py --evals evals .claude/skills
```

Inside a skill they're referenced as `${CLAUDE_SKILL_DIR}/<script>`, which is what lets them run from any working directory — you can use `/ship-check` in a completely different repo and it still finds its scanner.

### Getting started

Open Claude Code in this repo and run `/goals`, then `/draft` to build your voice profile from a few writing samples. `/weekly-review` gets more useful each week, since it compares against the last one.

See [`personal/README.md`](personal/README.md) for where each skill stores its output — **including a note on privacy if this repo is shared with your team.**

### How these are built

The skills follow Anthropic's [skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), and `skill-lint` enforces the mechanical half of that guidance on every PR via [CI](.github/workflows/skills.yml). Three constraints shape how they're written:

- **Descriptions are the only trigger.** Only `name` and `description` load at startup; the body loads when the skill fires. A description that doesn't name concrete trigger phrases doesn't fire.
- **Bodies stay short because they persist.** Once loaded, a skill's content stays in context for the rest of the session, so every line is a recurring cost on every later turn — not a one-time one. All bodies are ~60–105 lines against a 500-line guideline.
- **Frontmatter stays inside the [Agent Skills spec](https://agentskills.io)'s six fields.** Claude Code accepts about twenty, but claude.ai uploads and the Skills API reject anything outside the spec with a hard error. Staying portable costs a couple of Claude Code-only features; the reasoning is written up in [`personal/decisions/`](personal/decisions/).

[`evals/`](evals/README.md) holds three evaluations per skill in Anthropic's documented format. They're the baseline for telling whether an edit to a skill actually helped — the case each one targets is a specific way Claude gets the task wrong *without* the skill.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add new skills and agents.
