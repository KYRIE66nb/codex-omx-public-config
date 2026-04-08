---
name: using-superpowers
description: Use when starting any conversation - establishes how to find and use skills, requiring Skill tool invocation before ANY response including clarifying questions
---

# Using Skills

## The Rule

Invoke relevant or requested skills before any response or action, including clarifying questions. If there is even a 1% chance a skill applies, invoke it first. If the skill turns out not to apply, you can stop using it after checking.

In environments with a Skill tool, use that tool instead of reading skill files manually.

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
- If the skill has a checklist, create a todo for each item
- Follow the skill exactly unless it explicitly says it is flexible

Rigid skills such as TDD or debugging must be followed literally. Pattern skills can be adapted, but only after they have been invoked.

## User Instructions

Instructions say WHAT, not HOW. "Add X" or "Fix Y" doesn't mean skip workflows.
