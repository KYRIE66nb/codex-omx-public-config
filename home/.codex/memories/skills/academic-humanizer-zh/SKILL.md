---
name: academic-humanizer-zh
description: |
  Use when the user wants to lower AI rate or repetition in academic writing without changing the original meaning,
  stance, terminology, argument, or evidence boundaries. Best for papers, abstracts, coursework, reports, and thesis sections.
---

# Academic Humanizer ZH

用于论文、摘要、课程作业、实验报告、毕业设计等学术文本的“降 AI 率 / 降重复率”改写。

## 核心原则

1. 保留原意、原立场、原论证方向。
2. 不编造任何数据、作者、年份、文献、案例、结论或背景信息。
3. 保留术语、变量名、模型名、指标名、引文关系和结论边界。
4. 默认最小改写优先：先替换套话和重复表达，再做句式微调。
5. 语气保持审慎、克制、学术化，避免口语、营销腔和绝对化表述。

## 使用流程

1. 先阅读 `references/academic-low-ai-rewrite.md`。
2. 先冻结关键信息，再处理 AI 痕迹和重复表达。
3. 信息不足时，明确写“信息不足以判断”或“原文未说明”。
4. 输出可直接替换的改写版本；若有必要，再附 2-4 条简短修改说明。

## 明确禁止

- 不新增事实或证据。
- 不擅自补充常识背景。
- 不把“结果表明”强化成“充分证明”。
- 不为了降重替换关键术语。
- 不改动核心句序和论证骨架，除非用户明确允许大改。
