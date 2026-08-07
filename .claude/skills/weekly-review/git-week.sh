#!/usr/bin/env bash
# git-week.sh — what you actually committed over the last N days, across one or more repos.
#
# Usage:
#   ./git-week.sh [-d DAYS] [-a AUTHOR] [-s SCAN_DIR] [repo ...]
#
#   -d DAYS      how far back to look (default: 7)
#   -a AUTHOR    author filter, matched against name and email (default: your git user.email)
#                pass -a '' to include every author
#   -s SCAN_DIR  treat each immediate subdirectory of SCAN_DIR that is a git repo as a repo
#   repo ...     explicit repo paths (default: the current repo)
#
# Reads only. Never writes, never changes checked-out state.

set -uo pipefail

# One week, matching the review cadence this feeds. Override with -d.
DAYS=7

# Branches listed per repo, most-recently-committed first. Five is enough to show
# what's in flight without printing every stale branch in a long-lived repo.
BRANCHES_SHOWN=5

AUTHOR="__unset__"
SCAN_DIR=""
REPOS=()

while getopts ":d:a:s:h" opt; do
  case "$opt" in
    d) DAYS="$OPTARG" ;;
    a) AUTHOR="$OPTARG" ;;
    s) SCAN_DIR="$OPTARG" ;;
    h) sed -n '2,14p' "$0"; exit 0 ;;
    \?) echo "unknown option -$OPTARG" >&2; exit 1 ;;
    :) echo "option -$OPTARG needs a value" >&2; exit 1 ;;
  esac
done
shift $((OPTIND - 1))

if ! [[ "$DAYS" =~ ^[0-9]+$ ]]; then
  echo "-d needs a whole number of days, got: $DAYS" >&2
  exit 1
fi

if [[ "$AUTHOR" == "__unset__" ]]; then
  AUTHOR="$(git config user.email 2>/dev/null || true)"
fi

for r in "$@"; do REPOS+=("$r"); done

if [[ -n "$SCAN_DIR" ]]; then
  if [[ ! -d "$SCAN_DIR" ]]; then
    echo "no such directory: $SCAN_DIR" >&2
    exit 1
  fi
  while IFS= read -r d; do
    [[ -n "$d" ]] && REPOS+=("$d")
  done < <(find "$SCAN_DIR" -mindepth 1 -maxdepth 1 -type d -exec test -e '{}/.git' ';' -print 2>/dev/null | sort)
fi

if [[ ${#REPOS[@]} -eq 0 ]]; then
  if git rev-parse --git-dir >/dev/null 2>&1; then
    REPOS=(".")
  else
    echo "not a git repository, and no repos given; use -s DIR or pass repo paths" >&2
    exit 1
  fi
fi

echo "== git activity: last $DAYS days =="
echo "author filter: ${AUTHOR:-<all authors>}"
echo "repos:         ${#REPOS[@]}"
echo

G_COMMITS=0; G_ADD=0; G_DEL=0; G_FILES=0; G_ACTIVE=0

for repo in "${REPOS[@]}"; do
  if ! git -C "$repo" rev-parse --git-dir >/dev/null 2>&1; then
    echo "-- $repo  (not a git repo, skipped)"
    echo
    continue
  fi

  name="$(basename "$(cd "$repo" && pwd)")"

  if [[ -n "$AUTHOR" ]]; then
    LOG="$(git -C "$repo" log --all --no-merges --since="$DAYS days ago" \
             --author="$AUTHOR" --date=short --numstat \
             --pretty=format:'C|%h|%ad|%s' 2>/dev/null || true)"
  else
    LOG="$(git -C "$repo" log --all --no-merges --since="$DAYS days ago" \
             --date=short --numstat \
             --pretty=format:'C|%h|%ad|%s' 2>/dev/null || true)"
  fi

  if [[ -z "$LOG" ]]; then
    echo "-- $name  (nothing in the last $DAYS days)"
    echo
    continue
  fi

  G_ACTIVE=$((G_ACTIVE + 1))
  echo "-- $name"

  SUMMARY="$(printf '%s\n' "$LOG" | awk -F'\t' '
    /^C\|/ {
      n = split($0, p, "|")
      hash = p[2]; date = p[3]
      msg = ""
      for (i = 4; i <= n; i++) msg = msg (i > 4 ? "|" : "") p[i]
      cur = hash
      count++
      order[count] = hash
      h_date[hash] = date
      h_msg[hash] = msg
      next
    }
    NF == 3 {
      if ($1 != "-") { add[cur] += $1; t_add += $1 }
      if ($2 != "-") { del[cur] += $2; t_del += $2 }
      files[cur]++
      touched[$3] = 1
      next
    }
    END {
      prev = ""
      for (i = 1; i <= count; i++) {
        h = order[i]
        if (h_date[h] != prev) { printf "\n   %s\n", h_date[h]; prev = h_date[h] }
        printf "     %s  %s\n", h, h_msg[h]
        printf "              %d file(s), +%d/-%d\n", files[h] + 0, add[h] + 0, del[h] + 0
      }
      nf = 0
      for (f in touched) nf++
      printf "\nSTATS %d %d %d %d\n", count, t_add + 0, t_del + 0, nf
    }
  ')"

  printf '%s\n' "$SUMMARY" | grep -v '^STATS ' | sed '/^$/N;/^\n$/D'

  STATS="$(printf '%s\n' "$SUMMARY" | grep '^STATS ' | tail -1)"
  # shellcheck disable=SC2086
  set -- $STATS
  C=${2:-0}; A=${3:-0}; D=${4:-0}; F=${5:-0}
  echo "   ---- $C commit(s), $F distinct file(s), +$A/-$D"

  BR="$(git -C "$repo" for-each-ref --sort=-committerdate refs/heads \
        --format='%(refname:short) (%(committerdate:relative))' 2>/dev/null | head -"$BRANCHES_SHOWN" || true)"
  if [[ -n "$BR" ]]; then
    echo "   branches, most recent first:"
    printf '%s\n' "$BR" | sed 's/^/     /'
  fi
  echo

  G_COMMITS=$((G_COMMITS + C)); G_ADD=$((G_ADD + A)); G_DEL=$((G_DEL + D)); G_FILES=$((G_FILES + F))
done

echo "== totals: $G_COMMITS commit(s) across $G_ACTIVE active repo(s), $G_FILES file(s), +$G_ADD/-$G_DEL =="
if [[ $G_COMMITS -eq 0 && -n "$AUTHOR" ]]; then
  echo "   (nothing matched '$AUTHOR' — if you commit under another identity, rerun with -a '' or -a <email>)"
fi
