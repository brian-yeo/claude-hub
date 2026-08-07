---
name: repo-onboard
description: Map an unfamiliar codebase — how to run it, its entry points, the path a real request takes through it, its conventions, and where a given change belongs. Use when starting work in a repo you don't know, returning to one you've forgotten, reading a dependency's source, or when the user says "how does this codebase work", "where do I change X", "give me a tour of this repo", "get me up to speed on this project", or drops you into a repo with no context.
---

# Repo Onboarding

Produce a map of a codebase that makes the next change obvious. The output is a written map, not a summary — the test is whether someone could use it to find the right file on their first try.

## The rule that matters

**Verify against code, not docs.** READMEs rot. Where the docs and the code disagree, the code wins and the disagreement goes in the map — that gap is usually the most valuable thing you'll find.

## Procedure

### 1. Orient cheaply before reading any source

Cost-order your reading. In this order:

- `README`, `CONTRIBUTING`, `docs/`
- Package manifests — `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `Gemfile`. Dependencies tell you the architecture faster than the source does: an ORM, a queue client, a web framework each imply a whole layer.
- CI config (`.github/workflows/`, `.gitlab-ci.yml`) — this is the **real** build and test procedure, the one that must pass. Trust it over the README.
- Directory tree, two levels deep, plus file counts per directory. Where the code is concentrated is where the work happens.
- `git log --oneline -30` and `git log --format='%an' | sort | uniq -c | sort -rn | head` — what's active, who to ask.

### 2. Establish ground truth: run it

Actually run the build, the app, and the test suite. Do not skip this and do not report it as working because it looks like it should.

Record the exact commands that worked, including any setup that wasn't in the README (env vars, services, versions). If something fails, record the failure verbatim — a broken build is a finding, not a blocker to hide.

### 3. Trace one real path end to end

Pick the single most representative operation — the main CLI command, the most-used endpoint, the core library call — and follow it all the way down: entry point → routing/dispatch → business logic → data access → response.

Name real files and functions at each hop. One traced path beats ten summarized modules; it teaches the layering, the naming, and the error handling all at once.

### 4. Map the data

- Schemas, models, migrations — what are the core entities and how do they relate?
- Where does state live? Database, cache, queue, files, external services?
- What crosses a network boundary? Those are the failure points and the slow parts.

### 5. Read the conventions off the code

Infer from what's actually there, not from a style guide:

- Naming, file layout, module boundaries
- Error handling — exceptions, result types, error codes? Consistent?
- Testing — what's the test style, what's actually covered, what's conspicuously untested?
- What's the escape hatch people use when the architecture gets in the way? (Every codebase has one, and finding it tells you where the design is under strain.)

### 6. Locate the change site

If the user has a goal, end by answering it concretely: *to do X, change these files, in this order, and here's the test that will tell you it worked.* If there's no stated goal, skip this.

## What not to do

- Don't read every file. Read the manifest, the entry point, one full path, and the tests for that path.
- Don't summarize directory names back as if that's architecture. "`src/services/` contains services" is worthless.
- Don't guess at what code does when you can run it or read it.
- Don't bury the surprising thing. If the auth is homegrown, or there are two competing HTTP clients, or a "temporary" module from three years ago is load-bearing — that goes near the top.

## Output

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
Anything the README gets wrong or omits goes here.

## Architecture
The layers, and what each is responsible for. A diagram only if it earns its place.

## Traced path: <the operation>
Entry `file:line` → … → `file:line`. Each hop with its file and what happens there.

## Data model
Core entities, where state lives, what crosses the network.

## Conventions
How this codebase does naming, errors, tests, config. Follow these when changing it.

## Landmarks
| I want to change… | Start in… |
|---|---|
The 5–10 lookups that cover most work.

## Surprises and sharp edges
Where docs and code disagree. What's load-bearing but looks disposable. What's untested.

## Open questions
What you couldn't determine, and who or what would answer it.
```

Offer to save the map to the repo (`docs/repo-map.md`) or to `personal/repo-maps/<repo>.md` in claude-hub. Don't save without asking — it's a file the repo's owners may have opinions about.
