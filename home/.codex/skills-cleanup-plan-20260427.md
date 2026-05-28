# Skill Cleanup Plan - 2026-04-27

Goal: reduce Codex startup skill-index pressure while preserving high-value capabilities.

Priority capabilities to keep active:
- Code: feature work, debugging, refactor, tests, review, security, GitHub, browser testing.
- Office/Word: docx, officecli, thesis formatting, PPT/XLSX document tooling.
- Drawing/media: image generation, paper figures, plots, diagrams, pixel art, video/Sora.
- Multi-agent: team, ralph, ralplan, ultrawork, ultraqa, trace, worker, subagent planning.
- Discovery/recovery: skill management, find/install skills, help, doctor, handoff, note.
- Data analysis: spreadsheets, CSV/XLSX analysis, statistical tests, regression/time series, scientific computing, graph analysis, and publication plots.

Cleanup rules:
- Do not delete skills.
- Move legacy or lower-priority skills to a timestamped archive under `~/.codex/skill-archive/`.
- Prefer keeping `~/.codex/skills` as the active root.
- Remove `.agents/skills` duplicates first; migrate unique high-priority `.agents` skills into `.codex/skills`.
- Keep `paper-er-workflow` active because `AGENTS.md` references its `.agents` path directly.
- After moving, run `omx doctor` and recount active `SKILL.md` files.

Initial archive candidates:
- `.agents/skills` duplicates already present under `.codex/skills`.
- Scientific/math modeling helpers not needed for code/Office/drawing/multi-agent priority.
- Specialized research pipeline variants that can be restored on demand.
- Simulink/MATLAB niche skills unless explicitly needed.

Rollback:
- Move any archived directory back from `~/.codex/skill-archive/<timestamp>/...` to its original path.

Execution log:
- 2026-04-27: migrated active skills into `~/.codex/skills` and cleared legacy `.agents/skills` scanning overlap.
- 2026-04-27: shortened long system-skill frontmatter descriptions while preserving full skill bodies.
- 2026-04-27: archived low-priority and overlapping skill entries to `~/.codex/skill-archive/20260427-201024/`.
- 2026-04-27: restored `swarm` after verification because `AGENTS.md` still documents it as a team compatibility trigger.
- 2026-04-27: restored high-value data analysis skills (`statistical-analysis`, `statistical-modeling-coder-zh`, `statsmodels`, `scipy`, `sympy`, `networkx`) and added `data-analysis` as the protected data-analysis routing skill.
- 2026-04-27: added protected aliases `word-docx`, `excel-xlsx`, and `csv`; restored coding-quality skills `security-best-practices`, `vercel-react-best-practices`, `bug-finder`, `test-driven-development`, `systematic-debugging`, `frontend-design`, `frontend-ui-ux`, and `ui-designer`.
- 2026-04-28: rolled back the low-priority skill archive for quality reasons; restored non-duplicate archived skills into `~/.codex/skills`.
- 2026-04-28: added a global protected-lane context override so Word/Office, data/statistics, and coding tasks load full downstream instructions instead of relying on short alias summaries.
- 2026-04-28: switched the superpower/using-superpowers workflow to Legacy Quality Mode: when skill context size and output quality conflict, load the full relevant skill stack and preserve quality.

Final state:
- `.agents/skills` was removed after high-priority unique entries were migrated to `.codex/skills`.
- Broken `.codex/skills` symlinks were replaced with real directories.
- Skill descriptions were shortened in frontmatter only; skill bodies were preserved.
