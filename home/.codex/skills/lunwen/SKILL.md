---
name: lunwen
description: Use when the task concerns a Chinese graduation thesis, course-design paper, technical report, or thesis-style `.docx` deliverable with template alignment, sample analysis, chapter drafting, abstract/references, or thesis-specific Word formatting requirements.
---

# Lunwen

## Overview

`lunwen` 是中文论文任务的轻量总路由器。主 skill 只负责做任务分流、锁定模板和样文优先级、冻结项目事实、控制章节体量，以及决定何时按需加载重型子技能。不要把图表、截图、draw.io 或整套 `.docx` 成稿规则默认塞进每一次论文请求。

## Routing Contract

先把请求分成四类：

1. `format_only`：模板套版、目录/编号/样式修复、摘要/关键词/参考文献格式、`.doc -> .docx`、把已有内容灌入模板
2. `text_only`：写/补/压缩/改写正文、摘要、目录说明、答辩稿，不落地图表
3. `figure_or_screenshot`：ER 图、用例图、架构图、流程图、系统截图、图示/截图占位符补齐
4. `full_delivery`：从模板、样文和项目事实完成正文、图表、参考文献与 `.docx` 成稿

路由规则：

- 只要是论文任务，先进入 `lunwen`
- `format_only`：
  `REQUIRED SUB-SKILL:` `lunwen-format-docx`
  默认跳过项目事实提取、图表闭环和参考文献池
- `text_only`：留在主 skill，只有用户追加图表或 `.docx` 成稿要求时才进入子技能
- `figure_or_screenshot`：
  `REQUIRED SUB-SKILL:` `lunwen-figures`
  如果最终交付还要 `.docx`，最后再调用 `lunwen-format-docx`
- `full_delivery`：先走主 skill 的写作主线，到视觉资产阶段调用 `lunwen-figures`，到成稿阶段调用 `lunwen-format-docx`

如果用户原话里出现 `按模板改格式`、`套版`、`只调目录`、`只修标题编号`、`只改摘要/参考文献格式`、`把现有内容灌进模板`，默认判为 `format_only`。

## Core Flow

### 1. 锁定输入

默认优先级：模板 > 样文 > 用户口头要求 > 默认规则。首次响应优先索取模板、样文、开题报告、任务书等本地路径。若输入是 `.doc`，必须先用 `tools/convert_word_to_docx.py` 转成 `.docx`，再分析样式。

### 2. 冻结项目事实

先读项目代码和文档，提炼固定事实底稿。后续各章只能基于这份事实扩写，不允许凭经验补剧情。

### 3. 学模板和样文

进入模板优先模式，至少确认：结构、标题层级、编号机制、目录策略、非正文编号标题、图表和表格命名、章节节奏。模板负责最终样式，样文只补章节节奏和语言风格。

### 3.5 先回传设计

在正文写作前，必须先把以下内容回传给用户确认：

- 当前建议目录
- 各章目标字数
- 版式摘要
- 与默认规则的冲突项
- 目录保留/替换策略
- 标题编号由模板样式还是正文文本负责

未确认前，不开写正文。

### 4. 先定字数，再写作

默认贴近样文体量，不主动写厚。每写完一章就复查字数，超出就压缩，明显不足再补充项目事实、设计细节和测试分析。

### 5. 参考文献按需进入

只有在引用和参考文献进入交付范围时才建池。默认约束：2020 年及以后，中文 10-12 篇，英文 3-5 篇，总数约 15 篇；不真实、不可核验的文献直接丢弃。

### 6. 路由化验收

只验证当前任务范围：

- `format_only`：模板保留、目录、编号、样式、分页、`.docx` 是否存在
- `text_only`：章节完整性、字数目标、逻辑链、语言风格
- `figure_or_screenshot`：使用 `lunwen-figures` 的检查清单
- 凡是输出 `.docx`：额外使用 `lunwen-format-docx` 的检查清单

## Minimal Resource Map

- 输入与冲突：`prompts/intake.md`、`prompts/style_extractor.md`
- 项目事实：`prompts/fact_extractor.md`
- 写作与控字：`prompts/chapter_writer.md`、`prompts/language_style.md`、`tools/count_chapter_words.py`
- 参考文献：`prompts/reference_selector.md`、`tools/build_reference_pool.py`
- 模板/样文分析：`tools/analyze_docx_styles.py`、`tools/analyze_sample_pdf.py`
- 图示与截图：`lunwen-figures`
- `.docx` 成稿：`lunwen-format-docx`
