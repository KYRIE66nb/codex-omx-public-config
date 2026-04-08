---
name: "bug-finder"
description: "Investigate, reproduce, and fix software bugs across frontend, backend, tests, and CI. Use when the user asks to debug errors, find root causes, triage regressions, explain failures, or verify bug fixes."
---

# Bug Finder Skill

Debug with evidence, not guesswork. Reproduce first, narrow scope fast, patch minimally, then verify.

## Workflow
1. Capture expected behavior, actual behavior, and environment details.
2. Reproduce locally; if needed, add a minimal failing test or script.
3. Isolate the failure path from entry point to breaking line.
4. Form one or two hypotheses and test each with targeted logs/assertions.
5. Implement the smallest safe fix that follows existing project patterns.
6. Verify with focused tests first, then broader checks as needed.
7. Add or update a regression test when possible.
8. Report symptom, root cause, fix, and validation evidence.

## Triage Priorities
- Prefer deterministic repro steps over manual one-off checks.
- Check recent commits, config changes, and dependency bumps early.
- For flaky failures, capture seed, timing, retries, and concurrency conditions.
- If a third-party service is involved, isolate with mocks/stubs before broad refactors.

## Output Format
- Symptom
- Root cause
- Code fix
- Validation performed
- Remaining risk and follow-up
