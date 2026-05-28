---
name: cli-anything
description: "Build and validate CLI apps."
---

# CLI-Anything for Codex

Use this skill when the user wants Codex to act like the `CLI-Anything` builder.

If this skill is being used from inside the `CLI-Anything` repository, read `../cli-anything-plugin/HARNESS.md` before implementation. That file is the full methodology source of truth. If it is not available, follow the condensed rules below.

## Inputs

Accept either:

- A local source path such as `./gimp` or `/path/to/software`
- A GitHub repository URL

Derive the software name from the local directory name after cloning if needed.

## Modes

### Build

Use when the user wants a new harness.

Produce this structure:

```text
<software>/
└── agent-harness/
    ├── <SOFTWARE>.md
    ├── setup.py
    └── cli_anything/
        └── <software>/
            ├── README.md
            ├── __init__.py
            ├── __main__.py
            ├── <software>_cli.py
            ├── core/
            ├── utils/
            └── tests/
```

Implement a stateful Click CLI with:

- one-shot subcommands
- REPL mode as the default when no subcommand is given
- `--json` machine-readable output
- session state with undo/redo where the target software supports it

### Refine

Use when the harness already exists.

First inventory current commands and tests, then do gap analysis against the target software. Prefer:

- high-impact missing features
- easy wrappers around existing backend APIs or CLIs
- additions that compose well with existing commands

Do not remove existing commands unless the user explicitly asks for a breaking change.

For Word/docx targets, prioritize:

- styles and style inheritance
- paragraph and run-level formatting
- page setup, margins, section breaks, and page breaks
- headers, footers, footnotes, and endnotes
- tables, captions, lists, and numbering
- inline and display equations
- preserving layout semantics instead of flattening content into plain text

### Word/docx Target Checklist

When the target is a Word editor or `.docx` workflow, the harness should usually expose these areas first:

| Area | What to cover | Red flag |
|------|---------------|----------|
| Structure | paragraphs, runs, tables, sections, headers, footers | only plain-text read/write |
| Formatting | fonts, bold/italic, spacing, alignment, indentation, styles | formatting lost after round-trip |
| Layout | margins, page size, pagination, section breaks, line/page breaks | layout changes silently |
| Numbering | bullets, numbered lists, captions, headings | numbering resets or desyncs |
| Equations | inline math, display equations, equation insertion/update | equations become images or text blobs |
| References | footnotes, endnotes, captions, cross-references, TOC hooks | references cannot be preserved |
| Validation | schema checks, render/preview, diff after save | no round-trip verification |

Prefer wrappers that operate on document structure rather than string replacement. If the backend supports styles, tables, equations, or section-aware editing, those should be modeled as first-class commands instead of hidden behind a generic `edit` action.

### Word/docx Test Focus

For Word/docx harnesses, write tests that prove:

- formatting survives save/load
- equations round-trip without loss of semantic structure
- section and page layout stay stable
- list numbering and table structure remain intact
- headers and footers do not disappear
- the harness rejects unsafe plain-text-only fallbacks when richer editing is available

### Word/docx Common Gaps

- The harness can read text but cannot target runs, styles, or equations.
- The harness edits content but breaks page layout or section structure.
- The harness has no stable pathing for paragraphs, tables, or equation nodes.
- The harness exports or validates without checking the rendered result.

### Test

Plan tests before writing them. Keep both:

- `test_core.py` for unit coverage
- `test_full_e2e.py` for workflow and backend validation

When possible, test the installed command via subprocess using `cli-anything-<software>` rather than only module imports.

### Validate

Check that the harness:

- uses the `cli_anything.<software>` namespace package layout
- has an installable `setup.py` entry point
- supports JSON output
- has a REPL default path
- documents usage and tests

## Backend Rules

Prefer the real software backend over reimplementation. Wrap the actual executable or scripting interface in `utils/<software>_backend.py` when possible. Use synthetic reimplementation only when the project explicitly requires it or no viable native backend exists.

For Word/docx specifically, prefer a backend that preserves structure and layout. Avoid naive text replacement when the target supports styles, tables, equations, or section-aware editing.

## Packaging Rules

- Use `find_namespace_packages(include=["cli_anything.*"])`
- Keep `cli_anything/` as a namespace package without a top-level `__init__.py`
- Expose `cli-anything-<software>` through `console_scripts`

## Workflow

1. Acquire the source tree locally.
2. Analyze architecture, data model, existing CLIs, and GUI-to-API mappings.
3. Design command groups and state model.
4. Implement the harness.
5. Write `TEST.md`, then tests, then run them.
6. Update README usage docs.
7. Verify local installation with `pip install -e .`

## Output Expectations

When reporting progress or final results, include:

- target software and source path
- files added or changed
- validation commands run
- open risks or backend limitations

For Word/docx harnesses, call out equation coverage and layout fidelity explicitly.
