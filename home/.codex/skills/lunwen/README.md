<div align="center">

# 论文.skill

> “论文不是把字堆满，而是把项目事实、样文规范、图表截图和 Word 交付一次性闭环。”

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-F7C948)
![Codex](https://img.shields.io/badge/Codex-Skill-111111)
![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-6B7280)
![Chinese Thesis](https://img.shields.io/badge/Chinese-Thesis%20Workflow-0A7EFA)

面向本科计科学生推出的一键论文初稿 Skill。

不会写毕业论文初稿，开题报告和项目代码不知道怎么落成正文？
历届样文、学校模板、格式要求很多，但拼不出完整结构？
流程图、用例图、E-R 图、系统截图和测试内容总是缺一块？
最后要交 `.docx`，却还停留在零散材料和碎片化笔记里？

把零散材料快速整理成论文初稿的 Skill。
可以结合历届样文、开题报告、学校模板和真实项目内容生成初稿，
自动补充流程图、用例图、E-R 图等论文图表，并补齐项目截图与常见配图位，形成一套可继续精修的论文初稿工作流。

[安装](#安装) · [快速使用方式](#快速使用方式) · [使用流程](#推荐工作流) · [当前能力](#当前能力) · [常用脚本](#常用脚本) · [详细安装说明](./INSTALL.md) · [GitHub](https://github.com/Doryoku1223/lunwen-skill)

</div>

## 安装

### 方式 1：使用 Codex skill-installer 直接安装

```powershell
python "${HOME}\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py" --repo Doryoku1223/lunwen-skill --path . --name lunwen
```

### 方式 2：手动克隆到本地 skills 目录

```powershell
git clone https://github.com/Doryoku1223/lunwen-skill.git "${HOME}\.codex\skills\lunwen"
```

安装后重启 Codex，即可让它发现这个 skill。

如果你使用 Claude Code，也可以把仓库放到项目中直接复用其中的 `.claude/commands/` 和 `.claude/agents/` 兼容层，详细说明见 [INSTALL.md](./INSTALL.md)。

仓库同时补充了 `.trae/commands/` 与 `.trae/agents/` 兼容包装，方便在 Trae 这类只读取入口命令/代理定义的环境里尽量完整传递工作流。

## 快速使用方式

推荐优先在 Codex 中使用本 skill。

最简单的使用方法：

1. 把本项目 GitHub 链接复制给 Codex，让它帮你安装这个 skill。
2. 安装成功后，在 Codex 中打开你的项目文件夹。
3. 直接对 Codex 说：`为这个项目写一篇论文`
4. 然后按提示继续提供学校模板、历届样文、开题报告或任务书路径。

建议你在第一次使用时优先提供：

- 学校论文模板
- 历届样文
- 开题报告或任务书
- 项目源码目录

这样 Codex 才能按“先分析模板，再确认目录样式，最后生成 `.docx` 成稿”的正确流程工作。

## 论文优先路由（重要）

`lunwen` 不是普通作图 skill，而是论文场景的总协调器。只要用户同时提到论文/样文/模板/摘要/目录/参考文献/Word 成稿，以及 ER 图/用例图/架构图/流程图/系统截图，就应先由 `lunwen` 决定路由，再按需调用 `drawio`、`next_drawio_live`、Graphviz、Mermaid、`doc`、`pdf`、`playwright` 等能力。

默认优先级：

1. 论文章节、图题命名与版式约束
2. 图示语义与正文放置位置
3. 本地主产物：`PNG/SVG/.drawio/.docx`
4. 最后才是 MCP 会话或在线编辑

双 MCP 分工：

- `drawio`：基础打开/桥接，适合 Mermaid、XML、CSV、lightbox 导出
- `next_drawio_live`：实时精修，适合复杂布局、复杂连线、图标库和 `.drawio` 精修导出
- 如果基础路由已经足够，不默认进入 live 会话

## 推荐搭配 Skills

以下是这次实战迭代中证明有价值的搭配：

- `lunwen`
  论文主流程，负责模板优先分析、目录设计、正文写作、图表与成稿交付
- `docx`
  用于读取、分析和校验 `.docx` 模板与成稿，尤其适合处理样式、结构和文档对象
- `planning-with-files`
  用于长流程任务管理，适合论文这类多阶段任务，避免在模板分析、写作、成稿之间丢状态
- `systematic-debugging`
  当成稿出现目录重复、标题编号叠加、图片覆盖正文、附录样式错误等问题时，用它来定位根因，而不是盲改
- `verification-before-completion`
  在声称“论文已经生成好”之前，强制执行字数、引用、目录、图片和 `.docx` 存在性检查

如果论文工作流中还涉及以下任务，也建议按需搭配：

- `pdf`
  当学校只给 PDF 模板、PDF 样文或需要逐页视觉检查时使用
- `doc`
  当输入是 `.doc` 而不是 `.docx`，且需要先转换后再分析时使用
- `playwright`
  当需要抓真实系统截图替换论文占位图时使用

## 当前能力

- 样文目录与字数分析
- 样文 DOCX 样式提取与结构化样式配置
- 模板/样文样式提取
- 项目事实底稿抽取
- 按样文章节节奏控字写作
- 中文/英文参考文献比例控制
- 论文优先路由与双 MCP 图示决策
- draw.io / Mermaid / PlantUML / Graphviz 图表策略
- draw.io lightbox PNG 本地图资产桥接
- Chen 记法 E-R 图规范与系统型论文图示规则
- 内置 Playwright / Chrome CDP 浏览器自动截图策略
- doc / docx Word 成稿交付策略

## 推荐目录结构

```text
lunwen/
├── SKILL.md
├── README.md
├── INSTALL.md
├── agents/
│   └── openai.yaml
├── prompts/
├── references/
├── tools/
├── docs/
└── examples/
```

## 设计原则

1. 项目事实优先，不凭空补模块。
2. 样文章节体量优先，不默认写厚。
3. 学样文不只学内容，也学样式。
4. 图表、截图、参考文献和 Word 交付都要闭环。
5. 最终对用户展现过程与结果默认使用中文。

## 推荐工作流

建议按下面顺序使用本 skill：

1. 读取项目代码与文档，冻结项目事实底稿。
2. 分析样文或模板，提取章节体量和版式样式。
3. 生成目标章节字数表。
4. 分章写作并持续控字。
5. 构建参考文献池并检查中英文比例。
6. 处理 draw.io / Mermaid / PlantUML / Graphviz 图表。
7. 处理 Chen 记法 E-R 图、用例图和功能结构图，并优先落成可插入论文的本地 PNG。
8. 抓取真实系统截图替换占位。
9. 生成 `.docx`。
10. 做最终检查。

## 常用脚本

### 1. 统计论文各章字数

```bash
python tools/count_chapter_words.py thesis.md
```

### 2. 分析样文 PDF

```bash
python tools/analyze_sample_pdf.py sample.pdf
```

### 3. 检查参考文献池

```bash
python tools/build_reference_pool.py thesis.md
```

### 4. 分析样文 DOCX 并生成样式配置

```bash
python tools/analyze_docx_styles.py sample.docx output/style-profile.json
```

### 5. 提取截图占位并生成截图计划

```bash
python tools/extract_screenshot_placeholders.py thesis.md --json-out labels.json
python tools/build_image_map.py labels.json output/doc image-map.json
```

### 6. 提取 Mermaid 图块

```bash
python tools/extract_mermaid_blocks.py thesis.md tmp/mermaid --manifest tmp/mermaid/manifest.json
```

### 7. 渲染 Mermaid

```bash
python tools/render_mermaid.py tmp/mermaid/diagram-01.mmd tmp/mermaid/diagram-01.png
```

### 8. 生成 DOCX

```bash
python tools/generate_thesis_docx.py thesis.md thesis.docx --style-spec output/style-profile.json --image-map image-map.json
```

### 9. 渲染 Graphviz

```bash
python tools/render_graphviz.py tmp/graphviz/diagram.dot tmp/graphviz/diagram.png
```

### 10. 通过 draw.io 桥接生成本地 PNG

```bash
python tools/generate_drawio_assets.py tmp/diagram-manifest.json output/diagrams --result-manifest output/diagrams/result.json
```

### 11. 双 MCP 图示工作台（论文优先）

`lunwen` 现在采用“双 MCP + 本地资产”模式：

- `drawio`：第一阶段基础 MCP，适合直接打开 Mermaid / XML / CSV 内容，以及 lightbox 桥接导出
- `next_drawio_live`：第二阶段实时增强通道，适合 `start_session`、增量编辑、XML 修复和导出 `.drawio`
- 论文优先：默认主产物仍是本地 `PNG/SVG/.drawio`，而不是只停留在在线会话页面
- 默认先选一个主路由，不同时把同一张图丢给两个 MCP；只有基础路由不足时才升级到 `next_drawio_live`

统一图类型默认路由：

- `flowchart`：Mermaid -> draw.io bridge -> 本地 PNG
- `functional_structure`：Mermaid / 层次结构描述 -> draw.io bridge -> 本地 PNG
- `logical_er`：Mermaid `erDiagram` -> draw.io bridge -> 本地 PNG
- `conceptual_er`：Graphviz DOT -> 本地 PNG
- `use_case`：Graphviz / PlantUML 风格描述 -> 本地 PNG；复杂排版再进入 `next_drawio_live`
- `system_architecture`：Graphviz / draw.io XML -> 本地 PNG 或 `.drawio`；图标丰富或布局敏感时优先进入 `next_drawio_live`

最小 manifest 示例：

```json
{
  "diagrams": [
    {
      "id": "flow-01",
      "label": "图4-2 系统功能结构图",
      "title": "系统功能结构图",
      "type": "functional_structure",
      "content": "flowchart TD\nA[系统] --> B[管理员模块]\nA --> C[用户模块]"
    },
    {
      "id": "conceptual-er-01",
      "label": "图4-4 系统总体E-R图",
      "title": "系统总体E-R图",
      "type": "conceptual_er",
      "content": "graph ER { 用户 [shape=box]; 订单 [shape=box]; 下单 [shape=diamond]; 用户 -- 下单 [label=\"1\"]; 下单 -- 订单 [label=\"N\"]; }"
    }
  ]
}
```

`generate_drawio_assets.py` 的默认路由规则：

- 流程图、系统功能结构图、逻辑表关系图：优先走 draw.io lightbox PNG 桥接
- 用例图、系统架构图：默认先走本地图片产物路径，需要人工精修时再进入 `next_drawio_live`
- 概念 E-R 图：默认继续走 Graphviz DOT -> PNG，避免 Chen 记法退化
- 输出结果可直接接回 `image-map.json` / `.docx` 成稿链路

关于概念 E-R 图的固定原则：

- 只要用户要的是概念结构设计或系统总体 E-R 图，默认仍以 Chen / Graphviz 为主
- `next_drawio_live` 只作为辅助精修或可编辑 draw.io 源产物，不替代概念语义约束
- 论文正文主产物优先是本地图片或 `.drawio` 文件，而不是纯编辑链接

和现有图片映射链路配合时，可以直接把 `result.json` 作为手工映射输入：

```bash
python tools/build_image_map.py labels.json output/diagrams image-map.json --manual output/diagrams/result.json
```

## 当前限制

- 如果环境没有 LibreOffice / Poppler，无法做逐页渲染检查。
- 如果环境没有 Mermaid 渲染能力，流程图可能只能保留源码或占位。
- 如果环境没有 Graphviz 或 draw.io / Chrome / Playwright 能力，图资产桥接只能先保留源码，再补渲染。
- 如果环境没有可用浏览器会话，`next_drawio_live` 只能作为配置存在，无法完成实时预览和交互式精修。
- 浏览器截图与真实系统抓图能力依赖额外环境支持。

## 兼容性

- Codex：原生适配。
- Claude Code：已补 `.claude/commands/` 与 `.claude/agents/` 兼容层。
