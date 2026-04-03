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
```

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

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add new skills and agents.
