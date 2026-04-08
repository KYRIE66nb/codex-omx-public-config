#!/usr/bin/env sh
set -eu

if [ -z "${ANTHROPIC_AUTH_TOKEN:-}" ] && [ -f "$HOME/.config/codex/env" ]; then
  # shellcheck disable=SC1090
  . "$HOME/.config/codex/env"
fi

if [ -z "${ANTHROPIC_AUTH_TOKEN:-}" ]; then
  printf '%s\n' 'ANTHROPIC_AUTH_TOKEN is not set' >&2
  exit 1
fi

printf '%s\n' "$ANTHROPIC_AUTH_TOKEN"

