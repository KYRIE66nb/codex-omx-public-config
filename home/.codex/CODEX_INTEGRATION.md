# Codex 工作流整合配置

## 已同步的内容

✅ **agents/** - 6 个专业角色
- researcher.md
- planner.md
- implementer.md
- reviewer.md
- verifier.md
- reporter.md

✅ **skills/** - 专项技能库
- superagents/
- fix-bug/
- develop-feature/
- refactor/
- review-code/
- architecture-review/
- 等等...

✅ **rules/** - 全局规则约束
- code-quality.md
- output-style.md
- fast-path.md

✅ **AGENTS.md** - 增强的工作流协议
- FlowPilot 调度引擎集成
- 双模型协同配置
- 自然语言触发词
- 角色与技能映射

✅ **flow.js** - FlowPilot 核心引擎

## 在 Codex 中使用

### 方式 1：标准 FlowPilot 工作流

```bash
# 启动 Codex
codex --yolo

# 说触发词
你：全自动开发一个 TODO 应用
```

### 方式 2：双模型协同

```bash
# 在 Codex 中说：
codex+claude

实现一个电商系统
```

系统会自动：
- 在 tmux 中创建 team
- Codex 和 Claude 协同工作
- Codex 负责实现，Claude 负责架构和审查

### 方式 3：使用 flow 命令

```bash
# 在项目中
cd /your/project

# 初始化
node ~/.codex/flow.js init

# 或使用全局命令
flow init

# 然后启动 Codex
codex --yolo
```

## 自然语言触发词

### FlowPilot 工作流
- `全自动开发`
- `自动工作流`
- `flowpilot`
- `flow 工作流`

### 双模型协同
- `claude code协同`
- `codex+claude`
- `双模型协同`
- `opus4.6当大脑`
- `codex当员工`

### Claude 监工模式
- `claude当监工`
- `claude指挥codex`
- `监工大脑`

### 论文工作流
- `写毕业论文`
- `生成论文大纲`
- `设计数据库表`
- `画ER图`

## Codex 特有配置

### config.toml 中的设置

```toml
# 已启用的功能
[features]
multi_agent = true              # 多 Agent 支持
child_agents_md = true          # 子 Agent 使用 AGENTS.md

# 开发者指令
developer_instructions = "You have oh-my-codex installed. Use /prompts:architect, /prompts:executor, /prompts:planner for specialized agent roles. Workflow skills via $name: $ralph, $autopilot, $plan. AGENTS.md is your orchestration brain."
```

### 推荐设置

```toml
# 全自动模式
approval_policy = "never"       # 不需要确认
sandbox_mode = "workspace-write" # 工作区写入权限

# 模型配置
model = "gpt-5.4"               # 或 "gpt-4.5"
model_reasoning_effort = "xhigh" # 高推理能力
```

## 与 Claude Code 的区别

| 特性 | Claude Code | Codex |
|------|-------------|-------|
| 配置文件 | `~/.claude/settings.json` | `~/.codex/config.toml` |
| 工作流协议 | `CLAUDE.md` | `AGENTS.md` |
| 启动命令 | `claude --dangerously-skip-permissions` | `codex --yolo` |
| 多 Agent | `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` | `multi_agent = true` |
| 角色定义 | `~/.claude/agents/` | `~/.codex/agents/` |
| 技能库 | `~/.claude/skills/` | `~/.codex/skills/` |

## 验证安装

```bash
# 检查文件
ls ~/.codex/AGENTS.md
ls ~/.codex/flow.js
ls ~/.codex/agents/
ls ~/.codex/skills/
ls ~/.codex/rules/

# 测试 flow 命令
node ~/.codex/flow.js --help

# 或使用全局命令
flow --help
```

## 使用示例

### 示例 1：在 Codex 中使用 FlowPilot

```bash
# 启动 Codex
codex --yolo

# 说：
全自动开发一个博客系统，包括：
- 文章发布和编辑
- 评论功能
- 用户认证
- 标签和分类
```

### 示例 2：双模型协同

```bash
# 启动 Codex
codex --yolo

# 说：
codex+claude

实现一个在线教育平台，包括：
- 课程管理
- 视频播放
- 作业提交
- 成绩管理
```

### 示例 3：使用 oh-my-codex 集成

```bash
# 启动 Codex
codex --yolo

# 使用 oh-my-codex 的 prompts
/prompts:architect  # 架构设计
/prompts:executor   # 执行实现
/prompts:planner    # 规划任务

# 或使用工作流技能
$ralph              # Ralph 工作流
$autopilot          # 自动驾驶模式
$plan               # 规划模式
```

## 环境变量

```bash
# 双模型协同（可选）
export OMX_TEAM_WORKER_CLI_MAP="codex,claude"
export OMX_TEAM_WORKER_LAUNCH_ARGS="--model gpt-4.5"

# FlowPilot 增强（可选）
export ANTHROPIC_API_KEY="your-key"
export EMBEDDING_API_KEY="your-key"
```

## 更新

### 更新工作流协议

```bash
cp ~/ai-workflow-integration/CLAUDE.md ~/.codex/AGENTS.md
```

### 更新 FlowPilot 引擎

```bash
cp ~/.ai-workflow/bin/flow.js ~/.codex/
```

### 更新 agents/skills/rules

```bash
cd /tmp/ai
git pull
cp -r agents ~/.codex/
cp -r skills ~/.codex/
cp -r rules ~/.codex/
```

## 故障排除

### 问题 1：Codex 不识别 AGENTS.md

**解决**：
```bash
# 检查 config.toml
grep "child_agents_md" ~/.codex/config.toml

# 如果没有，添加：
[features]
child_agents_md = true
```

### 问题 2：flow 命令不工作

**解决**：
```bash
# 使用完整路径
node ~/.codex/flow.js init

# 或使用全局命令
flow init
```

### 问题 3：双模型协同不工作

**解决**：
```bash
# 检查 omx 是否安装
which omx

# 检查环境变量
echo $OMX_TEAM_WORKER_CLI_MAP
```

## 下一步

1. **测试基本功能**：
   ```bash
   codex --yolo
   # 说：全自动开发一个简单的计算器
   ```

2. **测试双模型协同**：
   ```bash
   codex --yolo
   # 说：codex+claude，实现一个 TODO 应用
   ```

3. **查看文档**：
   ```bash
   cat ~/ai-workflow-integration/HOW_TO_USE.md
   ```

---

**配置完成时间**: 2026-03-11
**Codex 版本**: 支持 gpt-5.4 / gpt-4.5
