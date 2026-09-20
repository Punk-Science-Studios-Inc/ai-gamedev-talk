#!/usr/bin/env bash
# Copies agents/ and skills/ into each harness directory. Writes only its own entries. Deletes nothing else.
set -e
here="$(cd "$(dirname "$0")" && pwd)"
targets=("${@:-$HOME/.agents $HOME/.claude}")
for t in ${targets[@]}; do
  mkdir -p "$t/agents" "$t/skills"
  for f in "$here"/agents/*.md; do cp "$f" "$t/agents/"; done
  for d in "$here"/skills/*/; do n="$(basename "$d")"; rm -rf "$t/skills/$n"; cp -r "$d" "$t/skills/$n"; done
  echo "installed into $t"
done
