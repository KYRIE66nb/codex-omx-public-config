---
name: next-ai-draw-io
keyword: next-drawio
description: "Generate and edit draw.io diagrams."
tags:
- draw.io
- diagram
- nextjs
- mcp
- visualization
platforms:
- Codex
- Claude
- Cursor
- VS Code
source: DayuanJiang/next-ai-draw-io
---

# Next AI Draw.io

Use this skill for the `next-ai-draw-io` repo when you need AI-assisted diagram creation, draw.io XML editing, or MCP integration.

## When to use

- Create or edit diagrams from natural language
- Run the web app locally
- Integrate the MCP server with Claude, Cursor, or VS Code
- Work on diagram history, provider setup, or deployment

## Quick Start

```bash
git clone https://github.com/DayuanJiang/next-ai-draw-io.git
cd next-ai-draw-io
npm install
cp env.example .env.local
npm run dev
```

Open `http://localhost:6002`.

## MCP

```bash
claude mcp add drawio -- npx @next-ai-drawio/mcp-server@latest
```

JSON config form:

```json
{
  "mcpServers": {
    "drawio": {
      "command": "npx",
      "args": ["@next-ai-drawio/mcp-server@latest"]
    }
  }
}
```

## What it does

- Natural-language diagram creation and edits
- Image-based diagram replication
- PDF and text upload for diagram generation
- Diagram history and restore
- Multi-provider support
- Cloud architecture diagrams and animated connectors

## Notes

- Use a strong model when generating or editing draw.io XML.
- If the task is only to render or lightly edit diagrams, prefer the existing draw.io path before the live MCP path.
- Keep the final artifact local when possible: `.drawio`, PNG, or SVG.
