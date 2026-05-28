---
name: lunwen-figures
description: "Chinese thesis figures workflow."
---

# Lunwen Figures

## Overview

论文图示不是通用画图任务。先看章节语义、图题命名和最终交付物，再选工具。最终产物优先是可插入论文的本地 `PNG`、`SVG` 或 `.drawio`，不要把在线会话页面当交付物。

## Entry Gate

只有满足以下任一条件才进入本 skill：

- 用户明确要求生成、修改、替换图表或系统截图
- 模板、样文或正文里有必须补齐的图示/截图占位符
- 当前任务是 `full_delivery`，且交付范围包含图示或截图

如果当前任务只是套版、调目录、修编号、改摘要/参考文献格式，停止，不要打开 draw.io、浏览器截图或图示脚本。

## Figure Flow

1. 先确定所在章节、图题命名格式、最终产物类型
2. 每张图只选一个主路由；默认不要双开多个 MCP
3. 本地脚本或静态产物优先，交互式 draw.io 精修靠后
4. 截图只有在用户明确要求，或占位符必须替换时才抓取

## Default Routes

- `conceptual_er`：`Graphviz DOT -> PNG`
- `logical_er`：Mermaid `erDiagram` 或 draw.io 桥接 -> 本地图片
- `use_case`：Graphviz / PlantUML 风格描述 -> 本地图片；复杂排版再升到 `next_drawio_live`
- `flowchart` / `functional_structure`：Mermaid -> `drawio` 或本地图片
- `system_architecture`：Graphviz / draw.io XML -> 本地 `PNG` 或 `.drawio`

MCP 选择规则：

- `drawio`：Mermaid / XML / CSV 打开、lightbox 查看、轻量导出
- `next_drawio_live`：复杂布局、正交连线、图标库精修、必须交付可编辑 `.drawio`
- 如果本地脚本已经能满足，不进入 `next_drawio_live`

## Semantic Guardrails

- 用例图遵循 UML：参与者在系统边界外，用例为椭圆，系统边界为矩形
- 概念 E-R 图默认用 Chen 记法：实体矩形、属性椭圆、关系菱形；不要退化成全方框表关系图
- 系统功能结构图默认是自上而下层次拆解，不混流程箭头和实体属性
- 系统架构图先讲分层、模块边界和主数据流；正文没解释时不要滥用厂商图标

## Screenshot Rules

只有在当前交付范围包含真实系统截图时，才调用 Chrome MCP、Playwright 或等效浏览器工具。若只是格式任务，保留原截图或占位，不主动补抓。

## Checklist

- 图片宽度不超过模板版心
- 图片段落不沿用正文固定行距
- 图题、表题单倍行距
- 图号连续，图前说明和图后承接与样文一致
- Mermaid 渲染失败时回退真实图片或程序化绘图，不把失败文本留在正文
- 本地产物真实存在，可插入论文

## Resources

- 规划：`../lunwen/prompts/diagram_designer.md`
- 规范：`../lunwen/references/diagram-conventions.md`
- Mermaid：`../lunwen/tools/render_mermaid.py`
- Graphviz：`../lunwen/tools/render_graphviz.py`
- draw.io 资产桥接：`../lunwen/tools/generate_drawio_assets.py`
- 截图占位符：`../lunwen/tools/extract_screenshot_placeholders.py`
