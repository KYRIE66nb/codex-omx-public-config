# Codex + OMX Public Config

这是我当前在用的一套公开可复刻配置快照，目标是把 Codex CLI、oh-my-codex、MCP、workflow、skills、Claude 协同层一起迁移到别的机器，同时不泄露任何密钥、登录态、历史会话和日志。

## 包含内容

- `home/AGENTS.md` 和 `home/CLAUDE.md`
- `home/.codex/AGENTS.md`
- `home/.codex/agents`
- `home/.codex/prompts`
- `home/.codex/skills`
- `home/.codex/memories/skills`
- `home/.agents/skills` 和 `home/.agents/.skill-lock.json`
- `home/.omx/agents`
- `home/.claude/agents`
- `home/.claude/rules`
- `home/.claude/openviking-memory-plugin`
- `home/vendor_imports/awesome-codex-subagents`
- 脱敏模板:
  - `templates/.codex/config.toml`
  - `templates/.codex/.omx-config.json`
  - `templates/.claude/config.toml`
  - `templates/.claude/api-key-helper.sh`
  - `templates/.config/codex/env.example`
  - `templates/shell/zshrc.codex-fragment.zsh`

## 明确排除

- `auth.json`
- API keys / tokens
- `history.jsonl`
- `sessions/`
- `shell_snapshots/`
- `.sqlite` 日志数据库
- `.omx/logs` / `.omx/state` / `.omx/team-jobs`
- 各类 backup、debug、cache、paste-cache、project runtime

## 当前版本

- `codex-cli 0.115.0`
- `oh-my-codex v0.11.13`
- `Node.js v22.22.0`
- `darwin arm64`

## 快速复刻

1. 安装基础工具:

```bash
npm install -g @openai/codex oh-my-codex
```

2. 克隆本仓库到任意目录:

```bash
git clone <this-repo-url>
cd codex-omx-public-config
```

3. 准备私有环境变量文件:

```bash
mkdir -p ~/.config/codex
cp templates/.config/codex/env.example ~/.config/codex/env
```

4. 编辑 `~/.config/codex/env`，填入你自己的 key 和 token。

5. 安装配置:

```bash
./scripts/install.sh
```

6. 在你的 `~/.zshrc` 里加入:

```bash
source "$HOME/.config/codex/zshrc.codex-fragment.zsh"
```

7. 重开终端后验证:

```bash
omx doctor
codex --version
```

## 可覆盖的安装变量

```bash
TARGET_HOME="$HOME"
OPENAI_BASE_URL_VALUE="https://tokenx24.com/v1"
CLAUDE_OPENAI_BASE_URL_VALUE="https://claw.xclawxx.top/v1"
OPENCLAW_GATEWAY_URL="http://127.0.0.1:18789/hooks/wake"
OPENCLAW_GATEWAY_TOKEN="..."
OMX_NOTIFY_HOOK="/path/to/oh-my-codex/dist/scripts/notify-hook.js"
```

## 目录说明

- `home/`: 直接同步到 `$HOME` 的公开文件
- `templates/`: 需要按目标机器路径和私有变量渲染的模板
- `scripts/install.sh`: 安装器
- `scripts/check-no-secrets.sh`: 公共仓库密钥扫描

## 说明

- 这是“公开版行为快照”，重点是复刻工作流和编排行为，不是裸拷运行痕迹。
- `templates/.codex/.omx-config.json` 的 OpenClaw 网关在没有 token 时会被安装脚本自动禁用。
- `templates/.claude/api-key-helper.sh` 会从 `~/.config/codex/env` 读取 `ANTHROPIC_AUTH_TOKEN`。

