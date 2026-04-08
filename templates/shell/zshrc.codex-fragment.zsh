export PATH="$HOME/.local/bin:$PATH"

# Load private API keys from an untracked file.
[[ -f "$HOME/.config/codex/env" ]] && source "$HOME/.config/codex/env"

export OMX_OPENCLAW="${OMX_OPENCLAW:-1}"
export NODE_USE_SYSTEM_CA="1"
export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC="1"
export CLAUDE_CODE_ATTRIBUTION_HEADER="0"

claude() {
  "$HOME/.local/bin/claude" --dangerously-skip-permissions --permission-mode bypassPermissions "$@"
}

claude-official() {
  "$HOME/.local/bin/claude" \
    --setting-sources local,project \
    --settings "$HOME/.claude/settings.official.json" \
    --dangerously-skip-permissions \
    --permission-mode bypassPermissions \
    "$@"
}

claude-official-status() {
  "$HOME/.local/bin/claude" --setting-sources local auth status 2>/dev/null
}

codex() {
  local has_model_flag=0
  local has_context_flag=0
  local codex_bin
  local arg
  codex_bin="$(whence -p codex)"

  for arg in "$@"; do
    case "$arg" in
      -m|--model|--model=*)
        has_model_flag=1
        ;;
      model_context_window=*|--config=model_context_window=*|-cmodel_context_window=*)
        has_context_flag=1
        ;;
    esac
  done

  if [[ $has_model_flag -eq 1 ]]; then
    if [[ $has_context_flag -eq 1 ]]; then
      env -u OPENAI_BASE_URL "$codex_bin" "$@"
    else
      env -u OPENAI_BASE_URL "$codex_bin" -c model_context_window=1050000 "$@"
    fi
  else
    if [[ $has_context_flag -eq 1 ]]; then
      env -u OPENAI_BASE_URL "$codex_bin" -m gpt-5.4 "$@"
    else
      env -u OPENAI_BASE_URL "$codex_bin" -m gpt-5.4 -c model_context_window=1050000 "$@"
    fi
  fi
}

_terminal_auto_attach_tmux() {
  [[ -o interactive ]] || return
  [[ -n "${TMUX:-}" ]] && return
  [[ "${TERM_PROGRAM:-}" == "Apple_Terminal" ]] || return
  [[ -n "${SSH_CONNECTION:-}${SSH_TTY:-}" ]] && return
  [[ "${TERMINAL_AUTO_TMUX:-1}" == "1" ]] || return
  command -v tmux >/dev/null 2>&1 || return
  exec tmux new-session -A -s main
}

# Uncomment if you want Apple Terminal to auto-attach into tmux.
# _terminal_auto_attach_tmux
