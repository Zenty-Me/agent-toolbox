# Claude Code 使用笔记

项目指令文件（`CLAUDE.md` / `AGENTS.md`）写法见 [project-instructions.md](project-instructions.md)。

## 优先安装路径（本仓库 / 官方 marketplace）

精选、按用途分类的第三方插件见 [../plugins/README.md](../plugins/README.md)。

长跑自主迭代（Ralph 插件、`max-iterations`、外层 bash 换新上下文）见 [自主持续迭代](autonomous-iteration.md)。

本仓库 skills（marketplace 名 `agent-toolbox`）：

```bash
/plugin marketplace add Zenty-Me/agent-toolbox
/plugin install frontend@agent-toolbox
# 其他：coding-standards / code-quality / planning / backend / skill-dev
/plugin marketplace update agent-toolbox
```

已安装旧名称时，见 [marketplace 迁移说明](../claude-code/README.md#marketplace-migration)。

官方目录与常用插件：

```bash
/plugin marketplace add anthropics/claude-plugins-official
/plugin install feature-dev@claude-plugins-official
/plugin install superpowers@claude-plugins-official
```

也可用 skills CLI 安装指定分区（以下选择 Claude Code 分区）：

```bash
npx skills add https://github.com/Zenty-Me/agent-toolbox/tree/main/claude-code/skills
npx skills add https://github.com/Zenty-Me/agent-toolbox/tree/main/claude-code/skills -s vercel-react-best-practices -g
```

## 体验向起步（hooks / 状态栏 / 记忆）

完整清单与安装命令见 [../plugins/README.md](../plugins/README.md) 的「Agent 使用体验」。最小组合（状态栏：纯 CC；双修见下方 Statusline 选型）：

```bash
npx -y ccstatusline@latest          # 状态栏（写入 ~/.claude/settings.json）
/plugin install hookify@claude-plugins-official
/plugin install claude-md-management@claude-plugins-official
/plugin install remember@claude-plugins-official   # 可选：更强跨会话记忆
npx tweakcc                         # 可选：主题 / spinner / 输入框样式
```

原生能力：`/statusline`、`/hooks`、settings 里的 `statusLine` 与 `Notification` hook。文档：[statusline](https://code.claude.com/docs/en/statusline)、[hooks](https://code.claude.com/docs/en/hooks-guide)。

### Statusline 选型

按 **Claude Code + Pi 双修** 场景排序（核实：2026-10-15）。官方接口：[statusline](https://code.claude.com/docs/en/statusline)。Pi 终端渲染见 [pi.md](pi.md)。

1. **双修首选**：[callmemorgan/claude-statusline](https://github.com/callmemorgan/claude-statusline) — 同时盖 Claude Code / Pi / Antigravity。Pi：`pi install npm:@morgan.rebrand/claude-statusline`；两边可统一风格（Pi 上额度/cost 段会藏，只留 model/context/git 等）
2. **纯 Claude Code 主流**：[sirmalloc/ccstatusline](https://github.com/sirmalloc/ccstatusline)（约 1.3 万★，TUI 配主题）：`npx -y ccstatusline@latest`（即上方最小组合）
3. **信息密度**：[erwint/claude-code-statusline](https://github.com/erwint/claude-code-statusline) — Agent/Todo/Tool、5h·周额度等；`/plugin marketplace add erwint/claude-code-statusline` 再 `/plugin install cc-statusline@cc-statusline`（仓小，不是社区默认）
4. **备选**：[gfreschi/claude-code-statusline](https://github.com/gfreschi/claude-code-statusline)（颜值/Powerline）、[OpenAnalystInc/Statusline](https://github.com/OpenAnalystInc/Statusline)（`npx skill-statusline install`）、[rz1989s/claude-code-statusline](https://github.com/rz1989s/claude-code-statusline)（约 480★ 壳脚本）

结论：双修 → callmemorgan；纯 CC → ccstatusline。下文 Context Monitor 是 aitmpl 模板示例，别当选型默认。

## 规划/执行分模型

两边都能规划用强模型、干活用便宜/快模型；Claude Code 有一键口（核实：2026-10-14）：

- **`opusplan`**：`/model opusplan` 或 `claude --model opusplan` — Plan Mode 用 Opus，批准后自动切 Sonnet 执行（也可用 `opusplan[1m]`）
- **子代理**：agent frontmatter 或 Task/`Agent` 参数写 `model: haiku|sonnet|opus`（或完整模型名）；社区常见 Opus 规划、Sonnet 改码、Haiku 跑腿
- **`/advisor`**：主模型干活时顾问模型旁听（`advisorModel` / `claude --advisor …`）；与 `opusplan` 不同——顾问是中途咨询，不是计划边界自动切换

官方：[model-config](https://code.claude.com/docs/en/model-config)、[advisor](https://code.claude.com/docs/en/advisor)。Pi 侧无 `opusplan`、靠 subagents / skill-model-handoff，见 [pi.md](pi.md)。跨 harness 把对方包成工具：见 [cross-agent.md](cross-agent.md)。

## 子 agent 配置

写 Markdown + YAML frontmatter 到 `.claude/agents/`（项目）或 `~/.claude/agents/`（个人）。必填 `name`、`description`；正文=系统提示。常用：`tools` / `disallowedTools`、`model`（sonnet/haiku/inherit…）、`isolation: worktree`、`background`、`memory`（核实：2026-10-15）。

最小例子：

```markdown
---
name: code-reviewer
description: 改完代码后主动做安全与质量审查。Use proactively.
tools: Read, Grep, Glob, Bash
model: sonnet
---
你是代码审查员。看 diff，按严重程度输出问题与改法。
```

调用：自然语言点名、`@` agent，或 `claude --agent code-reviewer`。内置：Explore / Plan / general-purpose。

注意：

- 新版 `/agents` **不再**开创建向导，直接写文件或让 Claude 写
- 子 agent **看不到**主会话历史，路由全靠 `description`
- 社区：编排用强模型，干活用便宜子 agent；**显式写 `model:`**，别依赖静默默认

教程：[官方 sub-agents](https://code.claude.com/docs/en/sub-agents) · [Builder.io](https://www.builder.io/blog/claude-code-subagents) · [Agent Notebook](https://www.agentnotebook.dev/tutorials/claude-code-subagents)

分模型口（`opusplan` / 子代理 model / `/advisor`）见上一节；跨 harness 见 [cross-agent.md](cross-agent.md)。

## 多会话分工

核实日期：**2026-10-15**。多开会话改同一仓时的落点、全局规则与「领航」调度（仓侧笔记，非整页粘贴）。

### 落点与官方对照

- **全局纪律**：`~/.claude/CLAUDE.md`（用户级）。仓内共享用项目 `CLAUDE.md` / `AGENTS.md`（Codex 读 AGENTS；共用时 `CLAUDE.md` 首行 `@AGENTS.md`）。官方：[memory](https://code.claude.com/docs/en/memory)
- **并行改同一仓**：优先 [git worktrees](https://code.claude.com/docs/en/worktrees)，每会话划文件边界
- **官方编排（可选）**：[Agent teams](https://code.claude.com/docs/en/agent-teams)（`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`）一会话当 lead；更轻用跨会话消息 / 子 agent。手动「领航」多开会话与 Agent teams **勿两套同时当老板**

### 全局规则（建议写入用户级 CLAUDE.md）

1. **先定稿再动手**
2. **主会话**：规划、定边界、核对证据、终审与汇报；小改自做；整块派出须写清任务/边界/验收
3. **按定稿程度**：未定 UI → 主会话快迭代+截图；已定模型/接口/测试/批量 → 默认可派 Codex 后台
4. **Codex 优先省额度**：代码/测试/批量/只读核查 → `codex exec`；写作与设计仍用 Claude
5. **调用 Codex**（推理默认 high；算钱/并发可用 xhigh。Fast 现名常写 `service_tier="fast"`，旧 `priority` 仍见；**注意**：`codex exec` 上 Fast 可能被服务端**静默回落**。可用 `--worktree`。任务写独立文件后台跑，等完成通知勿轮询；Codex 不提交，主会话提交。禁 Codex 屏幕/浏览器插件；浏览器只用无头）：

```bash
codex exec --skip-git-repo-check -m <模型> \
  -c 'service_tier="priority"' -c model_reasoning_effort=high \
  "…任务…"
```

6. **子代理分档**：haiku=查库/日志/测/截图/文案；sonnet=多数实现与复核；opus=账务/退款/并发/数据模型
7. **涉钱交叉复核**；阶段末写交接开新会话；生产写入需明确授权；自起长驻记 PID/端口，结束即停

### 「领航」调度（手动多开，如 agterm）

- **角色**：只派活不动手；写清任务/边界/验收；只读盘点、核对、汇总、汇报
- **自治可直接定**：本地 commit、清本地分支、DEV、只读核查、派 Codex、不花钱不外发默认项
- **必先问**：远端 push/PR/评审/远端分支/仓设置、生产写入、花钱、对外发布、业务方向、退出或关会话
- **转述**：原话转述；领航建议标「领航建议」；规则只发相关会话不群发
- **巡检**：卡住直接催；汇报分「需你回复」与「状态变化」

跨 harness 把对方包成工具见 [cross-agent.md](cross-agent.md)；子 agent 见上一节。

## 其他资源站点

- https://www.aitmpl.com/：Claude Code 相关 skills、plugins、Commands、Settings、Hooks 等资源聚合

## 其他 Agent（Codex / Cursor）可复用来源

多数 Agent Skills 标准 skill 可在 Claude Code、Codex、Cursor 间复用。本仓库 `skills/` 已精选一批；更多列表不必全量搬入：

- [openai/skills](https://github.com/openai/skills) — Codex 官方 skills 目录
- [composio-community/awesome-codex-skills](https://github.com/composio-community/awesome-codex-skills) — Codex 实用 skills 精选
- [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) — 多 harness 社区合集（质量参差，需挑）
- [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)、[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) — 已有条目收录进本仓库 `skills/`

## 备选：claude-code-templates（非本仓库主推）

若需从 aitmpl / claude-code-templates 拉单个模板，可用（路径可能随上游变更）：

```bash
npx claude-code-templates@latest --skill creative-design/frontend-design
npx claude-code-templates@latest --skill development/code-reviewer
npx claude-code-templates@latest --skill development/clean-code
```

**Context Monitor**（statusline）示例：

```bash
npx claude-code-templates@latest --setting statusline/context-monitor
```

再在 `~/.claude/settings.json` 最外层加入：

```json
{
  "statusLine": {
    "type": "command",
    "command": "python3 ~/.claude/plugins/.claude/scripts/context-monitor.py"
  }
}
```

本仓库已收录的同名 skill（如 `frontend-design`、`clean-code`）优先用上文 marketplace / `npx skills` 安装即可。
