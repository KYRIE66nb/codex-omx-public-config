---
name: doc
description: "Read, create, and edit DOCX."
---


# DOCX Skill

## When to use
- Read or review DOCX content where layout matters (tables, diagrams, pagination).
- Create or edit DOCX files with professional formatting.
- Validate visual layout before delivery.

## Workflow
1. Classify the task before choosing verification depth.
   - Use fast path for localized, reversible edits with a precise target and low layout risk.
   - Use delivery path for creating documents, final/client-ready outputs, pagination-sensitive edits, formal/thesis work, or broad formatting changes.
2. Prefer visual review (layout, tables, diagrams) on delivery path.
   - If `soffice` and `pdftoppm` are available, convert DOCX -> PDF -> PNGs.
   - Or use `scripts/render_docx.py` (requires `pdf2image` and Poppler).
   - If these tools are missing, install them or ask the user to review rendered pages locally.
3. Use `python-docx` for edits and structured creation (headings, styles, tables, lists).
4. On fast path, inspect the affected object before and after the edit, then run a structural validation or targeted extraction check. Do not convert the entire document unless the change may affect layout.
5. On delivery path, after each meaningful layout change, re-render and inspect the relevant pages; re-render the whole document before final delivery when pagination or page flow matters.
6. If visual review is not possible, extract text with `python-docx` as a fallback and call out layout risk.
7. Keep intermediate outputs organized and clean up after final approval.

## Temp and output conventions
- Use `tmp/docs/` for intermediate files; delete when done.
- Write final artifacts under `output/doc/` when working in this repo.
- Keep filenames stable and descriptive.

## Dependencies (install if missing)
Prefer `uv` for dependency management.

Python packages:
```
uv pip install python-docx pdf2image
```
If `uv` is unavailable:
```
python3 -m pip install python-docx pdf2image
```
System tools (for rendering):
```
# macOS (Homebrew)
brew install libreoffice poppler

# Ubuntu/Debian
sudo apt-get install -y libreoffice poppler-utils
```

If installation isn't possible in this environment, tell the user which dependency is missing and how to install it locally.

## Environment
No required environment variables.

## Rendering commands
DOCX -> PDF:
```
soffice -env:UserInstallation=file:///tmp/lo_profile_$$ --headless --convert-to pdf --outdir $OUTDIR $INPUT_DOCX
```

PDF -> PNGs:
```
pdftoppm -png $OUTDIR/$BASENAME.pdf $OUTDIR/$BASENAME
```

Bundled helper:
```
python3 scripts/render_docx.py /path/to/file.docx --output_dir /tmp/docx_pages
```

## Quality expectations
- Deliver a client-ready document: consistent typography, spacing, margins, and clear hierarchy.
- Avoid formatting defects: clipped/overlapping text, broken tables, unreadable characters, or default-template styling.
- Charts, tables, and visuals must be legible in rendered pages with correct alignment.
- Use ASCII hyphens only. Avoid U+2011 (non-breaking hyphen) and other Unicode dashes.
- Citations and references must be human-readable; never leave tool tokens or placeholder strings.

## Final checks
- Fast path: confirm the targeted edit, run structural validation or targeted extraction, and state that full-page rendering was intentionally skipped because the change was localized.
- Delivery path: re-render and inspect every page at 100% zoom before final delivery.
- Fix any spacing, alignment, or pagination issues and repeat the relevant render loop.
- Confirm there are no leftovers (temp files, duplicate renders) unless the user asks to keep them.
