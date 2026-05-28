---
name: using-superpowers
description: "Use skills correctly."
---

# Using Skills

## The Rule

Invoke relevant or requested skills before any response or action, including clarifying questions. If there is even a 1% chance a skill applies, invoke it first. If the skill turns out not to apply, you can stop using it after checking.

In environments with a Skill tool, use that tool instead of reading skill files manually.

## Legacy Quality Mode

Prioritize content quality over context minimization.

When a skill applies:

1. Load the full primary `SKILL.md`, not just its name or short description.
2. If the skill is an alias/router, immediately load the downstream primary skill(s) it points to.
3. If the skill references task guides, examples, scripts, templates, or troubleshooting notes that are relevant to the request, read those before acting.
4. Do not skip QA gates, visual verification, command sequencing rules, edge-case notes, or tool-specific caveats to save context.
5. Use progressive disclosure only to avoid clearly irrelevant files, not to avoid necessary operational instructions.

If context budget and quality conflict, choose quality and rely on later compaction rather than under-loading the skill.

## Red Flags

Stop and check skills if you catch yourself thinking:

- "This is simple, I can skip the skill check"
- "I need more context first"
- "I'll explore files first"
- "I remember the skill already"
- "This one action doesn't count"
- "The skill is overkill"

## Skill Priority

When multiple skills could apply, use this order:

1. **Process skills first** (brainstorming, debugging) - these determine HOW to approach the task
2. **Implementation skills second** (frontend-design, mcp-builder) - these guide execution

"Let's build X" means brainstorming first, then implementation skills.
"Fix this bug" means debugging first, then domain-specific skills.

## Execution

After invoking a skill:

- Announce which skill you are using and why
- Load enough related skill material to execute at full quality, especially for Office documents, spreadsheets, data analysis, coding, debugging, frontend work, and reviews
- If the skill has a checklist, create a todo for each item
- Follow the skill exactly unless it explicitly says it is flexible

Rigid skills such as TDD or debugging must be followed literally. Pattern skills can be adapted, but only after they have been invoked.

## User Instructions

Instructions say WHAT, not HOW. "Add X" or "Fix Y" doesn't mean skip workflows.
