---
name: er-json-dot-workflow
description: "Use when users ask to extract an ER model from thesis text, requirements, SQL DDL, reports, or ORM/code models with a strict two-phase protocol: Stage 1 JSON extraction first, then Stage 2 Graphviz DOT only after explicit confirmation."
---

# ER JSON to DOT Workflow

## Overview

Enforce a hard two-stage ER workflow for database modeling tasks. Always extract schema as strict JSON first, then generate Graphviz DOT only after explicit user confirmation.

## Workflow Contract

1. Determine current stage from user intent:
- Enter Stage 1 when user provides source materials or asks to extract ER structure.
- Enter Stage 2 only when user explicitly confirms Stage 1 output (examples: `确认`, `按这个来`, `继续画图`, `JSON没问题`, `已修改如下`).
2. Never skip Stage 1.
3. If user asks for both stages in one message, still output Stage 1 JSON only and wait for confirmation.
4. If user gives revision feedback on Stage 1 JSON, output revised Stage 1 JSON only.

## Hard Rules

- Stage 1 output must be JSON only. No explanation, no markdown fences, no DOT, no extra text.
- Stage 2 output must be Graphviz DOT only. No JSON, no explanation.
- Do not output Mermaid, ASCII diagrams, screenshots, image links, or base64 image data.
- Preserve strict relevance to provided materials; do not invent unrelated business entities.

## Stage 1: Extract and Package (JSON only)

Use the contract in [stage1-json-contract.md](references/stage1-json-contract.md).

Extraction guidance:
- SQL inputs: trust `CREATE TABLE`, `PRIMARY KEY`, `FOREIGN KEY`, `REFERENCES`, `UNIQUE`.
- ORM/code inputs: map models/classes/annotations and declared associations.
- Thesis/requirements inputs: map core nouns to entities, field descriptions to attributes, action verbs to relationships.
- Many-to-many detection: junction table primarily composed of two foreign keys indicates `many_to_many`; junction extra columns become `relationship_attributes`.
- Unknown cardinality: set `cardinality: null` and add a confirmation question.
- Keep `source_name` as original token from source while using clean logical `name`.

Stage 1 output shape must match the exact JSON object schema in the reference file.

## Stage 2: Draw Diagram (DOT only after confirmation)

Use the style contract in [stage2-dot-contract.md](references/stage2-dot-contract.md).

Render rules:
- Output exactly one fenced `dot` code block and nothing else.
- Use `rankdir=LR` and increased spacing (`nodesep`, `ranksep`) to avoid clutter.
- Node shapes:
  - Entities: `shape=box`
  - Attributes: `shape=ellipse`
  - Relationships: `shape=diamond`
- Edge styles:
  - Entity to relationship: solid
  - Attribute to entity/relationship: dashed
- Node IDs must be ASCII-only:
  - Entities: `E_xxx`
  - Attributes: `A_xxx`
  - Relationships: `R_xxx`
- Labels may be Chinese.
- Prefix PK attributes with `PK:` in label (optionally add `UQ:` when appropriate).

## Output Safety Checks

Before sending Stage 1:
- Ensure response is pure JSON object with required top-level keys.
- Ensure no markdown fence and no explanatory lines.

Before sending Stage 2:
- Ensure user confirmation is explicit.
- Ensure response contains only one `dot` code fence.
- Ensure no JSON or prose appears outside the dot block.

## References

- [Stage 1 JSON Contract](references/stage1-json-contract.md)
- [Stage 2 DOT Contract](references/stage2-dot-contract.md)
