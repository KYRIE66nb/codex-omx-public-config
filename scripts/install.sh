#!/usr/bin/env bash
set -euo pipefail

dry_run=0
if [[ "${1:-}" == "--dry-run" ]]; then
  dry_run=1
fi

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
target_home="${TARGET_HOME:-$HOME}"

openai_base_url="${OPENAI_BASE_URL_VALUE:-https://tokenx24.com/v1}"
claude_base_url="${CLAUDE_OPENAI_BASE_URL_VALUE:-https://claw.xclawxx.top/v1}"
openai_api_key="${OPENAI_API_KEY_VALUE:-${OPENAI_API_KEY:-replace_me}}"
claude_openai_api_key="${CLAUDE_OPENAI_API_KEY_VALUE:-${CLAUDE_OPENAI_API_KEY:-$openai_api_key}}"
openclaw_gateway_url="${OPENCLAW_GATEWAY_URL:-http://127.0.0.1:18789/hooks/wake}"
openclaw_gateway_token="${OPENCLAW_GATEWAY_TOKEN:-}"

notify_hook="${OMX_NOTIFY_HOOK:-}"
if [[ -z "$notify_hook" ]] && command -v npm >/dev/null 2>&1; then
  npm_global_root="$(npm root -g 2>/dev/null || true)"
  if [[ -n "$npm_global_root" ]]; then
    notify_hook="${npm_global_root}/oh-my-codex/dist/scripts/notify-hook.js"
  fi
fi
if [[ -z "$notify_hook" ]]; then
  notify_hook="${target_home}/.volta/tools/image/packages/oh-my-codex/lib/node_modules/oh-my-codex/dist/scripts/notify-hook.js"
fi

codex_native_hook="${OMX_CODEX_NATIVE_HOOK:-}"
if [[ -z "$codex_native_hook" ]] && [[ -n "$notify_hook" ]]; then
  codex_native_hook="$(dirname "$notify_hook")/codex-native-hook.js"
fi

run() {
  if [[ "$dry_run" -eq 1 ]]; then
    printf '[dry-run] %s\n' "$*"
  else
    eval "$@"
  fi
}

sync_tree() {
  local src="$1"
  local dest="$2"
  run "mkdir -p \"$dest\""
  run "rsync -a \"$src\" \"$dest\""
}

render_text() {
  local src="$1"
  local dest="$2"
  if [[ "$dry_run" -eq 1 ]]; then
    printf '[dry-run] render %s -> %s\n' "$src" "$dest"
    return
  fi

  mkdir -p "$(dirname "$dest")"
  python3 - "$src" "$dest" "$target_home" "$notify_hook" "$openai_base_url" "$claude_base_url" "$codex_native_hook" "$openai_api_key" "$claude_openai_api_key" <<'PY'
import pathlib
import sys

src = pathlib.Path(sys.argv[1])
dest = pathlib.Path(sys.argv[2])
home = sys.argv[3]
notify_hook = sys.argv[4]
openai_base_url = sys.argv[5]
claude_base_url = sys.argv[6]
codex_native_hook = sys.argv[7]
openai_api_key = sys.argv[8]
claude_openai_api_key = sys.argv[9]

text = src.read_text()
text = text.replace("__HOME__", home)
text = text.replace("__OMX_NOTIFY_HOOK__", notify_hook)
text = text.replace("__OMX_CODEX_NATIVE_HOOK__", codex_native_hook)
text = text.replace("__OPENAI_BASE_URL__", openai_base_url)
text = text.replace("__CLAUDE_OPENAI_BASE_URL__", claude_base_url)
text = text.replace("__OPENAI_API_KEY__", openai_api_key)
text = text.replace("__CLAUDE_OPENAI_API_KEY__", claude_openai_api_key)
dest.write_text(text)
PY
}

render_omx_json() {
  local src="$1"
  local dest="$2"
  if [[ "$dry_run" -eq 1 ]]; then
    printf '[dry-run] render %s -> %s\n' "$src" "$dest"
    return
  fi

  mkdir -p "$(dirname "$dest")"
  python3 - "$src" "$dest" "$openclaw_gateway_url" "$openclaw_gateway_token" <<'PY'
import json
import pathlib
import sys

src = pathlib.Path(sys.argv[1])
dest = pathlib.Path(sys.argv[2])
gateway_url = sys.argv[3]
gateway_token = sys.argv[4]

raw = src.read_text()
raw = raw.replace("__OPENCLAW_GATEWAY_URL__", gateway_url)
raw = raw.replace("__OPENCLAW_GATEWAY_TOKEN__", gateway_token or "REPLACE_ME_OPENCLAW_TOKEN")
data = json.loads(raw)

enabled = bool(gateway_token)
data["notifications"]["openclaw"]["enabled"] = enabled
for hook in data["notifications"]["openclaw"]["hooks"].values():
    hook["enabled"] = enabled

dest.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
PY
}

printf 'Installing public Codex/OMX config into %s\n' "$target_home"

sync_tree "$repo_root/home/AGENTS.md" "$target_home/"
sync_tree "$repo_root/home/CLAUDE.md" "$target_home/"
sync_tree "$repo_root/home/.codex/" "$target_home/.codex/"
sync_tree "$repo_root/home/.agents/" "$target_home/.agents/"
sync_tree "$repo_root/home/.omx/agents/" "$target_home/.omx/agents/"
sync_tree "$repo_root/home/.claude/" "$target_home/.claude/"
sync_tree "$repo_root/home/vendor_imports/" "$target_home/vendor_imports/"

render_text "$repo_root/templates/.codex/config.toml" "$target_home/.codex/config.toml"
render_text "$repo_root/templates/.codex/hooks.json" "$target_home/.codex/hooks.json"
render_omx_json "$repo_root/templates/.codex/.omx-config.json" "$target_home/.codex/.omx-config.json"
render_text "$repo_root/templates/.claude/config.toml" "$target_home/.claude/config.toml"
render_text "$repo_root/templates/.claude/settings.json" "$target_home/.claude/settings.json"
render_text "$repo_root/templates/shell/zshrc.codex-fragment.zsh" "$target_home/.config/codex/zshrc.codex-fragment.zsh"

if [[ "$dry_run" -eq 1 ]]; then
  printf '[dry-run] install api-key helper -> %s\n' "$target_home/.claude/api-key-helper.sh"
else
  mkdir -p "$target_home/.claude" "$target_home/.config/codex"
  install -m 0755 "$repo_root/templates/.claude/api-key-helper.sh" "$target_home/.claude/api-key-helper.sh"
  install -m 0644 "$repo_root/templates/.config/codex/env.example" "$target_home/.config/codex/env.example"
fi

printf 'Done. If this is a fresh machine, run: omx doctor\n'
