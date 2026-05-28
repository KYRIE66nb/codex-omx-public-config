---
name: officecli
description: "Work with Office documents."
---

# officecli

AI-friendly CLI for `.docx`, `.xlsx`, `.pptx`.

## Install

```bash
if ! command -v officecli >/dev/null 2>&1; then
  curl -fsSL https://raw.githubusercontent.com/iOfficeAI/OfficeCLI/main/install.sh | bash
fi
```

```powershell
if (-not (Get-Command officecli -ErrorAction SilentlyContinue)) {
  irm https://raw.githubusercontent.com/iOfficeAI/OfficeCLI/main/install.ps1 | iex
}
```

Verify with `officecli --version`.

## Strategy

Prefer higher-level operations first:

- `L1` read
- `L2` DOM edit
- `L3` raw XML

Use `--json` when you need structured output.

## Help First

If you are unsure about paths or property names, run help instead of guessing:

```bash
officecli pptx set
officecli pptx set shape
officecli pptx set shape.fill
```

Swap `pptx` for `docx` or `xlsx`.

## Core Workflow

For multi-step edits, keep the file resident:

```bash
officecli open report.docx
officecli set report.docx ...
officecli close report.docx
```

For visual review and targeted edits, use watch/selection/marks:

```bash
officecli watch report.docx
officecli get report.docx selected --json
officecli mark report.docx /body/p[3] --prop find=foo --prop tofix=bar
officecli get-marks report.docx --json
officecli unmark report.docx --all
officecli unwatch report.docx
```

## Main Commands

- `create`
- `view`
- `get`
- `query`
- `validate`
- `set`
- `add`
- `move`
- `swap`
- `remove`
- `batch`
- `raw`
- `raw-set`

## Notes

- Paths are `1`-based; `--index` is `0`-based.
- Prefer stable IDs like `@id=` or `@paraId=` when a path must survive insert/delete.
- Use `view issues` to catch formatting, content, and structure problems early.
- For large documents, limit output with `--max-lines`.
- Close the file in Office/WPS before editing it.

## Related Skills

- `officecli-docx`
- `officecli-pptx`
- `officecli-xlsx`
- `officecli-academic-paper`
- `officecli-pitch-deck`
- `officecli-data-dashboard`
- `morph-ppt`

