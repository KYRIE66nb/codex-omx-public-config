# Lunwen Diagram Workbench Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a paper-first diagram workbench to `lunwen` by combining the existing draw.io bridge, a new `next_drawio_live` MCP channel, and explicit routing for ER, architecture, use-case, and flow diagrams.

**Architecture:** Keep the current `drawio` MCP and PNG bridge intact, layer in a separate live MCP alias for interactive draw.io sessions, and extend `lunwen`'s manifest-driven tooling plus prompt docs so each diagram type has an explicit default path.

**Tech Stack:** TOML config, Python 3, `unittest`, Pillow, Graphviz, Playwright, draw.io MCP, `@next-ai-drawio/mcp-server`

---

### Task 1: Add the live draw.io MCP alias

**Files:**
- Modify: `/Users/zhishixuebao/.codex/config.toml`

**Step 1: Add the failing expectation**

Expectation:
- Existing `drawio` server stays untouched
- New `next_drawio_live` server points to `npx -y @next-ai-drawio/mcp-server@latest`

**Step 2: Apply minimal config change**

Add a new `[mcp_servers.next_drawio_live]` block only.

**Step 3: Verify config shape**

Run:
```bash
rg -n "mcp_servers.drawio|mcp_servers.next_drawio_live|@next-ai-drawio/mcp-server|@drawio/mcp" /Users/zhishixuebao/.codex/config.toml
```

Expected:
- Both MCP blocks present
- Existing `@drawio/mcp` still present
- New `@next-ai-drawio/mcp-server` present

### Task 2: Extend lunwen diagram routing and tests

**Files:**
- Modify: `/Users/zhishixuebao/.codex/skills/lunwen/tools/generate_drawio_assets.py`
- Modify: `/Users/zhishixuebao/.codex/skills/lunwen/tests/test_generate_drawio_assets.py`
- Modify: `/Users/zhishixuebao/.codex/skills/lunwen/tests/fixtures/drawio-assets/manifest.json`

**Step 1: Write failing tests for new routing**

Add expectations for:
- `use_case`
- `system_architecture`
- explicit source-format normalization where relevant
- compatibility of existing types

**Step 2: Run tests to verify failure**

Run:
```bash
cd /Users/zhishixuebao/.codex/skills/lunwen && python3 -m unittest tests.test_generate_drawio_assets -v
```

Expected:
- FAIL on unsupported types or missing metadata

**Step 3: Write minimal implementation**

Extend routing logic so:
- current behavior remains compatible
- new types are recognized
- draw.io-vs-graphviz path is explicit and documented in code

**Step 4: Run tests to verify pass**

Run:
```bash
cd /Users/zhishixuebao/.codex/skills/lunwen && python3 -m unittest tests.test_generate_drawio_assets -v
```

Expected:
- PASS

### Task 3: Update lunwen skill docs and prompts

**Files:**
- Modify: `/Users/zhishixuebao/.codex/skills/lunwen/SKILL.md`
- Modify: `/Users/zhishixuebao/.codex/skills/lunwen/README.md`
- Modify: `/Users/zhishixuebao/.codex/skills/lunwen/prompts/diagram_designer.md`
- Modify: `/Users/zhishixuebao/.codex/skills/lunwen/references/diagram-conventions.md`

**Step 1: Document the dual-MCP model**

Clarify:
- `drawio` stays as the basic XML/Mermaid path
- `next_drawio_live` is the interactive session path

**Step 2: Document diagram routing**

Make routing explicit for:
- flowchart
- functional structure
- logical ER
- conceptual ER
- use case
- system architecture

**Step 3: Add usage examples**

Document:
- when to use local PNG-first path
- when to use live draw.io path
- how live draw.io output reconnects to local `.drawio` or PNG assets

### Task 4: Verify end-to-end

**Files:**
- Reuse modified files above

**Step 1: Run unit tests**

Run:
```bash
cd /Users/zhishixuebao/.codex/skills/lunwen && python3 -m unittest tests.test_generate_drawio_assets -v
```

Expected:
- PASS

**Step 2: Run lightweight syntax verification**

Run:
```bash
python3 -m py_compile /Users/zhishixuebao/.codex/skills/lunwen/tools/generate_drawio_assets.py
```

Expected:
- exit 0

**Step 3: Run config verification**

Run:
```bash
rg -n "mcp_servers.drawio|mcp_servers.next_drawio_live|@next-ai-drawio/mcp-server|@drawio/mcp" /Users/zhishixuebao/.codex/config.toml
```

Expected:
- both MCP entries visible

**Step 4: Summarize residual risks**

Call out:
- live MCP behavior depends on browser session availability
- concept ER still intentionally stays Graphviz-first
- icon-rich architecture diagrams may still need live refinement for best results
