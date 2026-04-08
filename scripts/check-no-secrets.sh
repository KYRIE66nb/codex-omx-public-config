#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

matches="$(
  {
    rg -n --hidden --glob '!**/.git/**' '(gho_[A-Za-z0-9_]+|APIsk-[A-Za-z0-9_]+|sk-[A-Za-z0-9]{20,})' . \
      | rg -v '__[A-Z0-9_]+__|replace_me|your-key'
  } || true
)"

if [[ -n "$matches" ]]; then
  printf '%s\n' "$matches"
  printf 'Secret-like strings detected.\n' >&2
  exit 1
fi

printf 'No secret-like strings detected.\n'
