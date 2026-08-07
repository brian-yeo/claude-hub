---
name: repo-onboard
description: Maps an unfamiliar codebase — how to run it, its entry points, the path a real request takes through it, its conventions, and where a given change belongs. Use when starting work in a repo you don't know, returning to one you've forgotten, reading a dependency's source, or when the user says "how does this codebase work", "where do I change X", "give me a tour of this repo", "get me up to speed on this project", or drops you into a repo with no context.
---

# Repo Onboarding

Produce a map that makes the next change obvious. The test is whether someone could use it to find the right file on their first try.

## Standing rules

- **Verify against code, not docs.** READMEs rot. Where docs and code disagree, the code wins and the disagreement goes in the map — that gap is usually the most valuable finding.
- **Don't read every file.** Read the manifest, the entry point, one full path, and the tests for that path.
- **Never report something as working because it looks like it should.** Run it.
- **Don't bury the surprising thing.** Homegrown auth, two competing HTTP clients, a "temporary" module that's load-bearing — that goes near the top.

## Checklist

```
- [ ] 1. Orient cheaply (docs, manifests, CI, tree, git log)
- [ ] 2. Run it — build, app, tests
- [ ] 3. Trace one real path end to end
- [ ] 4. Map the data
- [ ] 5. Read conventions off the code
- [ ] 6. Locate the change site (if there's a goal)
- [ ] 7. Write the map
```

## 1. Orient

In cost order, before reading any source:

- `README`, `CONTRIBUTING`, `docs/`
- Package manifests — `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `Gemfile`. Dependencies reveal architecture faster than source does: an ORM, a queue client, a web framework each imply a whole layer.
- CI config (`.github/workflows/`, `.gitlab-ci.yml`) — the **real** build and test procedure, the one that must pass. Trust it over the README.
- Directory tree two levels deep, plus file counts per directory. Concentration shows where the work happens.
- `git log --oneline -30`, and `git log --format='%an' | sort | uniq -c | sort -rn | head` — what's active, who to ask.

## 2. Run it

Build, run, and test. Record the exact commands that worked, including setup the README omits (env vars, services, versions). A failure is a finding — record it verbatim rather than hiding it.

## 3. Trace one real path

Pick the most representative operation — the main CLI command, the most-used endpoint, the core library call — and follow it down: entry point → routing → business logic → data access → response. Name real files and functions at each hop.

One traced path beats ten summarized modules; it teaches layering, naming, and error handling at once.

## 4. Data

Core entities and relationships. Where state lives (database, cache, queue, files, external services). What crosses a network boundary — those are the failure points and the slow parts.

## 5. Conventions

Infer from the code, not a style guide: naming, module boundaries, error handling (exceptions, result types, error codes — consistent?), test style and what's conspicuously untested.

Find the escape hatch people use when the architecture gets in the way. Every codebase has one, and it marks where the design is under strain.

## 6. Change site

If the user has a goal, answer it concretely: to do X, change these files, in this order, and here's the test that will tell you it worked. Skip if there's no stated goal.

## 7. Output

```markdown
# <repo> — Map
*Mapped <date> at commit <sha>*

## In one paragraph
What this is, who uses it, what it talks to.

## Run it
| Task | Command | Notes |
|------|---------|-------|
| Install | | |
| Run | | |
| Test | | |
| Lint | | |
What the README gets wrong or omits goes here.

## Architecture
The layers and what each owns. A diagram only if it earns its place.

## Traced path: <the operation>
Entry `file:line` → … → `file:line`, each hop with what happens there.

## Data model
Core entities, where state lives, what crosses the network.

## Conventions
Naming, errors, tests, config. Follow these when changing it.

## Landmarks
| I want to change… | Start in… |
|---|---|
The 5–10 lookups that cover most work.

## Surprises and sharp edges
Docs/code disagreements. Load-bearing things that look disposable. What's untested.

## Open questions
What you couldn't determine, and what would answer it.
```

Offer to save to `docs/repo-map.md` in the mapped repo, or `personal/repo-maps/<repo>.md` in claude-hub. Ask first — it's a file the repo's owners may have opinions about.
