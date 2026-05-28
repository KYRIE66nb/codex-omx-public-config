---
name: lunwen-format-docx
description: "Format Chinese thesis DOCX."
---

# Lunwen Format Docx

## Overview

这个 skill 只处理论文模板套版和 `.docx` 成稿，不负责图表生成和正文扩写。核心原则是模板优先：优先保留模板已有的封面、目录、分页、样式和特殊标题机制，再把内容灌进去。

## Entry Gate

以下场景进入本 skill：

- `format_only`
- 任意任务明确要求输出 `.docx` 成稿
- 用户要求修目录、修标题编号、修页眉页脚、修摘要/关键词/参考文献格式
- 输入源是 `.doc`，需要转成 `.docx`

## Formatting Flow

1. 输入若为 `.doc`，先用 `tools/convert_word_to_docx.py` 转换
2. 识别模板中的前置部分、正文部分、后置部分、附录部分
3. 优先保留模板封面、目录、分页、原生样式和特殊标题
4. 再灌入正文、表格、摘要、参考文献等内容
5. 模板没有定义的样式，才退回默认规则

## Non-Body Title Guardrails

以下标题默认不得误套正文章编号样式：

- `中文摘要`
- `ABSTRACT`
- `目　　录`
- `参考文献`
- `致　　谢`
- `声　　明`
- `在学期间参加课题的研究成果`
- 附录标题

如果模板标题样式自带编号，正文源稿里的 `第1章`、`1.1`、`1.1.1` 等文本编号必须先剥离，避免出现 `第1章第1章` 或 `1.11.1` 叠加。

## TOC and Table Rules

- 模板已有目录时，优先复用或替换原目录位置，不额外再插一个目录块
- 表格优先克隆模板或样文中的现成三线表，再回填内容
- 只有没有可复用三线表时，才退回程序生成的标准三线表

## Fallback Defaults

只有模板和样文都无法提供时，才用兜底规则：

- 摘要、Abstract、参考文献、致谢标题居中
- 摘要与 Abstract 独立分页
- 一级章节分页开始
- 中文正文宋体，英文正文 Times New Roman
- 中文关键词独立成段，`关键词：` 标签黑体小四加粗
- 中英文摘要正文除关键词行外默认首行缩进 2 字符
- 参考文献悬挂缩进

## Checklist

- `.docx` 文件真实存在
- 模板封面、目录、分页保留正确
- 只保留一个目录，且可刷新
- 摘要、Abstract、目录不显示为 `第N章`
- `参考文献`、`致　　谢`、`声　　明`、附录不误用正文编号样式
- 特殊标题字间空格和模板原生格式未被脚本覆盖
- 若输入源是 `.doc`，已成功转换为 `.docx`

## Resources

- 格式化：`../lunwen/prompts/docx_formatter.md`
- 默认版式：`../lunwen/references/default-style.md`
- 分析模板/样文：`../lunwen/tools/analyze_docx_styles.py`
- 转换：`../lunwen/tools/convert_word_to_docx.py`
- 生成成稿：`../lunwen/tools/generate_thesis_docx.py`
