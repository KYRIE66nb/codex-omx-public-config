# Lunwen Draw.io PNG Bridge Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a `drawio`-aware asset bridge to the `lunwen` skill so thesis workflows can generate local PNG diagram assets for flowcharts, functional structure diagrams, and logical ER diagrams while preserving Graphviz-first handling for Chen-style conceptual ER diagrams.

**Architecture:** Keep the existing `image-map -> generate_thesis_docx.py` pipeline unchanged. Add a new manifest-driven Python tool that routes supported diagram definitions either through a draw.io lightbox PNG export path or the existing Graphviz renderer, and update skill docs to make the routing rules explicit.

**Tech Stack:** Python 3, `unittest`, `subprocess`, `Pillow`, Graphviz `dot`, `npx playwright`, Chrome channel

---

### Task 1: Add failing tests for manifest parsing and routing

**Files:**
- Create: `tests/test_generate_drawio_assets.py`
- Create: `tests/fixtures/drawio-assets/manifest.json`
- Modify: `tools/generate_drawio_assets.py`

**Step 1: Write the failing test**

Add tests that expect:
- manifest loading to normalize diagram entries
- Mermaid-capable diagram types to route to `drawio`
- Chen conceptual ER diagrams to route to `graphviz`
- draw.io URL generation to include `lightbox=1`
- whitespace trimming helper to reduce oversized borders

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_generate_drawio_assets -v`
Expected: FAIL because `tools/generate_drawio_assets.py` does not exist yet.

**Step 3: Write minimal implementation**

Create the bridge module with importable helpers and a CLI entrypoint.

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_generate_drawio_assets -v`
Expected: PASS

### Task 2: Implement the draw.io PNG bridge

**Files:**
- Create: `tools/generate_drawio_assets.py`

**Step 1: Implement manifest parsing**

Support a JSON manifest with:
- top-level `diagrams`
- each item containing `id`, `title`, `type`, `engine`, `content`, `output`
- optional screenshot and trim settings

**Step 2: Implement routing**

Rules:
- `flowchart`, `functional_structure`, `logical_er` default to `drawio`
- `conceptual_er` defaults to `graphviz`
- explicit `engine` overrides the default when valid

**Step 3: Implement draw.io export**

For draw.io-routed diagrams:
- generate the official `app.diagrams.net` `#create=` URL using the draw.io MCP compression scheme
- use `npx playwright screenshot --channel=chrome` to capture a PNG from lightbox mode
- trim near-white borders with Pillow

**Step 4: Implement Graphviz export**

For Graphviz-routed diagrams:
- call `tools/render_graphviz.py`
- only allow DOT content

**Step 5: Emit artifacts**

Write:
- final PNG assets
- optional source sidecars (`.mmd`, `.dot`)
- a result manifest for downstream image mapping

### Task 3: Update lunwen workflow docs

**Files:**
- Modify: `SKILL.md`
- Modify: `prompts/diagram_designer.md`
- Modify: `references/diagram-conventions.md`
- Modify: `README.md`

**Step 1: Document routing rules**

Clarify that:
- `drawio-mcp` enhances PNG-first generation for Mermaid-friendly diagrams
- Graphviz remains the default for Chen conceptual ER diagrams
- Mermaid `erDiagram` is still only for logical ER drafts or table-relation views

**Step 2: Add tool usage examples**

Document:
- manifest format
- command examples
- output directory expectations

### Task 4: Verify end-to-end behavior

**Files:**
- Reuse: `tests/test_generate_drawio_assets.py`
- Temporary output under: `tmp/`

**Step 1: Run unit tests**

Run: `python3 -m unittest tests.test_generate_drawio_assets -v`
Expected: PASS

**Step 2: Run CLI smoke test**

Run the bridge against a small manifest and verify:
- at least one PNG is created
- result manifest points at the generated PNG

**Step 3: Spot-check compatibility**

Confirm the output structure can feed the existing `build_image_map.py` / `generate_thesis_docx.py` flow without further code changes.
