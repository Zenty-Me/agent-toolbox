# Agent Dev Kit

AI 协同开发工具箱：精选 Claude Code / Pi / Codex 通用开发 skills、实用插件与可复用提示词，以及 AI 编码工具的使用笔记。

> 仓库由 `skills-prompts` 更名为 `agent-dev-kit`；GitHub 会对旧路径做重定向，新安装请用下方命令。

| 目录 | 内容 |
|---|---|
| **skills/** | 从各官方仓库精选的开发类 skill，可通过 Claude Code 插件市场一键安装 |
| **plugins/** | 各 agent 的插件推荐、本机版本清单与 Pi 本地扩展源码快照 |
| **prompts/** | 可直接当系统提示词使用的角色提示词 |
| **agents-learning/** | Claude Code、Pi、Hermes 等工具的使用笔记 |

## 项目结构

```
agent-dev-kit/
├── .claude-plugin/
│   └── marketplace.json   # Claude Code 插件市场配置（按用途分成 7 个插件）
├── skills/                # 通用开发 skill 定义（每个目录一个 skill）
├── plugins/
│   ├── README.md          # 各 agent 插件推荐与安装方式
│   ├── installed.json     # 本机 Pi / Claude Code / Codex 开发插件版本与来源
│   ├── local-sync.md      # 本次扫描、版本比较与 skill 同步记录
│   └── pi/               # Pi 恢复说明、Pi Switch 与本地状态栏源码
├── prompts/               # 提示词模板
├── agents-learning/       # AI 编码工具使用笔记
├── scripts/
│   ├── sync-skills.sh         # 从本机同步 skill 到仓库
│   └── check-consistency.sh   # skills ≡ marketplace ≡ README 校验
└── LICENSE                # 本仓库原创内容（skills 仍归各自上游）
```

## 安装 Skills

### 方式一：Claude Code 插件市场（推荐）

```bash
/plugin marketplace add Zenty-Me/agent-dev-kit
```

然后按需安装插件（marketplace 名为 `agent-dev-kit`）：

| 插件 | 包含的 skill |
|---|---|
| `coding-standards@agent-dev-kit` | karpathy-guidelines、clean-code、humanizer、concept-first-tutorial |
| `code-quality@agent-dev-kit` | code-reviewer、refactor-advisor、security-best-practices、security-threat-model、code-simplification、test-driven-development、systematic-debugging |
| `planning@agent-dev-kit` | brainstorming、grill-me、grilling、drawio-skill |
| `frontend@agent-dev-kit` | frontend-design、nextjs、vercel-react-best-practices、vercel-composition-patterns、web-design-guidelines、vercel-react-view-transitions |
| `backend@agent-dev-kit` | supabase、supabase-postgres-best-practices、python-performance-optimization |
| `skill-dev@agent-dev-kit` | skill-creator、mcp-builder、find-skills |
| `ponytail-skills@agent-dev-kit` | ponytail、ponytail-review、ponytail-audit、ponytail-debt、ponytail-gain、ponytail-help |

```bash
/plugin install frontend@agent-dev-kit
```

更新：`/plugin marketplace update agent-dev-kit`。

`ponytail-skills` 提供 Ponytail 5.3.3 的六个技能。自动启用、状态栏与 hooks 由 [Ponytail 原插件](https://github.com/DietrichGebert/ponytail) 提供；已装原插件时避免重复安装同名 skills。

### 方式二：skills CLI

支持 Pi、Claude Code、Codex、Cursor 等多种 AI 工具：

```bash
npx skills add Zenty-Me/agent-dev-kit                      # 交互式选择
npx skills add Zenty-Me/agent-dev-kit -s karpathy-guidelines -g   # 全局安装单个 skill
```

### 方式三：手动复制

把 `skills/` 下需要的目录复制到 `~/.agents/skills/`（Pi 等支持的共享目录）、`~/.claude/skills/` 或 `~/.codex/skills/`。也可以放到项目中对应的 skills 目录；按需挑选，避免与已安装插件里的同名 skill 重复。

## Skills 列表

| 分类 | Skill | 说明 | 来源 |
|---|---|---|---|
| 编码与写作准则 | `karpathy-guidelines` | 基于 Andrej Karpathy 观察总结的 LLM 编码行为准则 | forrestchang/andrej-karpathy-skills |
| | `clean-code` | 简洁直接的编码规范，不过度设计 | vudovn/ag-kit |
| | `humanizer` | 去掉文字里的 AI 腔，读起来像本人写的，不改变原意 | blader/humanizer |
| | `concept-first-tutorial` | 用解释、小例子与最小代码编写技术教程 | 本机 Codex 自定义 skill |
| 代码质量 | `code-reviewer` | 关注安全、性能和最佳实践的代码审查 | awesome-llm-apps（Shubhamsaboo 等） |
| | `refactor-advisor` | 识别代码坏味道并给出重构方案 | 本仓库原创 |
| | `security-best-practices` | 按语言和框架做安全最佳实践审查 | openai/skills |
| | `security-threat-model` | 基于仓库证据的威胁建模（信任边界、滥用路径、缓解） | openai/skills |
| | `code-simplification` | 在不改变行为的前提下简化代码、提升可读性 | addyosmani/agent-skills |
| | `test-driven-development` | 红绿重构驱动开发与缺陷修复 | addyosmani/agent-skills |
| | `systematic-debugging` | 先根因再修复的系统化调试流程 | obra/superpowers |
| 设计与规划 | `brainstorming` | 动手前的头脑风暴与需求澄清 | obra/superpowers |
| | `grill-me` | 手动触发入口（`/grill-me`）；内部调用 `grilling` | mattpocock/skills |
| | `grilling` | 按设计树多轮追问，打磨方案或决策 | mattpocock/skills |
| | `drawio-skill` | 生成可编辑的 draw.io 架构图、UML、ERD、时序图 | Agents365-ai/drawio-skill |
| 前端 | `frontend-design` | 有辨识度的前端视觉设计 | anthropics/skills |
| | `nextjs` | Next.js App Router 开发指导（含本地 overlay） | openai/plugins（vercel/nextjs） |
| | `vercel-react-best-practices` | Vercel 的 React/Next.js 性能优化指南 | vercel-labs/agent-skills |
| | `vercel-composition-patterns` | React 组件组合模式 | vercel-labs/agent-skills |
| | `web-design-guidelines` | 按 Web Interface Guidelines 审查 UI/可访问性/UX | vercel-labs/agent-skills |
| | `vercel-react-view-transitions` | React View Transition API 与路由/共享元素动画 | vercel-labs/agent-skills |
| 后端与数据库 | `supabase` | Supabase 开发 | supabase/agent-skills |
| | `supabase-postgres-best-practices` | Postgres 最佳实践 | supabase/agent-skills |
| | `python-performance-optimization` | Python 性能分析与优化 | wshobson/agents |
| Skill 开发 | `skill-creator` | 创建、改进、评测 skill | anthropics/skills |
| | `mcp-builder` | 设计并实现高质量 MCP server（Python/TS） | anthropics/skills |
| | `find-skills` | 查找并安装可复用的 agent skills | vercel-labs/skills |
| 最小实现与审查 | `ponytail` | 用最小完整改动完成开发任务 | DietrichGebert/ponytail 5.3.3 |
| | `ponytail-review` | 审查变更的正确性、安全、负载与代码精简空间 | DietrichGebert/ponytail 5.3.3 |
| | `ponytail-audit` | 按风险审计整个仓库 | DietrichGebert/ponytail 5.3.3 |
| | `ponytail-debt` | 汇总 shortcut / ponytail 注释中的技术债 | DietrichGebert/ponytail 5.3.3 |
| | `ponytail-gain` | 展示上游发布的基准测试结果 | DietrichGebert/ponytail 5.3.3 |
| | `ponytail-help` | 模式、技能与命令速查 | DietrichGebert/ponytail 5.3.3 |

**版权与许可证**

- 根目录 [LICENSE](LICENSE)（MIT）覆盖本仓库**原创**内容：`README`、`prompts/`、`plugins/`、`scripts/`、marketplace 配置，以及本仓库原创 skill（如 `refactor-advisor`）。
- `skills/` 下各 skill **版权归原作者**；许可证以各目录 `LICENSE` / `LICENSE.txt` 为准，并参考 `SKILL.md` 的 `license` 字段。收录与再分发请遵守对应上游条款；本机安装未附许可证的项目在[同步记录](plugins/local-sync.md)中注明。
- 已去掉与 `vercel-react-best-practices` 重复的旧 `react-best-practices` 打包；前端性能规则以 Vercel 官方 skill 为准。

## Prompts

可直接作为系统提示词或对话开头使用，适用于 Claude、ChatGPT、Cursor 等助手。下列为仓库精选角色/任务提示词（原创表述，面向开发与生产力场景）。

| 提示词 | 说明 |
|---|---|
| [AI协同开发架构师与提示词工程专家](prompts/AI协同开发架构师与提示词工程专家.md) | 软件全生命周期的 AI 协同开发，生成开发级提示词指导编码助手落地 |
| [OCR 与排版专家](prompts/OCR%20与排版专家.md) | 图片转结构化 Markdown，支持数学公式 LaTeX |
| [项目注释](prompts/项目注释.md) | 为现有项目就地补文档注释与行内解释，不改业务逻辑 |
| [代码审查专家](prompts/代码审查专家.md) | 结构化审查 PR/模块：正确性、安全、性能、可维护性 |
| [系统架构师](prompts/系统架构师.md) | 澄清需求、划边界、给可落地架构方案与权衡 |
| [调试专家](prompts/调试专家.md) | 先根因后修复的系统化调试流程 |
| [重构顾问](prompts/重构顾问.md) | 行为不变的小步重构计划与风险控制 |
| [安全审计专家](prompts/安全审计专家.md) | 应用安全审查：威胁、评级与可落地修复建议 |
| [资深前端工程师](prompts/资深前端工程师.md) | React/Next 等实现与评审：状态、性能、a11y |
| [SQL与数据建模专家](prompts/SQL与数据建模专家.md) | 表结构设计、SQL 编写与优化、迁移注意点 |
| [API与后端设计专家](prompts/API与后端设计专家.md) | HTTP/RPC 契约、错误/分页/鉴权与兼容演进 |
| [CI与CD流水线顾问](prompts/CI与CD流水线顾问.md) | GitHub Actions 等：测试门禁、构建发布与可维护 CI |
| [Git提交与PR助手](prompts/Git提交与PR助手.md) | 整理 commit message、PR 正文与拆分建议 |
| [技术写作专家](prompts/技术写作专家.md) | README / 设计文档 / API 说明等清晰可执行文稿 |
| [产品经理](prompts/产品经理.md) | 用户故事、验收标准、优先级与迭代规格 |
| [数据分析师](prompts/数据分析师.md) | 指标口径、分析路径与可执行结论 |
| [中英翻译与润色](prompts/中英翻译与润色.md) | 中英互译与同语言润色，默认不改变原意 |
| [面试辅导教练](prompts/面试辅导教练.md) | 模拟面试、追问点评与示范答法 |
| [学习教练](prompts/学习教练.md) | 学习路径、理解检验与练习闭环 |



## Plugins

[plugins/README.md](plugins/README.md) 按 agent 分区，收录 **Claude Code、Codex、Pi、Cursor、Gemini CLI、OpenCode** 的插件和扩展。每个分区写明该 agent 的扩展机制、推荐条目和安装命令；另有一节支持多种 agent 的通用工具（记忆、通知、多会话管理）。

当前本机扫描见[同步记录](plugins/local-sync.md)与[版本清单](plugins/installed.json)。[Pi 插件恢复说明](plugins/pi/README.md)记录 9 个包的精确版本、安装来源，并保存 Pi Switch 与 compact-status 的源码快照。

## 使用笔记

- [Claude Code](agents-learning/claude-code.md)：优先用本仓库 / 官方 marketplace 安装；附 `opusplan` / 子代理 model / `/advisor`、[子 agent 配置](agents-learning/claude-code.md#子-agent-配置)
- [Pi](agents-learning/pi.md)：使用手册 / 总稿（分层、省上下文、核心包、终端渲染、全栈加装、规划/执行分模型、[子 agent 配置](agents-learning/pi.md#子-agent-配置)）
- [Pi 自助 bootstrap](agents-learning/pi-bootstrap.md)：可直接丢给 Pi 的安装配置提示词
- [AGENTS.md / CLAUDE.md 写法](agents-learning/project-instructions.md)：短硬可验证的项目指令文件
- [自主持续迭代](agents-learning/autonomous-iteration.md)：可验证终点 + 落盘状态 + 循环（Pi goal / circadian、Claude Ralph）
- [跨 agent 调用](agents-learning/cross-agent.md)：跨 harness 把对方包成工具（CLI / MCP / 桥）
- [Hermes](agents-learning/hermes.md)：常用命令（模型配置、会话管理）

## 维护

更新本机 skill 后同步到仓库：

```bash
npx skills update -g -y            # 从官方源更新本机 skill
./scripts/sync-skills.sh           # 默认读取 ~/.claude/skills
SKILLS_DIR="$HOME/.agents/skills" ./scripts/sync-skills.sh grilling  # Pi 共享目录
SKILLS_DIR="$HOME/.codex/skills" ./scripts/sync-skills.sh concept-first-tutorial
```

`sync-skills.sh` **只复制**选定来源目录里的内容，优先使用 `SKILLS_DIR`，兼容旧的 `CLAUDE_SKILLS_DIR`，默认 `~/.claude/skills`。执行前先核对来源版本与 diff；不同宿主可能保留较旧版本、同名不同实现或本地修复，不应整库覆盖。新增或下线 skill 时，还须**手动**更新：

1. `.claude-plugin/marketplace.json` 对应插件的 `skills` 列表
2. 上文「安装 Skills」插件表与「Skills 列表」
3. 各 skill 目录下的 `LICENSE`（从上游同步）

然后跑一致性检查：

```bash
./scripts/check-consistency.sh
```

CI：push 到 main 或提 PR 时，[.github/workflows/check-consistency.yml](.github/workflows/check-consistency.yml) 会自动跑该检查。
