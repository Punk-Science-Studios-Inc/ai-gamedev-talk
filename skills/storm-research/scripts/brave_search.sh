#!/usr/bin/env bash
# Brave Search helper for the storm-research skill.
# Finds leads only — always WebFetch the actual page before citing it.
#
# Usage:  brave_search.sh "your query" [count]
# Key:    read from $BRAVE_API_KEY, else from ~/.claude/brave_key
set -euo pipefail

QUERY="${1:-}"
COUNT="${2:-8}"

if [[ -z "$QUERY" ]]; then
  echo "usage: brave_search.sh \"query\" [count]" >&2
  exit 2
fi

KEY="${BRAVE_API_KEY:-}"
if [[ -z "$KEY" && -f "$HOME/.claude/brave_key" ]]; then
  KEY="$(tr -d '[:space:]' < "$HOME/.claude/brave_key")"
fi
if [[ -z "$KEY" ]]; then
  echo "error: no Brave API key (set BRAVE_API_KEY or ~/.claude/brave_key)" >&2
  exit 3
fi

RESP="$(curl -s --max-time 25 -G "https://api.search.brave.com/res/v1/web/search" \
  --data-urlencode "q=$QUERY" \
  --data-urlencode "count=$COUNT" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: $KEY" \
  -w $'\n%{http_code}')"

CODE="$(tail -n1 <<<"$RESP")"
BODY="$(sed '$d' <<<"$RESP")"

if [[ "$CODE" != "200" ]]; then
  echo "error: Brave API HTTP $CODE" >&2
  echo "$BODY" | head -c 400 >&2
  exit 4
fi

echo "$BODY" | jq -r '.web.results[]? | "• \(.title)\n  \(.url)\n  \(.description // "" | gsub("<[^>]*>";""))\n"'
