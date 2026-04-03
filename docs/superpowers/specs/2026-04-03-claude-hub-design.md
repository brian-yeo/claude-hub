# Claude Hub — Design Spec

## Overview

A shared GitHub repo for the leadership team (5-7 people, mixed Claude experience) to collaborate on company knowledge, reusable skills, and agent blueprints. Primary platform is claude.ai web (Claude Projects), with Claude Code users also supported.

## Problem

The leadership team all use Claude with an enterprise subscription but lack a central place to share knowledge, prompt templates, and project configurations. Everyone builds their own context from scratch.

## Repo Structure

```
claude-hub/
├── README.md
├── CONTRIBUTING.md
├── baseline/
│   ├── company-overview.md
│   ├── communication-style.md
│   └── processes.md
├── skills/
│   ├── ticket-triage.md
│   ├── client-qbr-prep.md
│   ├── vendor-evaluation.md
│   ├── sow-drafting.md
│   └── incident-postmortem.md
└── agents/
    ├── service-desk-advisor/
    │   ├── instructions.md
    │   └── knowledge/
    ├── sales-engineer/
    │   ├── instructions.md
    │   └── knowledge/
    ├── security-reviewer/
    │   ├── instructions.md
    │   └── knowledge/
    └── client-strategist/
        ├── instructions.md
        └── knowledge/
```

## Components

### Baseline (`baseline/`)

Company-wide context uploaded as knowledge files to every Claude Project. This is the shared foundation — Claude always knows who you are, what you do, and how you operate.

Files:
- **company-overview.md** — MSP identity, service stack, client profile, org structure, key vendors/partners
- **communication-style.md** — tone and formatting for client-facing vs internal communication
- **processes.md** — ticketing workflow, escalation paths, client onboarding, change management

### Skills (`skills/`)

Single-file prompt templates for recurring tasks. Copy-paste into any Claude conversation.

Each skill follows a standard format:

```markdown
# Skill: [Name]
**Purpose:** One-line description
**When to use:** Trigger conditions

## Instructions
[The prompt/instructions to paste into Claude]

## Example Usage
[Optional — show what input looks like and what output to expect]
```

Starter skills:
- **ticket-triage.md** — prioritize and categorize incoming tickets by urgency, impact, and SLA
- **client-qbr-prep.md** — generate quarterly business review content from ticket data and notes
- **vendor-evaluation.md** — structured evaluation of an IT vendor, tool, or platform
- **sow-drafting.md** — draft a statement of work from scope notes
- **incident-postmortem.md** — structure a post-incident review with timeline, root cause, and action items

### Agents (`agents/`)

Full Claude Project blueprints. Each agent is a folder with custom instructions and knowledge files. To use one: create a Claude Project, paste `instructions.md` as custom instructions, upload files from `knowledge/` plus the baseline files.

Each agent's `instructions.md` follows a standard format:

```markdown
# Agent: [Name]
**Purpose:** What this agent does
**Best for:** Who should use it and when

## Custom Instructions
[Paste everything below this line into Claude Project custom instructions]

...
```

Starter agents:
- **service-desk-advisor/** — escalation guidance, troubleshooting frameworks, documentation help
- **sales-engineer/** — scoping, proposal writing, solution design for prospects
- **security-reviewer/** — policy review, risk assessment, compliance checks, security questionnaire help
- **client-strategist/** — account planning, upsell identification, retention strategy, relationship management

## Workflow

### Using the repo

1. Clone `claude-hub` from the GitHub org
2. **Baseline setup** — create a Claude Project, upload all `baseline/` files as project knowledge
3. **Add agents** — for each agent, create a Claude Project: paste its `instructions.md` as custom instructions, upload its `knowledge/` files + baseline files
4. **Use skills** — copy a skill's instructions into any Claude conversation when needed
5. **Pull updates** — `git pull` to get new skills, agents, and knowledge updates from the team

### Contributing

Open contribution via PRs. Anyone on the team can submit new skills or agents.

Process:
1. Create a branch
2. Add your skill (single `.md` file in `skills/`) or agent (folder in `agents/` with `instructions.md` + `knowledge/`)
3. Follow the standard format templates
4. Open a PR with a short description of what it does and when to use it
5. One approval required to merge

### Versioning

Keep it simple — no semantic versioning. The `main` branch is always the current state. When baseline files change, a note in the PR description flags it so team members know to re-upload to their Claude Projects.

## What's Out of Scope

- Automated sync between the repo and Claude Projects (no API for this today)
- Claude Code-specific configuration (skills, MCP, hooks) — can be added later as adoption grows
- Per-user customization within the repo — leaders customize in their own Claude Projects, not in the shared repo

## Success Criteria

- Every leader has a working baseline Claude Project within the first week
- At least 3 skills and 2 agents are usable on day one
- A new team member can go from clone to working Claude Projects by following the README alone
- Team contributes at least 1 new skill or agent within the first month
