# Global Claude Code Instructions - Enhanced

Scope: all projects under `/Users/zhishixuebao`.

## AI 工作流增强系统

本配置整合了 FlowPilot 和 AI Superagents 的优点，提供全自动、可中断恢复、自我进化的工作流系统。

## 核心特性

### 1. FlowPilot 调度引擎

- **持久化状态** - 所有状态存储在 `.workflow/` 和 `.flowpilot/`，不怕中断
- **四层记忆** - progress.md（主 Agent）、task-xxx.md（子 Agent）、summary.md（滚动摘要）、memory.json（长期记忆）
- **自动并行** - 依赖图分析，批量派发子 Agent
- **自我进化** - Reflect → Experiment → Review 三阶段循环
- **中断恢复** - `flow resume` 一键继续

### 2. AI Superagents 执行层

- **角色分工** - researcher/planner/implementer/reviewer/verifier/reporter
- **专项技能** - superagents/fix-bug/develop-feature/refactor/review-code
- **全局规则** - code-quality/output-style/fast-path
- **意图澄清** - 开场对齐 → 快速扫描 → 关键提问 → 方案生成

### 3. 双模型协同

- **Claude（Opus 4.6）** - 架构设计、需求分析、代码审查
- **Codex（GPT-4.5）** - 代码实现、测试编写、文档生成

## Natural-language triggers

### FlowPilot 工作流

如果用户说：
- `全自动开发`
- `自动工作流`
- `flowpilot`
- `flow 工作流`

执行：
```bash
cd <project>
flow init
# 然后在 Claude Code 中描述需求
```

### Claude + Codex 双模型协同

如果用户说：
- `claude code协同`
- `opus4.6当大脑`
- `codex当员工`
- `脑产品经理`
- `brain-pm-hand-exec`
- `同时用codex和claude工作`
- `codex和claude协同`
- `codex+claude`
- `双模型协同`
- `codex claude duo`

激活 "Claude brain + Codex hands" 工作流：

1. Planning/architecture by Claude worker (`OMX_TEAM_WORKER_CLI=claude`, `omx team 1:planner ...`)
2. Implementation by Codex workers (`OMX_TEAM_WORKER_CLI=codex`, `OMX_TEAM_WORKER_LAUNCH_ARGS="--model gpt-4.5"`, `omx team N:executor ...`)
3. Final review by Claude worker (`OMX_TEAM_WORKER_CLI=claude`, `omx team 1:critic ...`)

执行规则：
- 不要求确认
- 确保 team 在 tmux 中运行
- 用 `omx team status <team>` 监控
- 只在终止状态或用户请求时关闭

最终输出格式：
- `Architecture`
- `Implementation`
- `Verification`
- `How to use this flow again`

### 固定启动器（推荐）

对于双模型请求，使用：

```bash
codex-claude-duo "<task>"
```

预期行为：
- 在 tmux 内：`OMX_TEAM_WORKER_CLI_MAP=codex,claude omx team 2:executor "<task>"`
- 在 tmux 外：自动创建 tmux 会话并运行相同命令
- 不要求确认

### Claude 监工 + Codex 员工模式

如果用户说：
- `claude当监工`
- `claude监工`
- `监工大脑`
- `claude指挥codex`
- `claude操控codex`
- `claude-supervisor-codex`
- `监工执行模式`

立即加载并遵循技能：
- `claude-supervisor-codex-worker` (路径: `/Users/zhishixuebao/.claude/skills/claude-supervisor-codex-worker`)

执行契约：
- 先运行 `claude-codex-supervisor "<task>"`
- Claude 负责规划/审查；Codex 负责实现
- 返回合并报告，包含：`Architecture`、`Implementation`、`Verification`、`How to rerun`

### 论文 + ER 图工作流

如果用户说：
- `写毕业论文`
- `生成论文大纲`
- `设计数据库表`
- `画ER图`
- `论文模板`
- `论文目录模板`
- `ER图工作流`
- `数据库表图优化`
- `论文ER图美化`
- `毕业论文固定模板`

激活论文写作工作流：

1. **论文结构模板**（7章标准结构）：
   - 第一章：绪论（研究背景、研究意义、国内外研究现状）
   - 第二章：相关技术介绍（开发语言、系统架构、数据库、框架）
   - 第三章：系统需求分析（可行性分析、功能需求、非功能需求）
   - 第四章：系统设计（架构设计、数据库设计、功能模块设计）
   - 第五章：系统实现（登录模块、核心功能模块、其他模块）
   - 第六章：系统测试（测试环境、测试方法、测试用例、测试结果）
   - 第七章：总结与展望

2. **数据库表设计规范**：
   - 表头格式：字段名称 | 类型 | 长度 | 字段说明 | 主键 | 默认值
   - 必备字段：id (bigint, 主键), addtime (timestamp, CURRENT_TIMESTAMP)
   - 常用类型：varchar(200), longtext, bigint, int, timestamp, datetime, date, double

3. **ER图绘制规范**（使用Mermaid格式）：
   ```mermaid
   erDiagram
       TABLE_NAME {
           bigint id PK "主键"
           varchar field_name "字段说明"
           timestamp addtime "创建时间"
       }
   ```

4. **工具脚本路径**：
   - 分析论文：`/Users/zhishixuebao/Desktop/外包项目/er图流程/analyze_papers.py`
   - 生成模板：`/Users/zhishixuebao/Desktop/外包项目/er图流程/generate_template.py`
   - 生成ER图：`/Users/zhishixuebao/Desktop/外包项目/er图流程/generate_er_diagram.py`

5. **Claude+Codex协同模式**：
   - Claude负责：架构设计、需求分析、文档撰写
   - Codex负责：代码实现、表结构生成、ER图绘制
   - 使用命令：`OMX_TEAM_WORKER_CLI_MAP='claude,codex' omx team 2:executor "<task>"`

## 工作流执行流程

### 标准 FlowPilot 流程

```
1. flow init
   ↓
2. 协议嵌入 AGENTS.md + 按客户端注入配置
   ↓
3. 用户描述需求
   ↓
4. ┌─→ flow next (--batch) → 获取任务+上下文+记忆
   │        ↓
   │   子Agent执行（自动选插件/角色）
   │        ↓
   │   flow checkpoint → 知识提取 + 记录 + git commit
   │        ↓
   └── 还有任务？→ 是 → 循环
                  否 ↓
5. flow finish → build/test/lint + Reflect + Experiment
   ↓
6. code-review → flow review（进化自愈检查）
   ↓
7. flow evolve（可选，深度反思）
   ↓
8. flow finish → 验证通过 → 最终提交 → idle
```

### 双模型协同流程

```
1. 触发词检测
   ↓
2. Claude worker: 需求分析 + 架构设计
   ↓
3. Codex workers: 并行实现（N个任务）
   ↓
4. Claude worker: 代码审查 + 质量把关
   ↓
5. 汇总报告
```

## 角色与技能映射

### 角色定义（来自 ai 仓库）

- **researcher** - 调研分析，收集信息，技术选型
- **planner** - 方案设计，制定计划，任务拆解
- **implementer** - 代码实现，编写代码，单元测试
- **reviewer** - 代码审查，质量把关，安全检查
- **verifier** - 验证测试，集成测试，性能测试
- **reporter** - 结果汇报，文档生成，总结输出

### 技能库（来自 ai 仓库）

- **superagents** - 统一编排入口，1 master + N workers
- **fix-bug** - 缺陷修复：定位 → 修复 → 验证
- **develop-feature** - 功能开发：设计 → 实现 → 测试
- **refactor** - 代码重构：分析 → 重构 → 验证
- **review-code** - 代码审查：静态分析 → 人工审查 → 建议
- **architecture-review** - 架构审查：设计评审 → 风险识别

### 任务类型自动路由

| 任务类型 | 角色组合 | 技能 |
|---------|---------|------|
| Bug 修复 | researcher + implementer + verifier | fix-bug |
| 新功能 | planner + implementer + reviewer + verifier | develop-feature |
| 重构 | planner + implementer + reviewer | refactor |
| 代码审查 | reviewer | review-code |
| 架构设计 | planner + reviewer | architecture-review |
| 调研分析 | researcher + reporter | answer |

## 质量门禁（来自 ai 仓库）

所有任务交付前检查：

1. **请求回看** - 逐条对照原始请求，标记 Done/Partial/Skipped
2. **产出物回读** - 审阅所有生成内容，检查遗漏/错误
3. **验证证据** - 提供命令 + 输出摘要，或说明无法验证原因
4. **质量门禁** - 按优先级检查：
   - 正确性 - 功能符合需求
   - 安全性 - 无安全漏洞（SQL注入、XSS、CSRF等）
   - 性能 - 满足性能要求
   - 可维护性 - 代码清晰易维护

未通过则自动修复，最多 3 轮；仍失败必须明确残余风险，禁止隐藏。

## 输出规范（来自 ai 仓库）

- **简洁直接** - 先结论，后细节
- **可执行** - 提供具体命令和步骤
- **有证据** - 附带验证结果（命令 + 输出摘要）
- **终端友好** - 适合命令行输出
- **文件引用** - 使用 `file:line` 格式

## 意图澄清（来自 ai 仓库）

适用条件：不确定性可通过快速扫描 + 一轮提问消除。

流程：
1. **开场对齐** - 回显"我理解的目标/范围/不做/关键假设"
2. **请求规范化** - 将原始请求收敛为可执行摘要
3. **快速扫描** - Glob/Grep 识别相关文件
4. **关键提问** - 有疑问时提问并等待回答
5. **生成方案** - 输出目标、范围、验收标准、不做项
6. **执行** - 需求明确且路径唯一时直接开始

提问规则：
- 需求明确、实现路径唯一：不提问，直接执行
- 涉及业务决策、缺少关键输入、多方案权衡：一次性提出全部关键问题
- 已进入 `brainstorming` 时：按其规则"一次一问"
- `AskUserQuestion` 不可用时：普通文本提问并暂停等待

## 命令参考

### FlowPilot 命令

```bash
flow init              # 初始化项目
flow next              # 获取下一个任务
flow next --batch      # 获取所有可并行任务
flow checkpoint <id>   # 标记任务完成
flow skip <id>         # 跳过任务
flow review            # 代码审查
flow finish            # 完成工作流
flow status            # 查看进度
flow resume            # 中断恢复
flow recall <关键词>   # 检索历史记忆
flow evolve            # 应用进化结果
```

### omx team 命令

```bash
omx team 2:executor "<task>"                    # 创建 2 个 executor
omx team status <team>                          # 查看状态
omx team attach <team>                          # 附加到 team
OMX_TEAM_WORKER_CLI_MAP=codex,claude omx team  # 双模型
```

## 环境变量

```bash
# FlowPilot（可选）
export ANTHROPIC_API_KEY="your-key"      # LLM 智能提取
export EMBEDDING_API_KEY="your-key"      # Dense 检索

# omx team（可选）
export OMX_TEAM_WORKER_CLI="claude"      # 或 codex
export OMX_TEAM_WORKER_CLI_MAP="codex,claude"
export OMX_TEAM_WORKER_LAUNCH_ARGS="--model gpt-4.5"
```

## Git 安全协议

- **永不**更新 git config
- **永不**运行破坏性命令（push --force, reset --hard）除非用户明确要求
- **永不**跳过 hooks（--no-verify）除非用户明确要求
- **永不**强制推送到 main/master，如果用户要求则警告
- **关键**：总是创建新提交而不是修改，除非用户明确要求 git amend
- 优先按名称添加特定文件，而不是 "git add -A" 或 "git add ."
- **永不**提交更改除非用户明确要求

## 错误处理

- **任务失败** - 自动重试 3 次，仍失败则标记 `failed` 并跳过
- **级联跳过** - 依赖失败任务的后续任务自动 `skipped`
- **中断恢复** - `active` 任务重置为 `pending`；有待接管变更时进入 `reconciling`
- **验证失败** - `flow finish` 报错后可派子Agent修复
- **循环检测** - 三策略防护（重复失败/乒乓/全局熔断）
- **心跳自检** - 活跃任务超时（>30分钟）告警
- **进化回滚** - 指标恶化时自动回滚

## 当前日期

Today's date is 2026-03-11.

---

**注意**: 本配置整合了 FlowPilot 和 AI Superagents，提供增强的全自动工作流能力。
