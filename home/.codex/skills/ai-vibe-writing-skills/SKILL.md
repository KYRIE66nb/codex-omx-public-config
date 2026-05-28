---
name: ai-vibe-writing-skills
description: "Ai vibe writing skills workflow."
---

# AI Vibe Writing Skills

Use this skill for personalized writing and editing with persistent style constraints.

## Resources
- Core prompts: `references/ai_context/prompts/`
- Style profile template: `references/ai_context/style_profile.md`
- Error log template: `references/ai_context/error_log.md`
- Long-term memory templates: `references/ai_context/memory/hard_memory.json`, `references/ai_context/memory/soft_memory.json`
- Custom writing context: `references/ai_context/custom_specs.md`

## Workflow
1. For style extraction tasks, follow `references/ai_context/prompts/1_style_extractor.md` and output content that can directly update a style profile.
2. For normal drafting tasks, follow `references/ai_context/prompts/2_writer.md` to align with style profile, error constraints, and recalled memory.
3. For correction feedback loops, follow `references/ai_context/prompts/3_error_logger.md` to convert feedback into reusable constraints.
4. For proofreading tasks, follow `references/ai_context/prompts/4_grammar_checker.md` and report precise local fixes.
5. For stable preferences and domain facts, follow `references/ai_context/prompts/5_long_term_memory.md` and separate hard memory from soft memory.

## Output Expectations
- Keep the user's original intent unchanged.
- Preserve target tone unless user requests a style shift.
- Avoid banned wording from the error log when available.
- Separate diagnosis from rewritten text when proofreading.
- Mark missing facts as `【TODO】` instead of guessing.

## Safety
- Do not fabricate references, data, or factual claims.
- Do not expose private memory content unless relevant to the current writing task.
