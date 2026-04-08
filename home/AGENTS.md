# Global Agent Triggers

This file applies to all projects under `/Users/zhishixuebao`.

## Natural-language trigger: Claude brain + Codex hands

When user text contains any of:
- `claude code协同`
- `opus4.6当大脑`
- `codex当员工`
- `脑产品经理`
- `brain-pm-hand-exec`
- `同时用codex和claude工作`
- `codex和claude协同`
- `codex+claude`
- `双模型协同`
- `codex claude duo`

Then immediately run this staged team workflow with `omx team`:

1) `team-plan` (Claude PM/architect)
- Use `OMX_TEAM_WORKER_CLI=claude`
- Ask for PRD, architecture, acceptance criteria, and test plan.

2) `team-exec` (Codex implementation)
- Use `OMX_TEAM_WORKER_CLI=codex`
- Set `OMX_TEAM_WORKER_LAUNCH_ARGS="--model gpt-5.3-codex"`
- Implement against stage-1 outputs and run verification.

3) `team-verify` (Claude review)
- Use `OMX_TEAM_WORKER_CLI=claude`
- Review deltas vs architecture and output fix list or sign-off.

Operational requirements:
- Team mode must run inside tmux.
- Use `omx team status <team>` for progress checks.
- Only run `omx team shutdown <team>` when tasks are terminal (`pending=0`, `in_progress=0`, `failed=0`) unless user explicitly asks to abort.

Reporting:
- Return a single merged report with sections: `Architecture`, `Implementation`, `Verification`, `How to rerun`.

## Default duo workflow command (works in VS Code terminals too)

When the trigger is about running Codex and Claude together (including the five Chinese/English phrases above),
prefer this fixed launcher first:

```bash
codex-claude-duo "<task>"
```

Behavior contract:
- If already inside tmux: run `OMX_TEAM_WORKER_CLI_MAP=codex,claude omx team 2:executor "<task>"`.
- If outside tmux: create/attach a tmux leader session and run the same command inside it.
- Do not ask for confirmation before starting.

## Natural-language trigger: Claude supervisor + Codex worker

When user text contains any of:
- `claude当监工`
- `claude监工`
- `监工大脑`
- `claude指挥codex`
- `claude操控codex`
- `claude-supervisor-codex`
- `监工执行模式`

Then immediately load and follow skill:

- `claude-supervisor-codex-worker` (shared skill path: `/Users/zhishixuebao/.codex/memories/skills/claude-supervisor-codex-worker`)

Execution contract:
- Run `claude-codex-supervisor "<task>"` first.
- Claude is responsible for planning/review; Codex is responsible for implementation.
- Return one merged report with sections: `Architecture`, `Implementation`, `Verification`, `How to rerun`.

## Natural-language trigger: Paper outline + ER workflow

When user text contains any of:
- `论文目录模板`
- `ER图工作流`
- `数据库表图优化`
- `论文ER图美化`
- `毕业论文固定模板`

Then immediately load and follow skill:

- `paper-er-workflow` (shared skill path: `/Users/zhishixuebao/.agents/skills/paper-er-workflow`)

Execution contract:
- Use `templates/outline-template.md` for chapter skeleton output.
- Use `templates/er-dod-checklist.md` as acceptance gate.
- If user requests Claude+Codex collaboration, pair this skill with the duo workflow above.

## Natural-language trigger: Academic de-AI rewriting

When user text contains any of:
- `论文降AI`
- `降低AI率`
- `降低查重率`
- `学术化改写`
- `论文降重`
- `摘要降AI`
- `academic humanize`
- `lower ai rate`
- `de-ai academic writing`

Then immediately load and follow skill:

- `academic-humanizer-zh` (shared skill path: `/Users/zhishixuebao/.codex/memories/skills/academic-humanizer-zh`)

Execution contract:
- Preserve original meaning, stance, terminology, and argument structure.
- Do not fabricate data, references, authors, dates, or conclusions.
- Prefer minimal rewriting first: reduce repetitive AI patterns, then lightly vary sentence form.
- If information is missing, explicitly say `信息不足以判断` or `原文未说明`.

