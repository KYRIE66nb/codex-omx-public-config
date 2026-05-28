---
name: student-cs
description: "CS student local workflow."
---

# Student CS Skill

Use the local pack through deterministic CLI commands. Keep everything local and file-based.

## Workflow
1. Work from the target repo root.
2. Ensure required paths exist: `bin/`, `skills/student-cs/templates/`, `skills/student-cs/scripts/`, `memory/`, `out/student-cs/`.
3. For template generation, run `./bin/student-cs <template-command>`.
4. For memory updates, run `./bin/student-cs memory-index` before query when needed.
5. For natural-language entry, run `./bin/student-cs-nl "<instruction>"`.
6. Return created/updated file paths and key command output.

## Commands
- `./bin/student-cs offer`
- `./bin/student-cs daily-content`
- `./bin/student-cs study-blocks`
- `./bin/student-cs weekly-review`
- `./bin/student-cs bug-report`
- `./bin/student-cs design-doc`
- `./bin/student-cs paper-checklist`
- `./bin/student-cs memory-index`
- `./bin/student-cs memory-query "<query>"`
- `./bin/student-cs-nl "<instruction>"`

## Safety
- Keep operations local only.
- Do not read secrets or config outside repo scope.
- Do not call external services for routing/index/query.

## Validation
- Confirm `./bin/student-cs --help` and `./bin/student-cs-nl --help` work.
- Run at least one template command and one memory command for smoke tests.
