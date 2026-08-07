#!/usr/bin/env bash
# scan.sh — mechanical pre-push scan of everything on this branch that isn't on the base.
#
# Covers committed, staged, and unstaged changes (i.e. the full "what I'm about to push,
# plus what I haven't committed yet" surface).
#
# Usage:
#   ./scan.sh [base-ref]
#
# base-ref defaults to the merge-base with the remote default branch (origin/HEAD),
# falling back to origin/main, origin/master, main, master.
#
# Always exits 0. Findings are advisory input for a human or an agent to triage —
# a "finding" is a thing to look at, not automatically a thing to fix.

set -uo pipefail

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "not a git repository" >&2
  exit 0
fi

# ---------- resolve base ----------
BASE="${1:-}"
if [[ -z "$BASE" ]]; then
  for cand in \
    "$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null || true)" \
    origin/main origin/master main master; do
    [[ -n "$cand" ]] || continue
    if git rev-parse --verify --quiet "$cand" >/dev/null 2>&1; then BASE="$cand"; break; fi
  done
fi

if [[ -z "$BASE" ]]; then
  echo "could not determine a base branch; pass one explicitly: ./scan.sh <base-ref>" >&2
  exit 0
fi

MERGE_BASE="$(git merge-base HEAD "$BASE" 2>/dev/null || true)"
if [[ -z "$MERGE_BASE" ]]; then
  echo "no merge-base between HEAD and $BASE" >&2
  exit 0
fi

HEAD_DESC="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo HEAD)"

echo "== ship-check scan =="
echo "branch:     $HEAD_DESC"
echo "base:       $BASE ($(git rev-parse --short "$MERGE_BASE"))"
echo

TAB=$'\t'

# Stream of added lines as  path:lineno<TAB>content  — real file locations, taken from
# the hunk headers, so every finding below points at somewhere you can actually go.
ADDED="$(
  git diff --unified=0 "$MERGE_BASE" -- 2>/dev/null | awk '
    /^\+\+\+ / { f = substr($0, 5); sub(/^b\//, "", f); next }
    /^@@/      { if (match($0, /\+[0-9]+/)) n = substr($0, RSTART+1, RLENGTH-1) + 0; next }
    /^\+/      { if (f != "" && f != "/dev/null") printf "%s:%d\t%s\n", f, n, substr($0, 2); n++; next }
    /^-/       { next }
    /^ /       { n++ }
  '
)"

FILES="$(git diff --name-only "$MERGE_BASE" -- 2>/dev/null || true)"

FINDINGS=0
note() { FINDINGS=$((FINDINGS + 1)); }
section() { echo "-- $1"; }

report() { # <label> <newline-separated hits>
  local label="$1" hits="$2"
  [[ -n "$hits" ]] || return 0
  note
  echo "[$label]"
  printf '%s\n' "$hits" | head -25 | sed $'s/\t/  |  /' | sed 's/^/    /'
  local n; n="$(printf '%s\n' "$hits" | wc -l | tr -d ' ')"
  (( n > 25 )) && echo "    … and $(( n - 25 )) more"
  echo
}

scan_added() { # <label> <extended-regex>
  report "$1" "$(printf '%s\n' "$ADDED" | grep -Ei -e "$2" || true)"
}

scan_files() { # <label> <extended-regex against paths>
  report "$1" "$(printf '%s\n' "$FILES" | grep -Ei -e "$2" || true)"
}

# ---------- 1. scope ----------
section "scope"
if [[ -z "$FILES" ]]; then
  echo "    no changes vs $BASE"
  echo
else
  git diff --shortstat "$MERGE_BASE" -- | sed 's/^ */    /'
  echo "    areas touched:"
  printf '%s\n' "$FILES" | awk -F/ '{print (NF>1 ? $1"/" : "(root)")}' | sort | uniq -c | sort -rn | sed 's/^/      /'
  echo
fi

# ---------- 2. secrets ----------
section "secrets"
scan_added "private key block"          '-----BEGIN [A-Z ]*PRIVATE KEY-----'
scan_added "aws access key id"          'AKIA[0-9A-Z]{16}'
scan_added "github token"               'gh[pousr]_[A-Za-z0-9]{30,}'
scan_added "slack token"                'xox[baprs]-[A-Za-z0-9-]{10,}'
scan_added "stripe live key"            'sk_live_[A-Za-z0-9]{16,}'
scan_added "google api key"             'AIza[0-9A-Za-z_-]{35}'
scan_added "anthropic/openai style key" '(sk-ant-|sk-proj-)[A-Za-z0-9_-]{16,}'
scan_added "json web token"             'eyJ[A-Za-z0-9_-]{8,}\.eyJ[A-Za-z0-9_-]{8,}'
scan_added "credentials in a url"       '://[A-Za-z0-9._%-]+:[^@/[:space:]]{6,}@'
scan_added "hardcoded credential"       '(api[_-]?key|secret|passwd|password|token|access[_-]?key|client[_-]?secret)[[:space:]]*[:=][[:space:]]*["'"'"'][^"'"'"'[:space:]]{8,}["'"'"']'
scan_files "credential-ish file in diff" '(^|/)\.env($|\.)|\.pem$|\.p12$|\.pfx$|(^|/)id_(rsa|dsa|ecdsa|ed25519)$|\.keystore$|\.jks$|(^|/)credentials(\.json)?$|\.kdbx$'

# ---------- 3. leftovers ----------
section "leftovers"
scan_added "merge conflict marker"    "${TAB}(<<<<<<<|>>>>>>>)[[:space:]]"
scan_added "debugger statement"       '\b(debugger;|binding\.pry|byebug|pdb\.set_trace\(|breakpoint\(\)|debug\.set_trace)'
scan_added "console/print debugging"  '\b(console\.(log|debug|dir|trace)|System\.out\.println|var_dump|dd|dump|fmt\.Print(f|ln)?|dbg!)[[:space:]]*\('
scan_added "commented-out code"       "${TAB}[[:space:]]*(//|#)[[:space:]]*(if|for|while|return|import|def |function |const |let |var |class )"
scan_added "skipped or focused test"  '(\.only\(|\.skip\(|xit\(|xdescribe\(|fdescribe\(|fit\(|@pytest\.mark\.skip|@unittest\.skip|t\.Skip\(|#\[ignore\])'
scan_added "new todo/fixme"           '\b(TODO|FIXME|XXX|HACK)\b'

# ---------- 4. size ----------
section "size"
BIG=""
while IFS= read -r -d '' f; do
  [[ -f "$f" ]] || continue
  sz=$(wc -c <"$f" 2>/dev/null || echo 0)
  if (( sz > 512000 )); then
    BIG+="$(( sz / 1024 ))K${TAB}$f"$'\n'
  fi
done < <(git diff --name-only -z "$MERGE_BASE" -- 2>/dev/null)
report "large file (>500K)" "$(printf '%s' "$BIG")"
scan_files "build output or vendored code in diff" '\.min\.(js|css)$|(^|/)(dist|build|out|vendor|node_modules)/'

# ---------- 5. commits ----------
section "commits"
COMMITS="$(git log --no-merges --pretty=format:'%h %s' "$MERGE_BASE"..HEAD 2>/dev/null || true)"
if [[ -z "$COMMITS" ]]; then
  echo "    (no commits yet on this branch — everything is uncommitted)"
  echo
else
  printf '%s\n' "$COMMITS" | sed 's/^/    /'
  echo
  WEAK="$(printf '%s\n' "$COMMITS" | awk '
    {
      msg = substr($0, index($0, " ") + 1)
      low = tolower(msg)
      if (length(msg) < 12 || low ~ /^(wip|fix|fixes|fixed|update|updates|updated|change|changes|stuff|temp|tmp|test|asdf|cleanup|minor|misc|oops|typo|more|again|\.+)$/) print
    }')"
  report "low-information commit message" "$WEAK"
fi

# ---------- 6. working tree ----------
section "working tree"
DIRTY="$(git status --porcelain 2>/dev/null || true)"
if [[ -n "$DIRTY" ]]; then
  report "uncommitted changes present" "$DIRTY"
else
  echo "    clean"
  echo
fi

echo "== $FINDINGS finding group(s); triage before pushing =="
