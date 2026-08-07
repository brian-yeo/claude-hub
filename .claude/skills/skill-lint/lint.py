#!/usr/bin/env python3
"""lint.py — check Agent Skills against Anthropic's published authoring rules.

Implements the "Checklist for effective Skills" from the skill authoring best
practices, plus the frontmatter validation rules from the Agent Skills spec, as
mechanical checks. Rules that need judgement (is the description specific? are the
examples concrete?) are left to a human or an agent reading the skill.

Usage:
    python3 lint.py                      # lint ./.claude/skills
    python3 lint.py path/to/skills       # a directory of skill directories
    python3 lint.py path/to/one-skill    # a single skill directory
    python3 lint.py --strict ...         # warnings fail the run too
    python3 lint.py --portable ...       # also require Agent Skills spec portability

Exit status is 1 when any ERROR is found (or any WARN under --strict), so this
works as a CI gate.

No third-party dependencies: the frontmatter parser handles the flat key/value
subset that skill frontmatter uses, so PyYAML is not required.
"""

import argparse
import os
import re
import sys

# ---------------------------------------------------------------------------
# Rules from the Agent Skills spec and the authoring best practices.
# ---------------------------------------------------------------------------

# Spec limits: name <=64 chars, description <=1024 chars.
NAME_MAX = 64
DESC_MAX = 1024

# Claude Code truncates the combined description + when_to_use text at 1536
# characters in the skill listing. Warn before the cliff rather than at it, so
# there is room to add a trigger phrase without silently losing the tail.
LISTING_CAP = 1536
LISTING_WARN = 1200

# "Keep SKILL.md body under 500 lines for optimal performance."
BODY_MAX_LINES = 500

# "For reference files longer than 100 lines, include a table of contents."
TOC_THRESHOLD = 100

# The six fields the Agent Skills spec allows. Anything outside this set is
# Claude Code-only: fine on the filesystem, a hard error when packaged for
# claude.ai upload or the Skills API.
SPEC_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}

CLAUDE_CODE_FIELDS = {
    "when_to_use", "argument-hint", "arguments", "disable-model-invocation",
    "user-invocable", "disallowed-tools", "model", "effort", "context",
    "agent", "background", "hooks", "paths", "shell",
}

# Reserved words the spec forbids in a skill name.
RESERVED_NAME_WORDS = ("anthropic", "claude")

NAME_RE = re.compile(r"^[a-z0-9-]+$")
XML_TAG_RE = re.compile(r"<[A-Za-z/][^>]*>")
FRONTMATTER_RE = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n?", re.S)
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
BACKSLASH_PATH_RE = re.compile(r"(?<![`\\])\b[\w.-]+\\[\w.-]+\.(?:py|sh|md|js|ts|json|txt)\b")

# "Avoid time-sensitive information" — dated conditionals go stale silently.
TIME_SENSITIVE_RE = re.compile(
    r"\b(?:before|after|as of|until|starting)\s+"
    r"(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b",
    re.I,
)

# First/second person in a description causes discovery problems, because the
# description is injected into the system prompt. Third person only.
PERSON_RE = re.compile(r"\b(?:I can|I will|I help|I'll|you can use this|use me to)\b", re.I)

SCRIPT_EXTS = (".sh", ".py", ".js", ".mjs", ".rb", ".pl")


class Finding:
    __slots__ = ("level", "rule", "msg")

    def __init__(self, level, rule, msg):
        self.level = level
        self.rule = rule
        self.msg = msg


def parse_frontmatter(text):
    """Return (fields, body, error).

    Handles the flat mapping subset skill frontmatter uses: `key: value`, block
    scalars (`key: |`/`key: >`), and `- item` lists. Nested mappings under a key
    are collected as raw text, which is enough for the `metadata` free-form map.
    """
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None, text, "no YAML frontmatter (file must start with a --- line)"

    raw = m.group(1)
    body = text[m.end():]
    fields = {}
    key = None
    buf = []
    in_block = False

    for line in raw.split("\n"):
        if in_block:
            # Block scalar content is indented; a non-indented line ends it.
            if line.strip() == "" or line.startswith((" ", "\t")):
                buf.append(line.strip())
                continue
            fields[key] = " ".join(x for x in buf if x).strip()
            in_block, buf, key = False, [], None

        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith("- ") and key is not None:
            existing = fields.get(key, "")
            fields[key] = (existing + " " + stripped[2:].strip()).strip()
            continue

        km = re.match(r"^([A-Za-z_][\w.-]*)\s*:\s*(.*)$", line)
        if km and not line.startswith((" ", "\t")):
            key = km.group(1)
            val = km.group(2).strip()
            if val in ("|", ">", "|-", ">-", "|+", ">+"):
                in_block, buf = True, []
                fields[key] = ""
            else:
                if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
                    val = val[1:-1]
                fields[key] = val
        elif key is not None and line.startswith((" ", "\t")):
            # Continuation or nested mapping; append so length checks stay honest.
            fields[key] = (fields.get(key, "") + " " + stripped).strip()

    if in_block:
        fields[key] = " ".join(x for x in buf if x).strip()

    return fields, body, None


def lint_skill(skill_dir, portable=False, evals_dir=None):
    findings = []
    add = lambda lvl, rule, msg: findings.append(Finding(lvl, rule, msg))

    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        add("ERROR", "structure", "no SKILL.md in this directory")
        return findings

    with open(skill_md, encoding="utf-8") as fh:
        text = fh.read()

    fields, body, err = parse_frontmatter(text)
    if err:
        add("ERROR", "frontmatter", err)
        return findings

    dirname = os.path.basename(os.path.abspath(skill_dir))

    # ---- name -------------------------------------------------------------
    name = fields.get("name")
    if name is None:
        # Claude Code falls back to the directory name, so this is a warning.
        add("WARN", "name", "no name field; Claude Code will fall back to the directory name")
        name = dirname
    else:
        if len(name) > NAME_MAX:
            add("ERROR", "name", f"name is {len(name)} chars, spec maximum is {NAME_MAX}")
        if not NAME_RE.match(name):
            add("ERROR", "name", f"name '{name}' must be lowercase letters, numbers, and hyphens only")
        if XML_TAG_RE.search(name):
            add("ERROR", "name", "name cannot contain XML tags")
        for word in RESERVED_NAME_WORDS:
            if word in name.lower():
                add("ERROR", "name", f"name cannot contain the reserved word '{word}'")
        if name != dirname:
            # For personal and project skills the command comes from the directory,
            # so a mismatch means /name does not invoke what the file calls itself.
            add("WARN", "name",
                f"name '{name}' != directory '{dirname}'; the command is /{dirname}")

    # ---- description ------------------------------------------------------
    desc = fields.get("description", "")
    if not desc.strip():
        add("ERROR", "description", "description is empty; it is the only trigger signal")
    else:
        if len(desc) > DESC_MAX:
            add("ERROR", "description", f"description is {len(desc)} chars, spec maximum is {DESC_MAX}")
        if XML_TAG_RE.search(desc):
            add("ERROR", "description", "description cannot contain XML tags")

        combined = len(desc) + len(fields.get("when_to_use", ""))
        if combined > LISTING_CAP:
            add("ERROR", "description",
                f"description + when_to_use is {combined} chars; truncated at {LISTING_CAP} in the listing")
        elif combined > LISTING_WARN:
            add("WARN", "description",
                f"description + when_to_use is {combined} chars, close to the {LISTING_CAP} listing cap")

        pm = PERSON_RE.search(desc)
        if pm:
            add("ERROR", "description",
                f"description must be third person; found '{pm.group(0)}'")

        # Must say when to use it, not only what it does.
        if not re.search(r"\b(use (this )?(skill )?(when|for|before|after)|when the user|triggers? on)\b",
                         desc, re.I):
            add("WARN", "description",
                "description does not say when to use the skill; add 'Use when ...' triggers")

        if len(desc) < 60:
            add("WARN", "description",
                f"description is only {len(desc)} chars; likely too vague to trigger reliably")

    # ---- frontmatter fields ----------------------------------------------
    for key in fields:
        if key in SPEC_FIELDS:
            continue
        if key in CLAUDE_CODE_FIELDS:
            if portable:
                add("ERROR", "portability",
                    f"'{key}' is Claude Code-only; packaging for claude.ai or the Skills API fails on it")
            else:
                add("INFO", "portability",
                    f"'{key}' is Claude Code-only; not usable if this skill is uploaded to claude.ai")
        else:
            add("WARN", "frontmatter", f"unrecognized field '{key}'")

    # ---- body -------------------------------------------------------------
    body_lines = body.count("\n") + 1
    if body_lines > BODY_MAX_LINES:
        add("ERROR", "length",
            f"body is {body_lines} lines, over the {BODY_MAX_LINES}-line guidance; split into reference files")
    elif body_lines > BODY_MAX_LINES * 0.8:
        add("WARN", "length", f"body is {body_lines} lines, approaching the {BODY_MAX_LINES}-line guidance")

    for m in BACKSLASH_PATH_RE.finditer(body):
        add("ERROR", "paths", f"Windows-style path '{m.group(0)}'; use forward slashes")

    for m in TIME_SENSITIVE_RE.finditer(body):
        add("WARN", "time-sensitive",
            f"dated conditional '{m.group(0).strip()}' will go stale; use an 'old patterns' section")

    # ---- bundled files ----------------------------------------------------
    bundled = []
    for root, dirs, files in os.walk(skill_dir):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fn in files:
            rel = os.path.relpath(os.path.join(root, fn), skill_dir).replace(os.sep, "/")
            if rel != "SKILL.md":
                bundled.append(rel)

    for rel in bundled:
        full = os.path.join(skill_dir, rel)
        mentioned = rel in body or os.path.basename(rel) in body

        if not mentioned:
            add("INFO", "unused",
                f"'{rel}' is bundled but never mentioned in SKILL.md; Claude will not find it")
            continue

        if rel.endswith(SCRIPT_EXTS):
            # A bundled script referenced by a bare relative path only resolves
            # when the working directory happens to be the project root. Skills
            # run from wherever the user is, so anchor to ${CLAUDE_SKILL_DIR}.
            anchored = re.search(
                r"\$\{CLAUDE_SKILL_DIR\}/" + re.escape(rel),
                body,
            )
            if not anchored:
                add("ERROR", "skill-dir",
                    f"'{rel}' is referenced by a relative path; use ${{CLAUDE_SKILL_DIR}}/{rel} "
                    "so it resolves from any working directory")

            if not os.access(full, os.X_OK):
                add("WARN", "scripts", f"'{rel}' is not executable (chmod +x)")

            with open(full, encoding="utf-8", errors="replace") as fh:
                first = fh.readline()
            if not first.startswith("#!"):
                add("WARN", "scripts", f"'{rel}' has no shebang line")

        if rel.endswith(".md"):
            with open(full, encoding="utf-8", errors="replace") as fh:
                ref_text = fh.read()
            if ref_text.count("\n") + 1 > TOC_THRESHOLD and not re.search(
                r"^##\s*(contents|table of contents)", ref_text, re.I | re.M
            ):
                add("WARN", "toc",
                    f"'{rel}' is over {TOC_THRESHOLD} lines with no table of contents")
            # References must stay one level deep from SKILL.md.
            for link in MD_LINK_RE.findall(ref_text):
                if link.startswith(("http://", "https://", "#", "mailto:")):
                    continue
                if link.endswith(".md"):
                    add("ERROR", "nesting",
                        f"'{rel}' links to '{link}'; keep references one level deep from SKILL.md")

    # ---- evaluations ------------------------------------------------------
    # "At least three evaluations created" is on the official checklist. Without a
    # baseline you cannot tell whether editing a skill helped or hurt.
    if evals_dir:
        ev_path = os.path.join(evals_dir, f"{name}.json")
        if not os.path.isfile(ev_path):
            add("WARN", "evals", f"no evaluations at {ev_path}; the checklist asks for at least three")
        else:
            try:
                import json
                with open(ev_path, encoding="utf-8") as fh:
                    cases = json.load(fh)
                if not isinstance(cases, list):
                    add("ERROR", "evals", f"{ev_path} must contain a list of evaluation objects")
                else:
                    if len(cases) < 3:
                        add("WARN", "evals",
                            f"only {len(cases)} evaluation(s); the checklist asks for at least three")
                    for i, case in enumerate(cases):
                        if not isinstance(case, dict):
                            add("ERROR", "evals", f"evaluation {i} is not an object")
                            continue
                        missing = {"query", "expected_behavior"} - set(case)
                        if missing:
                            add("ERROR", "evals",
                                f"evaluation {i} is missing {', '.join(sorted(missing))}")
                        elif not case["expected_behavior"]:
                            add("ERROR", "evals", f"evaluation {i} has no expected_behavior")
            except (ValueError, OSError) as exc:
                add("ERROR", "evals", f"could not read {ev_path}: {exc}")

    # ---- dead links from SKILL.md ----------------------------------------
    for link in MD_LINK_RE.findall(body):
        if link.startswith(("http://", "https://", "#", "mailto:")):
            continue
        target = link.split("#", 1)[0]
        if not target:
            continue
        if os.path.isabs(target) or target.startswith("${"):
            continue
        # Links may point outside the skill (e.g. to repo docs); check both.
        if not (os.path.exists(os.path.join(skill_dir, target))
                or os.path.exists(os.path.join(os.getcwd(), target))):
            add("WARN", "links", f"link target '{link}' does not exist relative to the skill or cwd")

    return findings


def collect_skill_dirs(path):
    if os.path.isfile(os.path.join(path, "SKILL.md")):
        return [path]
    out = []
    try:
        for entry in sorted(os.listdir(path)):
            sub = os.path.join(path, entry)
            if os.path.isdir(sub) and os.path.isfile(os.path.join(sub, "SKILL.md")):
                out.append(sub)
    except NotADirectoryError:
        pass
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("paths", nargs="*", default=None,
                    help="skill directories, or directories containing them")
    ap.add_argument("--strict", action="store_true", help="treat warnings as failures")
    ap.add_argument("--portable", action="store_true",
                    help="require Agent Skills spec portability (no Claude Code-only fields)")
    ap.add_argument("--evals", metavar="DIR",
                    help="directory of <skill>.json evaluation files; checks each skill has at least three")
    ap.add_argument("--quiet", action="store_true", help="only show skills that have findings")
    args = ap.parse_args()

    paths = args.paths or [os.path.join(".claude", "skills")]

    skill_dirs = []
    for p in paths:
        if not os.path.exists(p):
            print(f"no such path: {p}", file=sys.stderr)
            return 2
        found = collect_skill_dirs(p)
        if not found:
            print(f"no skills found under: {p}", file=sys.stderr)
        skill_dirs.extend(found)

    if not skill_dirs:
        return 2

    totals = {"ERROR": 0, "WARN": 0, "INFO": 0}
    print(f"skill-lint: {len(skill_dirs)} skill(s)\n")

    for sd in skill_dirs:
        findings = lint_skill(sd, portable=args.portable, evals_dir=args.evals)
        for f in findings:
            totals[f.level] += 1
        name = os.path.basename(os.path.abspath(sd))
        if not findings:
            if not args.quiet:
                print(f"  {name}: ok")
            continue
        print(f"  {name}")
        for level in ("ERROR", "WARN", "INFO"):
            for f in findings:
                if f.level == level:
                    print(f"    {level:<5} [{f.rule}] {f.msg}")
        print()

    print(f"\n{totals['ERROR']} error(s), {totals['WARN']} warning(s), {totals['INFO']} note(s)")

    if totals["ERROR"]:
        return 1
    if args.strict and totals["WARN"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
