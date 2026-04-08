---
name: claude-supervisor-codex-worker
description: Use when the user wants Claude to act as supervisor/brain and drive Codex implementation, especially phrases like "claude当监工", "claude指挥codex", or "监工大脑".
---

# Claude Supervisor Codex Worker

## Overview

Run a strict 3-stage loop where Claude plans and reviews while Codex executes. Prefer the command `claude-codex-supervisor "<task>"` so the workflow is reproducible.

## Trigger Phrases

- `claude当监工`
- `claude监工`
- `监工大脑`
- `claude指挥codex`
- `claude操控codex`
- `claude-supervisor-codex`
- `监工执行模式`

## Workflow

1. Normalize the user request into one executable task sentence.
2. Run `claude-codex-supervisor "<task>"`.
3. Use Claude output as architecture and acceptance gate.
4. Use Codex output as implementation delta.
5. Use Claude final review as pass/fail decision.

## Output Contract

Return one merged report with these sections:

1. `Architecture`
2. `Implementation`
3. `Verification`
4. `How to rerun`

## Failure Handling

- If Claude plan step fails: return the failure and retry with a shorter task sentence.
- If Codex execution step fails: keep artifacts, summarize blocker, and request targeted retry.
- If Claude review fails: return explicit fix list with severity (`P0`, `P1`, `P2`).
