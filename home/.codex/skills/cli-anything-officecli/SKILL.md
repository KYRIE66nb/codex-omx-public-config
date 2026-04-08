---
name: cli-anything-officecli
description: Check, fix, report, and generate thesis-style DOCX files from natural-language instructions by wrapping the real officecli binary.
---

# cli-anything-officecli

Use this when you need a thesis-focused wrapper over `officecli` for `.docx`
files instead of low-level paragraph commands, including thesis generation from
task books or proposal reports.

## Prerequisite

`officecli` must already be installed and available in `PATH`.

## Commands

```bash
cli-anything-officecli check paper.docx
cli-anything-officecli fix paper.docx --dry-run
cli-anything-officecli fix paper.docx
cli-anything-officecli report paper.docx --output report.md
cli-anything-officecli --json check paper.docx
cli-anything-officecli ask "根据这个任务书写一篇论文" --source task.docx --out-dir out
cli-anything-officecli pipeline --source task.docx --out-dir out
cli-anything-officecli extract --source task.docx --json
cli-anything-officecli write --source task.docx --out-dir out
```

## Behavior

- `check` reads `/body` from the real Word file through `officecli`
- `fix` applies only clear paragraph-style fixes
- `report` writes a Markdown or JSON artifact
- `ask` routes natural-language instructions into the thesis workflow
- `pipeline` runs the deterministic thesis workflow directly
- `extract` converts source material into structured thesis requirements
- `write` generates `requirements.json`, `outline.md`, `draft.docx`, and `report.md`
- `--profile` loads an external JSON rule set
- `--json` returns machine-readable output for agents

## Natural-Language Triggers

Use prompts like:

- `帮我分析这个任务书或者开题报告`
- `根据这个任务书写一篇论文`
- `根据以下要求写一篇论文`
- `把这篇论文整理成符合要求的 Word 文档`

## Default Role Mapping

- `第一章 绪论` or `Chapter 1` -> `Heading1`
- `1.1 研究背景` -> `Heading2`
- `1.1.1 研究问题` -> `Heading3`
- fallback body paragraphs -> `Normal`
