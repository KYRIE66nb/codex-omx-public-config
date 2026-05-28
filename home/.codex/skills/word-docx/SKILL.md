---
name: word-docx
description: Word and DOCX editing alias for Documents and officecli-docx.
---

# Word DOCX

Use this skill when the user asks to create, edit, review, format, redline, comment on, or render Word/DOCX documents.

This is a strong routing skill, not a thin alias. Do not stop after reading this file.
For Word work, choose the smallest safe downstream instruction set before editing:

1. `documents` plugin skill for artifact creation, editing, redlines, comments, rendering, and layout verification.
2. `doc` for DOCX read/create/edit workflows.
3. `officecli-docx` for precise OfficeCLI-based `.docx` inspection and edits.
4. `officecli` when the task needs broader OfficeCLI examples, Word tables, figures, headers/footers, equations, or cross-format work.
5. `lunwen-format-docx` for Chinese thesis formatting.

Prefer structured DOCX tools over plain text rewriting when the file format, comments, tables, pagination, or layout matters.

## Efficiency Gate

Use a targeted fast path for small, local, reversible edits: one formula style, one picture size/position/alt-text adjustment, one typo/text replacement, or one paragraph/list/table-cell formatting change.

Fast path requirements:

- Inspect the affected paragraph/run/table cell/image/equation before editing.
- Use the most direct structured edit available.
- Re-inspect only the affected object or immediate neighborhood after editing.
- Run `officecli validate` or the cheapest equivalent structural check.
- Escalate to the full workflow if the target cannot be located precisely, validation fails, layout changes are visible/likely, or the user asks for final/client-ready output.

Full workflow is still required for thesis/formal documents, redlines/comments, templates, tables spanning pages, headers/footers, TOC, references, citations, tracked changes, multiple layout regions, pagination-sensitive work, or final PDF/print-ready delivery.

Quality rules:

- Never use this alias as the only context for a real DOCX job.
- Inspect the existing document structure before editing.
- Preserve the original file unless the user explicitly asks to overwrite it.
- For layout-sensitive deliverables, render pages to images and visually inspect them before claiming completion.
- For fast-path localized edits, do not render the whole document unless targeted checks show layout risk.
- For thesis, forms, tables, headers/footers, tracked changes, comments, references, TOC, or equations, read the relevant downstream task guide or OfficeCLI section first.
