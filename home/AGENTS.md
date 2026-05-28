# Global Agent Triggers

This file applies to all projects under `/Users/zhishixuebao`.

Workspace preference:
- For future Codex multi-agent collaboration, default Codex child agents and Codex-backed team workers to `gpt-5.5` with `xhigh` reasoning unless the user explicitly asks for another model or lower effort.
- Before answering, asking clarifying questions, or taking action, first apply the `superpower` skill alias. This means checking whether any available skill applies and loading the relevant skill before continuing. Treat `superpower`, `superpowers`, and `using-superpowers` as the same pre-response skill-check workflow.
- Use quality-preserving fast paths when the task is small, local, and reversible. Do targeted inspection and targeted verification first; escalate to full downstream skills, rendering, or multi-agent work only when the file type, scope, risk, or user-facing deliverable requires it.

## Natural-language trigger: Superpower preflight

When user text contains any of:
- `superpower`
- `superpowers`
- `using-superpowers`
- `先加载superpower`
- `先检查skill`
- `回答前先加载skill`

Then immediately load and follow skill:

- `superpower` (alias skill path: `/Users/zhishixuebao/.codex/skills/superpower/SKILL.md`)
- Canonical workflow: `/Users/zhishixuebao/.codex/skills/using-superpowers/SKILL.md`

Execution contract:
- Check applicable skills before any response or action.
- If a specific skill applies, load it and follow it.
- If no specific skill applies, answer or act normally after this preflight.

## Protected capability lanes

These capability lanes must stay active and must not be archived or weakened during skill cleanup:

1. Word/Office document editing
- Primary skills/plugins: `word-docx`, `doc`, `officecli`, `officecli-docx`, `officecli-xlsx`, `officecli-pptx`, `cli-anything-officecli`, Documents, Spreadsheets, Presentations.
- Trigger examples: `Word`, `docx`, `编辑文档`, `改论文格式`, `表格文件`, `PPT`, `Excel`.

2. Data analysis
- Primary skills/plugins: `data-analysis`, `excel-xlsx`, `csv`, `analyze-results`, `plot-from-data`, `plot-from-image`, `statistical-analysis`, `statistical-modeling-coder-zh`, `statsmodels`, `scipy`, `sympy`, `networkx`, `officecli-xlsx`, Spreadsheets.
- Trigger examples: `数据分析`, `统计分析`, `CSV`, `XLSX`, `Excel`, `画图`, `回归`, `时间序列`, `实验结果分析`, `数据可视化`.

3. Coding and software engineering
- Primary skills: `develop-feature`, `fix-bug`, `bug-finder`, `systematic-debugging`, `build-fix`, `refactor`, `tdd`, `test-driven-development`, `code-review`, `security-review`, `security-best-practices`, `git`, `github`, `playwright`, `agent-browser`, `frontend-skill`, `frontend-design`, `frontend-ui-ux`, `ui-designer`, `vercel-react-best-practices`, `web-clone`.
- Trigger examples: `写代码`, `开发`, `修 bug`, `构建失败`, `类型错误`, `重构`, `测试`, `代码审查`, `前端`.

When a request fits one of these lanes, load the lane's primary skill before considering lower-priority or more niche skills.

## Legacy Skill Quality Mode

Quality and capability take priority over context minimization.
Operate skills in the pre-context-limit style: when a task matches a skill, load the full primary skill instructions and the relevant downstream task guides/tool references before acting. Short alias skills are only routers, never sufficient execution context.

Native Codex may still compact the startup skill catalog to fit its own metadata budget. Treat that catalog as discovery only: do not infer that truncated descriptions authorize skipping skill files. The authoritative workflow is to open and read every applicable `SKILL.md` plus directly relevant downstream guides before acting.

Context-saving is allowed only after the agent has the operational details needed to do the task well. Do not skip examples, caveats, QA gates, rendering steps, command sequencing rules, or troubleshooting notes when they are relevant to the requested deliverable.

- Word/Office work: load `word-docx` first, then load only the downstream guides needed for the actual risk surface. For small localized edits (single formula style, one image adjustment, typo/text replacement, one paragraph/list/table-cell formatting change), use targeted structure inspection plus `validate`/local checks before full rendering. Load full `documents`, `doc`, `officecli`, and `officecli-docx` instructions and render/visually verify when creating deliverables, editing thesis/formal documents, touching pagination/TOC/headers/footers/references, changing multiple layout regions, or when targeted checks reveal layout risk.
- Data/statistics work: load the domain skill and the concrete library/workflow skill that matches the task (`data-analysis`, `statistical-analysis`, `statsmodels`, `scipy`, `sympy`, `networkx`, `excel-xlsx`, or `csv`) instead of relying only on alias summaries.
- Coding work: load the concrete workflow skill (`develop-feature`, `fix-bug`, `build-fix`, `refactor`, `tdd`, `code-review`, `security-review`, frontend skills, or Playwright skills) before implementation or review.

Progressive disclosure should only filter clearly irrelevant files. It must not remove operational knowledge needed for quality. If there is a conflict between saving context and preserving task quality, preserve task quality.

## Quality-Preserving Efficiency Gates

Default to the lightest workflow that can prove correctness.

Fast path is allowed only when all are true:
- The request is localized, reversible, and has a narrow blast radius.
- The user is not asking for final/client-ready/thesis/legal/regulatory delivery.
- The edit does not affect pagination, section breaks, global styles, TOC, citations, references, headers/footers, tracked changes, or document-wide layout.
- A targeted pre/post check can prove the requested change and a structural validator can catch file corruption.

Fast path still requires verification:
- Inspect the affected object or nearby structure before editing.
- Make the smallest structured edit available.
- Re-inspect the affected object after editing.
- Run the cheapest relevant validator or consistency check.
- Report any skipped full-render/full-QA step as an intentional fast-path tradeoff.

Escalate to full delivery workflow immediately when:
- The targeted check fails, is ambiguous, or indicates layout drift.
- The document is long/formal or the change touches multiple regions.
- The task involves final delivery quality, printing, PDF export, visual placement, page flow, or cross-reference correctness.

## Natural-language trigger: Claude brain + Codex hands

Launch this workflow only when the user is explicitly asking to start, run, or use Claude+Codex collaboration for the current task and the text contains any of:
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

Do not activate this workflow when the user is merely discussing, debugging, quoting, searching for, or asking about these phrases or multi-agent collaboration behavior.

Then run this staged team workflow with `omx team` only from an attached tmux OMX CLI shell. In Codex App/native outside-tmux sessions, stay on the nearest app-safe surface unless the user explicitly asks to launch the external tmux runtime.

1) `team-plan` (Claude PM/architect)
- Use `OMX_TEAM_WORKER_CLI=claude`
- Ask for PRD, architecture, acceptance criteria, and test plan.

2) `team-exec` (Codex implementation)
- Use `OMX_TEAM_WORKER_CLI=codex`
- Set `OMX_TEAM_WORKER_LAUNCH_ARGS="--model gpt-5.5 -c model_reasoning_effort=\"xhigh\""`
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

After the explicit launch gate above passes, prefer this fixed launcher first:

```bash
codex-claude-duo "<task>"
```

Behavior contract:
- If already inside tmux: run `OMX_TEAM_WORKER_CLI_MAP=codex,claude omx team 2:executor "<task>"`.
- If outside tmux: create/attach a tmux leader session and run the same command inside it.
- Do not run this launcher for discussion, debugging, quoting, or search requests that only mention Codex+Claude collaboration.
- Do not ask for confirmation before starting.

## Natural-language trigger: Claude supervisor + Codex worker

Launch this workflow only when the user is explicitly asking to start, run, or use Claude-supervised Codex execution and the text contains any of:
- `claude当监工`
- `claude监工`
- `监工大脑`
- `claude指挥codex`
- `claude操控codex`
- `claude-supervisor-codex`
- `监工执行模式`

Do not activate this workflow when the user is merely discussing, debugging, quoting, searching for, or asking about these phrases.

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

- `paper-er-workflow` (shared skill path: `/Users/zhishixuebao/.codex/skills/paper-er-workflow`)

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
