# Lunwen Diagram Workbench Design

**Date:** 2026-04-06

## Goal

把 `next-ai-draw-io` 的会话式 draw.io 能力，与当前已经存在的 `@drawio/mcp` 和 `lunwen` 的 PNG 桥接链路融合起来，形成一个更适合论文场景的统一图示工作台。

本次设计以“论文优先”为默认原则：

- 默认主产物是本地可插入论文的图片或源文件
- 交互式会话作为增强通道，而不是唯一通道
- 概念 E-R 图继续保持 Chen / Graphviz 优先，不被 draw.io 表框图替代

## Confirmed Decisions

1. 保留当前全局 `drawio` MCP，不替换。
2. 新增一个 `next-ai-drawio` 风格的 live MCP 别名，用于实时会话、增量编辑、导出。
3. `lunwen` 内引入统一图类型路由，而不是只靠零散 prompt 约定。
4. 默认双轨产物：
   - 论文插图优先的本地 `PNG/SVG/.drawio`
   - 需要精修时再进入 live draw.io 会话

## Target Diagram Types

- `flowchart`
- `functional_structure`
- `logical_er`
- `conceptual_er`
- `use_case`
- `system_architecture`

## Engine Strategy

### Paper-first default path

- `flowchart` -> Mermaid -> draw.io bridge -> PNG
- `functional_structure` -> Mermaid / structured graph -> draw.io bridge -> PNG
- `logical_er` -> Mermaid `erDiagram` -> draw.io bridge -> PNG
- `conceptual_er` -> Graphviz DOT -> PNG
- `use_case` -> Graphviz DOT by default; live draw.io as optional refinement path
- `system_architecture` -> Graphviz DOT or draw.io XML; live draw.io preferred when icon-rich or layout-sensitive

### Live enhancement path

新增 `next_drawio_live` MCP 通道，专门负责：

- `start_session`
- `create_new_diagram`
- `edit_diagram`
- `get_diagram`
- `export_diagram`

其定位不是替换现有脚本，而是补强以下场景：

- 用户用例图的边界、参与者和椭圆布局微调
- 系统架构图的层次与连接线整理
- 复杂流程图和功能结构图的可视化精修
- draw.io XML 的校验、自动修复和增量编辑

## Required Changes

### 1. Global MCP config

在 [`/Users/zhishixuebao/.codex/config.toml`](/Users/zhishixuebao/.codex/config.toml) 中新增 live MCP 别名，保留现有 `drawio` 配置不动。

### 2. Lunwen tooling

增强 [`generate_drawio_assets.py`](/Users/zhishixuebao/.codex/skills/lunwen/tools/generate_drawio_assets.py)：

- 新增 `use_case`、`system_architecture` 图类型
- 将“图类型”和“源格式”分开
- 为 draw.io 路径显式支持多种 source format
- 保持现有 Graphviz 路径兼容

### 3. Lunwen prompts and references

更新 `SKILL.md`、`README.md`、`prompts/diagram_designer.md`、`references/diagram-conventions.md`，把“什么时候用现有 drawio / next live / Graphviz”写清楚。

## Out of Scope

- 不改 `generate_thesis_docx.py` 主体链路
- 不把 `next-ai-draw-io` 的整套 Next.js UI 嵌进 `lunwen`
- 不把概念 E-R 图默认切到 draw.io 表关系图
- 不提交 git commit

## Acceptance

1. 全局配置里同时存在 `drawio` 与 `next_drawio_live`
2. `lunwen` 文档中明确给出统一图类型路由
3. `generate_drawio_assets.py` 能识别新增图类型并维持旧行为兼容
4. 测试覆盖新增类型与路由
5. 最终验证包含 fresh test evidence
