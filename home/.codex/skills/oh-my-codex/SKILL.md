---
name: oh-my-codex
keyword: omx
description: "OMX multi-agent orchestration."
allowed-tools:
- Read
- Write
- Bash
- Grep
- Glob
tags:
- omx
- multi-agent
- orchestration
- codex
- openai
- team-mode
- mcp-servers
- workflow
platforms:
- Codex
- Claude
- Gemini
version: 0.14.3
source: Yeachan-Heo/oh-my-codex
---

# oh-my-codex (OMX)

Use this skill when you need multi-agent orchestration, team workers, persistent state, or OMX-specific read-only shell routing.

## What It Covers

- Role prompts for `architect`, `planner`, `executor`, `debugger`, `verifier`, `explore`, and the review/domain roles
- Workflow skills like `$autopilot`, `$ralph`, `$ultrawork`, `$team`, `$plan`, `$tdd`, `$build-fix`, `$code-review`, `$security-review`, and `$cancel`
- `omx explore` for read-only lookup
- `omx sparkshell` for bounded shell summaries
- `omx adapt` for external target adapter setup
- Persistent MCP servers for state, memory, code intelligence, and traces

## Install & Refresh

```bash
npm install -g @openai/codex oh-my-codex
omx setup
omx doctor
```

If the repo or config changes later, rerun `omx update` or `omx setup` to refresh the shipped assets.

## Common Usage

```text
/prompts:architect "analyze current auth boundaries"
/prompts:executor "implement input validation in login"
/prompts:security-reviewer "audit OAuth flow"
```

```text
$plan "ship OAuth callback safely"
$team 3:executor "fix all TypeScript errors"
$ralph "finish the refactor and verify"
```

```bash
omx team 4:executor "parallelize a multi-module refactor"
omx team status <team-name>
omx team shutdown <team-name>
```

## Quick Reference

| Command | Action |
|---------|--------|
| `omx` | Launch Codex with HUD |
| `omx setup` | Install prompts, skills, and config wiring |
| `omx update` | Refresh installed OMX assets |
| `omx doctor` | Installation/runtime diagnostics |
| `omx team <n>:<role> "<task>"` | Start team workers |
| `omx explore` | Read-only repository lookup |
| `omx sparkshell` | Bounded shell summaries |
| `omx adapt` | Adapter workflow for external targets |
| `omx status` | Show active modes |
| `omx cancel` | Cancel execution modes |
| `omx reasoning <mode>` | Set reasoning level |
| `omx hud` | HUD display options |
| `omx help` | Show help |

## Notes

- Keep AGENTS.md injection enabled unless you have a strong reason to bypass it.
- Prefer `omx team` only when parallel coordination actually helps.
- Use `omx --xhigh --madmax` only in trusted environments.

