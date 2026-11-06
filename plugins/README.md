# Agent 插件与扩展清单

插件通过各 agent 自己的 marketplace / 包管理安装。本页收**日常开发实用**、仓库存在且近期还在维护的推荐条目（核实日期：2026-10-14），不全量镜像各官方目录。体验向（hooks / 状态栏 / 记忆 / 主题）见 Claude Code 章节的「Agent 使用体验」。

本机实际安装版本另见[同步记录](local-sync.md)与[机器可读清单](installed.json)；[Pi 目录](pi/README.md)提供精确版本恢复命令，并归档 Pi Switch 和 compact-status 本地源码。

| Agent | 扩展机制 | 跳转 |
|---|---|---|
| Claude Code | plugin marketplace（`/plugin`）、skills、hooks、MCP | [Claude Code](#claude-code) |
| Codex（OpenAI Codex CLI） | plugin marketplace（`/plugins`、`codex plugin`）、skills、MCP、hooks | [Codex](#codex) |
| Pi（pi coding agent） | pi packages（`pi install`）、MCP adapter、AGENTS.md / APPEND_SYSTEM | [Pi](#pi) · [笔记](../agents-learning/pi.md) |
| Cursor | Cursor Plugins / Agent Plugins（Customize 面板、Cursor Marketplace）、rules、MCP | [Cursor](#cursor) |
| Gemini CLI | extensions（`gemini extensions install`） | [Gemini CLI](#gemini-cli) |
| OpenCode | npm 插件（`opencode.json` 的 `plugin`）、本地插件目录 | [OpenCode](#opencode) |
| 多种 agent 通用 | 独立 CLI / hooks / MCP | [跨 agent 通用工具](#跨-agent-通用工具) |

## Claude Code

本机显式开启的插件为 Matt Pocock Skills 1.2.3、Ponytail 5.1.0、Warp 2.4.0；其余已登记安装项的版本与配置状态见[同步记录](local-sync.md#claude-code)。

### 安装方式

先添加 marketplace，再安装插件：

```bash
/plugin marketplace add <marketplace 仓库>
/plugin install <插件名>@<marketplace 名>
```

更新：`/plugin marketplace update <marketplace 名>`。

### Marketplace

| 名称 | 仓库 | 说明 |
|---|---|---|
| claude-plugins-official | anthropics/claude-plugins-official | Anthropic 官方目录（含首方插件与精选第三方；约 300+） |
| knowledge-work-plugins | anthropics/knowledge-work-plugins | 官方 Knowledge Work：按岗位角色（sales / marketing / legal / finance 等）打包 |
| skills（官方 Agent Skills） | anthropics/skills | 官方 skill 市场；含 `document-skills`（PDF/DOCX/PPTX/XLSX）等 |
| claude-plugins-community | anthropics/claude-plugins-community | 社区插件市场（自动化校验；建议 pin SHA） |
| supabase-agent-skills | supabase/agent-skills | Supabase / Postgres skill 插件 |
| claude-code-workflows | wshobson/agents | 多 harness 工作流与开发插件合集 |
| planning-with-files | OthmanAdi/planning-with-files | 文件化持久计划 |
| ponytail | DietrichGebert/ponytail | 强制最简实现 |
| claude-code-warp | warpdotdev/claude-code-warp | Warp 终端通知与集成 |

> 多数第三方插件也可直接从 `claude-plugins-official` 安装（例如 `github@claude-plugins-official`）。若某插件同时出现在专用 marketplace，任选其一即可。
>
> Knowledge Work / Skills 示例：
> ```bash
> /plugin marketplace add anthropics/knowledge-work-plugins
> /plugin install productivity@knowledge-work-plugins
> /plugin marketplace add anthropics/skills
> /plugin install document-skills@anthropic-agent-skills
> ```

### 插件列表

#### 开发流程

| 插件 | 说明 |
|---|---|
| `superpowers@claude-plugins-official` | 核心技能库：头脑风暴、TDD、子 agent 开发、内置审查等 |
| `feature-dev@claude-plugins-official` | 完整功能开发：代码库探索、架构设计、质量审查 |
| `planning-with-files@planning-with-files` | 用项目文件持久化开发计划，hooks 注入计划上下文 |
| `ralph-loop@claude-plugins-official` | 循环迭代同一提示直到完成（Ralph Wiggum 技法）；做法见 [autonomous-iteration.md](../agents-learning/autonomous-iteration.md) |
| `ponytail@ponytail` | 强制最简实现：YAGNI、优先标准库、不做多余抽象 |
| `mattpocock-skills@claude-plugins-official` | Matt Pocock 的方案追问、规格/工单、TDD、架构与代码审查技能包 |
| `code-modernization@claude-plugins-official` | 遗留代码现代化：评估、业务规则挖掘、改造/重写与验证 |
| `claude-code-setup@claude-plugins-official` | 分析仓库并推荐 hooks、skills、MCP、subagent 等自动化 |
| `claude-md-management@claude-plugins-official` | 维护 CLAUDE.md：质量审计、沉淀会话学习、保持项目记忆 |
| `hookify@claude-plugins-official` | 用 markdown 规则快速写 hooks，约束不想要的行为 |
| `project-artifact@claude-plugins-official` | 生成可分享的项目状态页（目标、工作流、下一步） |
| `conductor@claude-code-workflows` | Context-Driven Development：Context → Spec & Plan → Implement |
| `ship-mate@claude-code-workflows` | 故事文件驱动：架构 → 开发 → PR 审查 → QA → Playwright |
| `tdd-workflows@claude-code-workflows` | 红绿重构 TDD 工作流与配套审查 |
| `developer-essentials@claude-code-workflows` | Git/SQL/错误处理/代码审查/E2E/鉴权/monorepo 等基础技能包 |

#### 代码审查与质量

| 插件 | 说明 |
|---|---|
| `code-review@claude-plugins-official` | 多专用 agent 对 PR 自动审查，带置信度评分 |
| `pr-review-toolkit@claude-plugins-official` | PR 审查合集：注释、测试、错误处理、类型、简化 |
| `code-simplifier@claude-plugins-official` | 不改变功能的前提下简化、规范代码 |
| `security-guidance@claude-plugins-official` | 编辑时安全模式警告 + Stop 时 diff 审查 + 提交审查 |
| `claude-security@claude-plugins-official` | 会话内深度漏洞扫描，发现经多 agent 挑战后再给补丁 |
| `semgrep@claude-plugins-official` | 实时安全扫描，引导写出更安全的代码 |
| `coderabbit@claude-plugins-official` | 外部 AI 审查伙伴，配合 40+ 静态分析器交叉验证 |
| `greptile@claude-plugins-official` | GitHub/GitLab AI 审查：查看/处理评论、对工作分支跑审查 |
| `debugging-toolkit@claude-code-workflows` | 交互式调试与调试工作流 |
| `comprehensive-review@claude-code-workflows` | 多视角审查：架构、安全、最佳实践 |
| `security-scanning@claude-code-workflows` | SAST、依赖漏洞、OWASP、容器安全扫描 |
| `code-refactoring@claude-code-workflows` | 清理、重构自动化与技术债管理 |
| `unit-testing@claude-code-workflows` | Python/JS 单元与集成测试自动化 |
| `performance-testing-review@claude-code-workflows` | 性能分析、测试覆盖与代码质量评估 |

#### 工具与集成

先装「日常必装」，再按技术栈补「按需」。星标为大多数开发仓库的默认起点（约 12 个）。

##### 日常必装（★ 推荐）

| 插件 | 说明 |
|---|---|
| ★ `github@claude-plugins-official` | GitHub MCP：Issue/PR/代码搜索与仓库操作 |
| ★ `commit-commands@claude-plugins-official` | git 提交、推送、创建 PR 的快捷命令 |
| ★ `context7@claude-plugins-official` | 查询最新库文档（MCP，远程托管） |
| ★ `playwright@claude-plugins-official` | 浏览器自动化与端到端测试（MCP） |
| ★ `serena@claude-plugins-official` | 语义代码分析 MCP（LSP）：理解、导航与重构建议 |
| ★ `typescript-lsp@claude-plugins-official` | TS/JS 语言智能（前端/Node 项目几乎都要） |
| ★ `pyright-lsp@claude-plugins-official` | Python 语言智能（有 Python 再装） |
| ★ `vercel@claude-plugins-official` | Vercel 部署/构建/日志（用 Vercel 再装） |
| ★ `sentry@claude-plugins-official` | 生产报错与栈追踪（已接 Sentry 再装） |
| ★ `figma@claude-plugins-official` | 读设计文件与 token，辅助落地 UI |
| ★ `notion@claude-plugins-official` | 搜页面、写文档、管知识库 |
| ★ `linear@claude-plugins-official` | 事务跟踪（团队用 Linear 时） |

> `typescript-lsp` / `pyright-lsp` 与下文「语言智能」表重复列出，是为了把「第一天该装什么」收在一处；其余语言 LSP 仍见专表。

##### 按需（栈相关 / 少用场景）

| 插件 | 说明 |
|---|---|
| `gitlab@claude-plugins-official` | GitLab：仓库、MR、CI/CD、Issue、Wiki |
| `atlassian@claude-plugins-official` | Jira / Confluence |
| `cloudflare@claude-plugins-official` | Cloudflare：Workers、DO、Agents SDK、Wrangler 等 |
| `firebase@claude-plugins-official` | Firebase：Firestore、Auth、Functions、Hosting、Storage |
| `prisma@claude-plugins-official` | Prisma Postgres：schema 迁移、SQL、连接串 |
| `terraform@claude-plugins-official` | Terraform MCP：IaC |
| `datadog@claude-plugins-official` | Datadog：日志、指标、链路、看板 |
| `stripe@claude-plugins-official` | Stripe 支付集成 |
| `expo@claude-plugins-official` | Expo / React Native |
| `laravel-boost@claude-plugins-official` | Laravel 智能辅助 |
| `firecrawl@claude-plugins-official` | 网页抓取为 Markdown / 结构化数据 |
| `exa@claude-plugins-official` | Exa 网页搜索与深度研究 |

#### 语言智能（LSP）

官方提供多语言 LSP 插件，给 Claude 更强的跳转、类型与重构能力。按项目语言选装即可：

| 插件 | 说明 |
|---|---|
| `typescript-lsp@claude-plugins-official` | TypeScript / JavaScript |
| `pyright-lsp@claude-plugins-official` | Python（Pyright） |
| `gopls-lsp@claude-plugins-official` | Go |
| `rust-analyzer-lsp@claude-plugins-official` | Rust |
| `clangd-lsp@claude-plugins-official` | C / C++ |
| `jdtls-lsp@claude-plugins-official` | Java |
| `csharp-lsp@claude-plugins-official` | C# |
| `kotlin-lsp@claude-plugins-official` | Kotlin |
| `ruby-lsp@claude-plugins-official` | Ruby |
| `php-lsp@claude-plugins-official` | PHP |
| `swift-lsp@claude-plugins-official` | Swift |
| `lua-lsp@claude-plugins-official` | Lua |

#### 技能与扩展开发

| 插件 | 说明 |
|---|---|
| `skill-creator@claude-plugins-official` | 创建、改进、评测 skill |
| `frontend-design@claude-plugins-official` | 前端 UI/UX 设计 |
| `supabase@supabase-agent-skills` | Supabase 开发 |
| `postgres-best-practices@supabase-agent-skills` | Postgres 最佳实践 |
| `plugin-dev@claude-plugins-official` | 插件开发：agent、command、hooks、MCP、结构指南 |
| `mcp-server-dev@claude-plugins-official` | 设计与构建适配 Claude 的 MCP server |
| `agent-sdk-dev@claude-plugins-official` | Claude Agent SDK 开发套件 |
| `mcp-tunnels@claude-plugins-official` | 经 Anthropic MCP tunnel 连接私有 MCP（Docker 快速起步） |
| `playground@claude-plugins-official` | 生成可交互的单文件 HTML playground（控件 + 实时预览） |

#### 输出风格与会话辅助

| 插件 | 说明 |
|---|---|
| `explanatory-output-style@claude-plugins-official` | 解释实现选择与代码库模式（替代已弃用的 Explanatory 输出风格） |
| `learning-output-style@claude-plugins-official` | 交互式学习：在决策点要求你动手写关键代码 |
| `session-report@claude-plugins-official` | 从本地会话日志生成用量 HTML 报告（token、缓存、贵提示等） |
| `remember@claude-plugins-official` | 跨会话连续记忆：SessionStart / PostToolUse hooks + 日志；`/remember` 交接（市场安装量很高） |

`skill-creator`、`frontend-design`、`supabase`、`postgres-best-practices`、以及本仓库 `coding-standards` 中的 `humanizer` 等，与官方/上游 marketplace 可能同名，二选一即可。

### Agent 使用体验

只适用于 Claude Code 的体验工具：hooks、状态栏、主题、用量、会话 GUI、记忆连续性。支持多种 agent 的通知、记忆、多会话管理器放在下文[跨 agent 通用工具](#跨-agent-通用工具)。★ 为最推荐。

**架构说明：** 插件可打包 hooks / commands / skills，但 `statusLine` 写在 `~/.claude/settings.json`（不是插件 manifest）。状态栏类工具通常靠 SessionStart hook 或 `/setup` 把配置写进去。官方文档：[statusline](https://code.claude.com/docs/en/statusline)、[hooks](https://code.claude.com/docs/en/hooks-guide)。

#### 官方体验类插件（hooks / 记忆 / 用量）

上文「开发流程」「输出风格与会话辅助」已列；这里收成体验向短表，方便对照：

| 插件 | 改善点 | 安装 |
|---|---|---|
| ★ `hookify@claude-plugins-official` | 用对话或 markdown 写 warn/block hooks，少手写 JSON | `/plugin install hookify@claude-plugins-official` |
| ★ `claude-md-management@claude-plugins-official` | 审计 / 改进 `CLAUDE.md`，沉淀会话学习 | `/plugin install claude-md-management@claude-plugins-official` |
| ★ `remember@claude-plugins-official` | 跨会话连续记忆（SessionStart / PostToolUse） | `/plugin install remember@claude-plugins-official` |
| `claude-code-setup@claude-plugins-official` | 扫仓库，推荐 hooks / skills / MCP / subagent | `/plugin install claude-code-setup@claude-plugins-official` |
| `session-report@claude-plugins-official` | 会话 token / 缓存 / 贵提示的 HTML 报告 | `/plugin install session-report@claude-plugins-official` |
| `explanatory-output-style` / `learning-output-style` | 解释型输出 / 交互式学习模式 | `@claude-plugins-official` |
| `plugin-dev@claude-plugins-official` | 自己写 hooks / commands / agents 时的脚手架 | `/plugin install plugin-dev@claude-plugins-official` |

#### 状态栏 / 主题 / 用量 / GUI

| 工具 | 来源 | 说明 | 安装 / 启用 |
|---|---|---|---|
| ★ ccstatusline | [sirmalloc/ccstatusline](https://github.com/sirmalloc/ccstatusline) | 可高度自定义的状态栏（模型、上下文用量、git、费用、限流、powerline；官方 statusline 文档亦提及） | `npx -y ccstatusline@latest` 交互配置，写入 `~/.claude/settings.json` 的 `statusLine` |
| claude-powerline | [Owloops/claude-powerline](https://github.com/Owloops/claude-powerline) | vim 风格 powerline 状态栏，开箱主题；`/powerline` 向导 | `/plugin marketplace add Owloops/claude-powerline` → `/plugin install claude-powerline@claude-powerline` |
| ★ tweakcc | [Piebald-AI/tweakcc](https://github.com/Piebald-AI/tweakcc) | 改 Claude Code 主题、spinner、输入框等界面样式 | `npx tweakcc` |
| cc-statusline（CN） | [dualface/cc-statusline](https://github.com/dualface/cc-statusline) | 偏中文场景的状态栏插件（模型 / effort / 任务耗时；SessionStart 注入） | 见仓库 README（marketplace 安装） |
| ccstatusline-zh | [huangguang1999/ccstatusline-zh](https://github.com/huangguang1999/ccstatusline-zh) | ccstatusline 中文本地化 fork（第三方，装前审一下） | 见仓库 README |
| SammyLin/cc-statusline | [SammyLin/cc-statusline](https://github.com/SammyLin/cc-statusline) | 多行看板 + Subagent / PreCompact 等 hooks | `/plugin marketplace add SammyLin/cc-statusline` → 安装 `cc-statusline@cc-statusline` |
| ★ ccusage | [ccusage/ccusage](https://github.com/ccusage/ccusage) | 读取本地日志，按日/月/会话/5 小时窗口统计 token 和费用 | `npx ccusage@latest`（如 `npx ccusage@latest daily`、`blocks --live`） |
| Claude Code Usage Monitor | [Maciek-roboblog/Claude-Code-Usage-Monitor](https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor) | 终端实时额度看板，预测何时用完并提前告警 | `uv tool install claude-monitor`（或 `pip install claude-monitor`），运行 `claude-monitor` |
| opcode | [winfunc/opcode](https://github.com/winfunc/opcode) | Claude Code 桌面 GUI：管理会话、自定义 agent、查看用量、浏览会话历史 | 从 GitHub Releases 下载，或按 README 从源码构建 |
| claude-code-viewer | [d-kimuson/claude-code-viewer](https://github.com/d-kimuson/claude-code-viewer) | Web 客户端：浏览和恢复历史会话，并在网页中继续对话 | `npx @kimuson/claude-code-viewer@latest --port 3400` |

#### 原生能力（不必装插件）

| 能力 | 位置 | 说明 |
|---|---|---|
| `statusLine` / `refreshInterval` / `subagentStatusLine` | `~/.claude/settings.json` | 任意 shell 命令画状态栏；stdin 给会话 JSON |
| `/statusline` | 内置斜杠命令 | 用自然语言生成自定义 statusline 脚本 |
| `hooks` + `/hooks` | 用户/项目 settings 或插件 `hooks/hooks.json` | Notification、Pre/PostToolUse、Stop、SessionStart、PreCompact 等 |
| `CLAUDE.md` + `#` 快捷写入 | 项目 / 用户记忆 | 原生上下文记忆；`claude-md-management` / `remember` 是增强 |
| `permissions.allow/ask/deny` | settings | 确认/拦截 UX，无需插件 |
| `/usage` | 内置 | 费用与用量；也可叠 statusline JSON 字段 |

桌面通知示例（Linux，写入 settings 的 `hooks`）：

```json
{
  "hooks": {
    "Notification": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "notify-send 'Claude Code' 'Needs your attention'"
      }]
    }]
  }
}
```

跨 agent 的打包通知 / 记忆见下文 [agent-notifications](#跨-agent-通用工具)、[claude-mem](#跨-agent-通用工具)。

#### 体验向起步短清单

1. 状态栏：`ccstatusline`（与 `claude-powerline` 二选一）
2. Hooks：`hookify`
3. 记忆：`claude-md-management`；要更强跨会话连续性再加 `remember` 或跨 agent 的 `claude-mem`
4. 通知：先写原生 `Notification` hook；不够再装 `agent-notifications`
5. 仓库定制：跑一次 `claude-code-setup`
6. 外观：`tweakcc`

> 状态栏同时只能生效一个。statusline 类工具会改 `~/.claude/settings.json`，装之前先备份。第三方 hooks / MCP 会带权限与上下文成本，装前在 `/plugin` 里看「Will install」。

## Codex

本机扫描到的开发插件与启用配置见[同步记录](local-sync.md#codex)。浏览器、可视化等桌面运行时插件由宿主管理；缓存中的 Ponytail 4.10.0 未在当前配置中显式启用。

机制（见 [官方文档](https://developers.openai.com/codex/plugins)）：插件可打包 skills、MCP server、hooks。在 Codex CLI 里输入 `/plugins` 打开插件浏览器，或用命令行 `codex plugin add <插件>@<marketplace>`；第三方 marketplace 用 `codex plugin marketplace add owner/repo` 添加。官方 marketplace 名为 `openai-curated`，源码在 [openai/plugins](https://github.com/openai/plugins)。单个 skill 可在 Codex 里用 `$skill-installer <名称>` 从 [openai/skills](https://github.com/openai/skills) 安装；MCP 用 `codex mcp add`。插件装好后要新开会话才生效。IDE 扩展不支持插件。

| 插件 | 来源 | 说明 | 安装 |
|---|---|---|---|
| ★ `github` | [openai/plugins](https://github.com/openai/plugins/tree/main/plugins/github) | GitHub 仓库、Issue、PR 操作 | `/plugins` 或 `codex plugin add github@openai-curated` |
| ★ `superpowers` | [openai/plugins](https://github.com/openai/plugins/tree/main/plugins/superpowers) | obra/superpowers 工作流：头脑风暴、TDD、计划与审查 | `codex plugin add superpowers@openai-curated` |
| ★ `codex-security` | [openai/plugins](https://github.com/openai/plugins/tree/main/plugins/codex-security) | 扫描有授权的代码，确认漏洞并准备修复 | `codex plugin add codex-security@openai-curated` |
| `build-web-apps` | [openai/plugins](https://github.com/openai/plugins/tree/main/plugins/build-web-apps) | Web 应用的部署、UI、支付、数据库工作流 | `codex plugin add build-web-apps@openai-curated` |
| `coderabbit` | [openai/plugins](https://github.com/openai/plugins/tree/main/plugins/coderabbit) | CodeRabbit AI 代码审查 | `codex plugin add coderabbit@openai-curated` |
| `sentry` | [openai/plugins](https://github.com/openai/plugins/tree/main/plugins/sentry) | 查看报错与栈追踪 | `codex plugin add sentry@openai-curated` |
| `vercel` / `supabase` | [openai/plugins](https://github.com/openai/plugins/tree/main/plugins) | 部署平台 / 数据库开发（按技术栈选装） | `codex plugin add vercel@openai-curated` 等 |
| `figma` / `linear` / `notion` | [openai/plugins](https://github.com/openai/plugins/tree/main/plugins) | 设计稿、事务跟踪、文档知识库 | `codex plugin add figma@openai-curated` 等 |
| `plugin-eval` | [openai/plugins](https://github.com/openai/plugins/tree/main/plugins/plugin-eval) | 评测自己写的 Codex 插件 | `codex plugin add plugin-eval@openai-curated` |

> 用 API key 登录的 Codex 只能装一部分官方插件（有些插件需要 OAuth）。本仓库的 skills 也可以用 `npx skills add Zenty-Me/agent-dev-kit` 装进 Codex。

## Pi

当前使用的 **9 个包 + 1 个本地状态栏扩展**见 [Pi 插件快照与恢复](pi/README.md)：涵盖搜索、子代理、视觉、浏览器、上下文查看、渲染、Pi Switch 与 Ponytail，记录精确版本和 Git commit。

机制（见 [packages 文档](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/packages.md)；目录 [pi.dev/packages](https://pi.dev/packages)）：pi package 把 extensions、skills、prompt、themes 打成包。安装：`pi install npm:<包名>` / `pi install git:github.com/<owner>/<repo>`；`pi list` / `pi remove`；`-l` 写项目级 `.pi/settings.json`；`pi -e npm:<包名>` 仅本次试用。扩展会执行代码，装前看源码。

新版 Pi **已内置 MCP**（`pi mcp add`）；社区有人反馈可不再装 adapter。`pi-mcp-adapter` 仍是高下载路径，建议 **先试内置 MCP，复杂场景再 adapter，二者勿双开**。装 adapter 后跑 `/mcp-adapter setup`。更细说明见 [agents-learning/pi.md](../agents-learning/pi.md)。（X 社区增量核实：2026-10-14）

### 主生产力起步（核实：2026-10-14）

前置：Node **≥ 22.19**；`pi-browser-use` 需 Node **≥ 24** + Chrome。本体：`curl -fsSL https://pi.dev/install.sh | sh` → `pi` → `/login` → `/model`。快捷键与 `/compact` 等见 [agents-learning/pi.md](../agents-learning/pi.md)。

| 档位 | 包 | 说明 | 安装 |
|---|---|---|---|
| 核心可选 | [pi-mcp-adapter](https://pi.dev/packages/pi-mcp-adapter) | 复杂 MCP 场景；新版可先试**内置 MCP**，需要再装（与内置 / `pi-mcp-extension` 勿双开） | `pi install npm:pi-mcp-adapter` 后 `/mcp-adapter setup` |
| ★ 核心 | [pi-web-access](https://www.npmjs.com/package/pi-web-access) | 搜索、抓页、clone GitHub、PDF/YouTube；Exa 可无 key | `pi install npm:pi-web-access` |
| ★ 核心 | [pi-subagents](https://www.npmjs.com/package/pi-subagents) | 子代理委派；复杂任务拆开做；规划/执行分模型靠 frontmatter `model`/`thinking`（无 opusplan）见 [pi.md](../agents-learning/pi.md) | `pi install npm:pi-subagents` |
| 全栈 | [pi-browser-use](https://www.npmjs.com/package/pi-browser-use) | Chrome DevTools MCP 浏览器自动化（需 Node ≥24 + Chrome） | `pi install npm:pi-browser-use` |
| 全栈 | [pi-vision-handoff](https://www.npmjs.com/package/pi-vision-handoff) | 无视觉模型时：用视觉模型描述截图/设计稿再交回 | `pi install npm:pi-vision-handoff` |
| 全栈 | [pi-lens](https://www.npmjs.com/package/pi-lens) | 边写边验（LSP/lint/类型/格式化回灌）；符号搜索、`/lens-map`；约 20MB+ 可能拖启动；**项目级 `-l`，勿全局常开** | `pi install -l npm:pi-lens` |
| 全栈备选 | [@mrclrchtr/supi-code-intelligence](https://www.npmjs.com/package/@mrclrchtr/supi-code-intelligence) | LSP + AST 导航/诊断/重构（与 pi-lens 二选一即可） | `pi install npm:@mrclrchtr/supi-code-intelligence` |
| 长会话推荐（按需） | [billion-context](https://www.npmjs.com/package/billion-context) / [billion-context-pi](https://www.npmjs.com/package/billion-context-pi) | 上下文压缩（月下载高）；社区有反馈长会话仍会忘，**优先试内置 `/compact`** | `pi install npm:billion-context` 或 `billion-context-pi` |

更完整的分层 / 省上下文 / 演进 / 操作速记见 [agents-learning/pi.md](../agents-learning/pi.md)（使用手册总稿）。
>
> **社区常驻做减法（X，约 2026-10-09～10-14）：** 小墨常驻约三件套 `pi-cc-extensions` / `pi-web-access` / `pi-context-view`；也可只锁后两者。`pi-lens` 建议 **项目级** `pi install -l npm:pi-lens`，别全局常开。长会话优先内置 `/compact`；`billion-context` / SoL-Pi 等按需。经验详 [pi.md](../agents-learning/pi.md)。
>
> 日常够用 = web +（内置 MCP 或 adapter 二选一）+ subagents。全栈再加 browser/chrome +（lens 项目级）+ 按需 vision。别一口气堆包。
>
> **勿双开：** 内置 MCP ↔ `pi-mcp-adapter` ↔ `pi-mcp-extension`；`pi-subagents` ↔ `@tintinweb/pi-subagents`；`pi-browser-use` ↔ `pi-chrome`（按场景选：隔离自动化 vs 已登录日常 Chrome）。

配置落点：`~/.pi/agent/`（项目用 `.pi/`）— `settings.json`、`mcp.json`、`APPEND_SYSTEM.md`；仓根 `AGENTS.md`；可选 `~/.pi/web-search.json`。用 `pi config` 开关扩展。模板要点见 [pi.md](../agents-learning/pi.md)。

**终端渲染 / pi-lens：** 默认渲染够用；要更好看装 `pi-code-render` + `pi-better-render`（可选 `pi-agent-extensions`）。`typebox` 警告多来自旧版 `pi-browser-use`，与渲染无关。`pi-lens` 边写边验、务必项目级 `-l`，约 20MB+ 可能拖启动。可粘贴提示词与细节见 [pi.md](../agents-learning/pi.md)「终端渲染」「全栈加装」。

### 第二档：按需体验（别进核心）

| 包 | 说明 | 安装 |
|---|---|---|
| [pi-context-view](https://www.npmjs.com/package/pi-context-view) | 看清上下文占用（含隐藏的 base prompt / tools / 扩展注入）；社区常驻推荐 | `pi install npm:pi-context-view` |
| [pi-chrome](https://www.npmjs.com/package/pi-chrome) | 经授权使用本机已登录 Chrome（与 `pi-browser-use` 按场景二选一） | `pi install npm:pi-chrome` |
| [pi-agents](https://www.npmjs.com/package/pi-agents) | 基于 pi-durable 的持久命名子代理 / 图编排 | `pi install npm:pi-agents` |
| [pi-gpt-search](https://www.npmjs.com/package/pi-gpt-search) | 借 Codex 独立搜索，省 GPT token | `pi install npm:pi-gpt-search` |
| [pi-file-preview](https://www.npmjs.com/package/pi-file-preview) | TUI 点文件链接预览（含 :line）；Quick Open | `pi install npm:pi-file-preview` |
| [pi-minimal-footer](https://www.npmjs.com/package/pi-minimal-footer) | 极简一行 footer（用量 / 路径 / 模型 / 上下文） | `pi install npm:pi-minimal-footer` |
| [layermap](https://www.npmjs.com/package/layermap) | 代码分层地图：目录 / 模块 / 调用链与改动影响面 | `pi install npm:layermap` |
| [pi-cc-extensions](https://www.npmjs.com/package/pi-cc-extensions) | Claude Code 风格 TUI 输出与实用小工具（社区常驻可选） | `pi install npm:pi-cc-extensions` |
| [pi-memory](https://www.npmjs.com/package/pi-memory) | 跨会话记忆（daily / 长期 / scratchpad） | `pi install npm:pi-memory` |
| [@narumitw/pi-plan-mode](https://www.npmjs.com/package/@narumitw/pi-plan-mode) 或 [@hank-warren/pi-plan-mode](https://www.npmjs.com/package/@hank-warren/pi-plan-mode) | 只读规划模式（二选一） | `pi install npm:@narumitw/pi-plan-mode` |
| [@juicesharp/rpiv-todo](https://www.npmjs.com/package/@juicesharp/rpiv-todo) + [rpiv-ask-user-question](https://www.npmjs.com/package/@juicesharp/rpiv-ask-user-question) | todo 浮层 + 结构化追问 | 见下表安装命令 |
| [pi-background-tasks](https://www.npmjs.com/package/pi-background-tasks) | 长跑 shell / 后台委派 | `pi install npm:pi-background-tasks` |
| [@gotgenes/pi-permission-system](https://www.npmjs.com/package/@gotgenes/pi-permission-system) | 工具调用权限闸 | `pi install npm:@gotgenes/pi-permission-system` |
| [pi-agent-extensions](https://www.npmjs.com/package/pi-agent-extensions) | 界面扩展合集 + 主题；`/settings` 选 Theme，主题也可放 `~/.pi/agent/themes/` | `pi install npm:pi-agent-extensions` |
| [pi-long-task](https://www.npmjs.com/package/pi-long-task) / [pi.dev 文档](https://pi.dev/packages/pi-long-task) | 长任务：拆 TODO、子会话执行、TUI 进度；自然语言 *Run a long task…*；自主迭代见 [autonomous-iteration.md](../agents-learning/autonomous-iteration.md) | `pi install npm:pi-long-task` |
| [pi-async-compaction](https://www.npmjs.com/package/pi-async-compaction) | 长会话后台异步压缩摘要（可选） | `pi install npm:pi-async-compaction` |
| [pi-longrun](https://www.npmjs.com/package/pi-longrun) | 后台任务与定时唤醒（可选） | `pi install npm:pi-longrun` |
| [pi-code-render](https://www.npmjs.com/package/pi-code-render) | 代码块卡片 + 一键复制 | `pi install npm:pi-code-render` |
| [pi-better-render](https://www.npmjs.com/package/pi-better-render) | Markdown/表格/公式图（公式图建议 Ghostty/Kitty/WezTerm；不进上下文） | `pi install npm:pi-better-render` |
| [pi-automode-classifier](https://www.npmjs.com/package/pi-automode-classifier) | Auto mode：危险命令分级确认 | `pi install npm:pi-automode-classifier` |
| [sol-pi](https://www.npmjs.com/package/sol-pi) / [@herbertgao/sol-pi](https://www.npmjs.com/package/@herbertgao/sol-pi) | 省上下文类扩展（社区常称 SoL-Pi） | `pi install npm:sol-pi` 等 |

### 其他常用包

| 包 | 来源 | 说明 | 安装 |
|---|---|---|---|
| pi-powerline-footer | [nicobailon/pi-powerline-footer](https://github.com/nicobailon/pi-powerline-footer) | powerline 风格状态栏 | `pi install npm:pi-powerline-footer` |
| plannotator（Pi 扩展） | [backnotprop/plannotator](https://github.com/backnotprop/plannotator) | 计划审阅与批注；`--plan` 或 `/plannotator-plan-mode` | `pi install npm:@plannotator/pi-extension` |
| rpiv-todo | [juicesharp/rpiv-mono](https://github.com/juicesharp/rpiv-mono) | 模型用 todo，实时浮层，`/reload` 后仍保留 | `pi install npm:@juicesharp/rpiv-todo` |
| rpiv-ask-user-question | [juicesharp/rpiv-mono](https://github.com/juicesharp/rpiv-mono) | 需要澄清时弹出结构化问卷 | `pi install npm:@juicesharp/rpiv-ask-user-question` |
| pi-btw | [dbachelder/pi-btw](https://github.com/dbachelder/pi-btw) | `/btw` 旁支对话，不打断主任务 | `pi install npm:pi-btw` |
| pi-fff | [dmtrKovalenko/fff](https://github.com/dmtrKovalenko/fff) | FFF 模糊文件与内容搜索 | `pi install npm:@ff-labs/pi-fff` |
| pi-observability-plugin | [langfuse/pi-observability-plugin](https://github.com/langfuse/pi-observability-plugin) | 追踪到 Langfuse | `pi install npm:@langfuse/pi-observability-plugin` |
| LangSmith | npm `@langchain/langsmith-pi-extension` | 会话 / 轮次 / 工具追踪到 LangSmith | `pi install npm:@langchain/langsmith-pi-extension` |
| Braintrust | npm `@braintrust/pi-extension` | 自动 tracing 到 Braintrust | `pi install npm:@braintrust/pi-extension` |
| pi-mcp-extension | npm `pi-mcp-extension` | 另一路 MCP client（**与 `pi-mcp-adapter` 二选一，勿双开**） | `pi install npm:pi-mcp-extension` |
| @tintinweb/pi-subagents | npm `@tintinweb/pi-subagents` | Claude Code 风格子代理 UI（**与 `pi-subagents` 二选一，勿双开**） | `pi install npm:@tintinweb/pi-subagents` |

## Cursor

机制（见 [Cursor Plugins 文档](https://cursor.com/docs/plugins)）：插件可打包 rules、skills、agents、commands、MCP、hooks；同时支持 Cursor Plugin（`.cursor-plugin/plugin.json`）和开放标准 Agent Plugin（根目录 `plugin.json`）。安装方式：侧栏 **Customize** → 找到插件 → **Install**，选项目或用户范围；官方插件在 [cursor.com/marketplace](https://cursor.com/marketplace)，社区插件和 MCP 见 [cursor.directory](https://cursor.directory)。官方插件源码在 [cursor/plugins](https://github.com/cursor/plugins)。

| 插件 | 来源 | 说明 | 安装 |
|---|---|---|---|
| ★ `continual-learning` | [cursor/plugins](https://github.com/cursor/plugins/tree/main/continual-learning) | 从对话记录中提取要点，增量更新 AGENTS.md 作为记忆 | Customize / Marketplace 搜索安装 |
| ★ `thermos` | [cursor/plugins](https://github.com/cursor/plugins/tree/main/thermos) | 深度分支审查：安全和正确性审计、并行子 agent、产出可合并的 PR | 同上 |
| `pr-review-canvas` | [cursor/plugins](https://github.com/cursor/plugins/tree/main/pr-review-canvas) | 把 PR diff 按重要性分组展示成审查画布 | 同上 |
| `advisor` | [cursor/plugins](https://github.com/cursor/plugins/tree/main/advisor) | 做重大决策、卡住或准备收尾时，先咨询更强的模型 | 同上 |
| `orchestrate` | [cursor/plugins](https://github.com/cursor/plugins/tree/main/orchestrate) | 把大任务拆给多个并行云端 agent（规划、执行、校验） | 同上 |
| `agent-compatibility` | [cursor/plugins](https://github.com/cursor/plugins/tree/main/agent-compatibility) | 扫描仓库对 agent 是否友好，核对启动、校验、文档 | 同上 |
| `ralph-loop` | [cursor/plugins](https://github.com/cursor/plugins/tree/main/ralph-loop) | 用同一提示循环迭代直到完成（Ralph Wiggum 技法）；见 [autonomous-iteration.md](../agents-learning/autonomous-iteration.md) | 同上 |
| `github` / `playwright` | [cursor/plugins](https://github.com/cursor/plugins/tree/main/third_party) | GitHub 仓库/PR/Actions；真实浏览器操作与测试 | 同上 |
| `create-plugin` | [cursor/plugins](https://github.com/cursor/plugins/tree/main/create-plugin) | 生成并校验新插件的骨架 | 同上 |

> 本仓库 skills 可用 `npx skills add Zenty-Me/agent-dev-kit` 装进 Cursor。

## Gemini CLI

机制（见 [extensions 文档](https://github.com/google-gemini/gemini-cli/blob/main/docs/extensions/index.md)）：extension 带有 `gemini-extension.json`，可以打包 MCP、上下文文件、自定义命令。安装：`gemini extensions install <GitHub URL>`，`gemini extensions list` 查看。

| 扩展 | 来源 | 说明 | 安装 |
|---|---|---|---|
| ★ conductor | [gemini-cli-extensions/conductor](https://github.com/gemini-cli-extensions/conductor) | Context-Driven Development：先写规格和计划，再实现 | `gemini extensions install https://github.com/gemini-cli-extensions/conductor` |
| ★ security | [gemini-cli-extensions/security](https://github.com/gemini-cli-extensions/security) | 对代码改动做安全分析 | `gemini extensions install https://github.com/gemini-cli-extensions/security` |
| workspace | [gemini-cli-extensions/workspace](https://github.com/gemini-cli-extensions/workspace) | Google Workspace：Docs、Sheets、Gmail、Calendar 等 | `gemini extensions install https://github.com/gemini-cli-extensions/workspace` |
| chrome-devtools-mcp | [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) | 通过 Chrome DevTools 调试页面、看性能和网络请求 | `gemini extensions install https://github.com/ChromeDevTools/chrome-devtools-mcp` |
| context7 | [upstash/context7](https://github.com/upstash/context7) | 查询最新的库文档 | `gemini extensions install https://github.com/upstash/context7` |
| jules | [gemini-cli-extensions/jules](https://github.com/gemini-cli-extensions/jules) | 把任务交给 Jules 异步执行 | `gemini extensions install https://github.com/gemini-cli-extensions/jules` |
| nanobanana | [gemini-cli-extensions/nanobanana](https://github.com/gemini-cli-extensions/nanobanana) | 图片生成和编辑 | `gemini extensions install https://github.com/gemini-cli-extensions/nanobanana` |

## OpenCode

机制（见 [OpenCode plugins 文档](https://opencode.ai/docs/plugins)）：npm 插件写进 `opencode.json` 的 `"plugin": ["<包名>"]`，启动时自动安装；本地插件放在 `.opencode/plugins/`（项目级）或 `~/.config/opencode/plugins/`（全局）。社区插件列表见 [ecosystem](https://opencode.ai/docs/ecosystem#plugins)。

| 插件 | 来源 | 说明 | 安装（加进 `opencode.json` 的 `plugin`） |
|---|---|---|---|
| ★ opencode-dynamic-context-pruning | [Tarquinen/opencode-dynamic-context-pruning](https://github.com/Tarquinen/opencode-dynamic-context-pruning) | 清理已过时的工具输出，减少上下文 token | `"@tarquinen/opencode-dcp"` |
| ★ opencode-supermemory | [supermemoryai/opencode-supermemory](https://github.com/supermemoryai/opencode-supermemory) | 基于 Supermemory 的持久记忆 | `"opencode-supermemory"` |
| magic-context | [cortexkit/magic-context](https://github.com/cortexkit/magic-context) | 跨会话记忆与上下文管理 | `"@cortexkit/opencode-magic-context"` |
| opencode-pty | [shekohex/opencode-pty](https://github.com/shekohex/opencode-pty) | 交互式 PTY：跑后台进程，并向它发送输入 | `"opencode-pty"` |
| opencode-observability-plugin | [langfuse/opencode-observability-plugin](https://github.com/langfuse/opencode-observability-plugin) | 把会话遥测发到 Langfuse | `"@langfuse/opencode-observability-plugin"` |

## 跨 agent 通用工具

同时支持多种 agent 的工具，按各自 README 的说明标出支持范围。跨 harness 互调（CLI / MCP / 桥）见 [cross-agent.md](../agents-learning/cross-agent.md)。

| 工具 | 来源 | 支持的 agent | 说明 | 安装 |
|---|---|---|---|---|
| ★ claude-mem | [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | Claude Code、Codex、Gemini、OpenCode、Hermes、Copilot 等 | 跨会话记忆：记录会话、压缩后在之后的会话里注入相关上下文 | `npx claude-mem install`（其他 agent 加 `--ide <name>`） |
| ★ claude-squad | [smtg-ai/claude-squad](https://github.com/smtg-ai/claude-squad) | Claude Code、Codex、OpenCode、Amp | 在 TUI 里管理多个 agent 会话，每个任务一个 git worktree | `brew install claude-squad`，运行 `cs` |
| agent-notifications | [777genius/agent-notifications](https://github.com/777genius/agent-notifications) | Claude、Codex、OpenCode、Gemini CLI | 任务完成或需要确认时发桌面通知、声音或 webhook | `curl -fsSL https://agent-notifications.com/install.sh \| bash` |
| ccmanager | [kbwo/ccmanager](https://github.com/kbwo/ccmanager) | Claude Code、Gemini CLI、Codex、Cursor Agent、Copilot CLI、Cline、OpenCode、Kimi | 多会话与 worktree 管理器 | `npx ccmanager` |
| CloudCLI（Claude Code UI） | [siteboon/claudecodeui](https://github.com/siteboon/claudecodeui) | Claude Code、OpenCode、Cursor CLI、Codex | 在网页或手机上远程管理会话 | `npx @cloudcli-ai/cloudcli` |
| cc-safety-net | [kenryu42/cc-safety-net](https://github.com/kenryu42/cc-safety-net) | Claude Code、Codex、Gemini CLI 等 | hook：拦截破坏性命令和对密钥文件的读取 | 见 [安装文档](https://ccsafetynet.com/docs/installation) |
| plannotator | [backnotprop/plannotator](https://github.com/backnotprop/plannotator) | Claude Code、Codex、Pi | 交互式审阅、批注计划 | Claude Code：`/plugin marketplace add backnotprop/plannotator` → `/plugin install plannotator@plannotator`；其他见 README |

## 更多 skill 来源

本仓库的 `skills/` 主要服务 Claude Code 插件市场，但不少 skill 也兼容 Codex / Cursor（`npx skills add` 等）。不必硬塞进本仓库结构的来源可记在这里：

| 来源 | 适用 | 备注 |
|---|---|---|
| [openai/skills](https://github.com/openai/skills) | Codex 等 | 官方 Codex skills 目录；本仓库已收录其 security 相关 skill |
| [composio-community/awesome-codex-skills](https://github.com/composio-community/awesome-codex-skills) | Codex | 实用 Codex skills 精选列表 |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | 多 harness | React/Web 性能与设计；本仓库已收录多条 |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | 多 harness | 生产级工程技能；本仓库已收录 TDD / 简化等 |
| [obra/superpowers](https://github.com/obra/superpowers) | Claude Code / 多 | 也可作为 `superpowers@claude-plugins-official` 安装 |
| [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code)（ECC） | Claude Code | 大而全 agents/skills/hooks/MCP 合集；按需装，别一次全开 |
| [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | 多 | 社区 agent skills 大合集，挑选时注意质量 |

更细的安装笔记见 [agents-learning/claude-code.md](../agents-learning/claude-code.md)。
