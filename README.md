# Agent Dev Kit

按 **Pi、Claude Code、Codex** 分区维护的个人能力同步库，保留跨项目可复用的开发和日常使用插件、skills、提示词与使用笔记。各 agent 可以重复收录同一能力，并独立记录版本和安装方式。

仓库原名 `skills-prompts`，GitHub 会重定向旧地址；新安装使用 `Zenty-Me/agent-dev-kit`。

## 按 agent 使用

| Agent | 能力入口 | 插件来源与版本 | Skills |
|---|---|---|---|
| Pi | [pi/README.md](pi/README.md) | [pi/plugins.json](pi/plugins.json)：9 个包、1 个本地扩展 | 33 个 |
| Claude Code | [claude-code/README.md](claude-code/README.md) | [claude-code/plugins.json](claude-code/plugins.json)：18 个安装记录 | 33 个 |
| Codex | [codex/README.md](codex/README.md) | [codex/plugins.json](codex/plugins.json)：16 个开发与日常插件记录 | 33 个 |

Ponytail 全套六个 skills、grill-me / grilling、技术教程、写作和日常提示词都保留。Pi 专用插件和 Next.js / Supabase 等技术栈能力也可以收录，不要求每个能力支持所有宿主。飞书、业务项目资料、账户凭据与会话历史不在同步范围。

## 项目结构

```text
agent-dev-kit/
├── pi/
│   ├── README.md
│   ├── plugins.json
│   ├── package.json        # 本地 Pi skills 包
│   ├── skills/
│   └── extensions/compact-status/
├── claude-code/
│   ├── README.md
│   ├── plugins.json
│   └── skills/
├── codex/
│   ├── README.md
│   ├── plugins.json
│   └── skills/
├── .claude-plugin/marketplace.json
├── prompts/
├── agents-learning/
├── plugins/                # 参考目录、完整性检查与历史记录
└── scripts/                # 预览、双向同步与一致性校验
```

三个 skills 目录都是独立文件，不使用跨分区符号链接。插件优先记录项目地址和安装方式；[Pi Switch](https://github.com/Zenty-Me/pi-switch) 在自己的仓库维护源码，本库不保留其完整工作副本。

## 快速安装

在仓库根目录安装 Pi 的技能包：

```bash
pi install ./pi
```

Claude Code 使用原有 marketplace 和插件组名称，安装路径已切换到 Claude Code 分区：

```text
/plugin marketplace add Zenty-Me/agent-dev-kit
/plugin install planning@agent-dev-kit
/plugin install ponytail-skills@agent-dev-kit
```

Codex 可预览并复制选定技能；执行时加 `--apply`：

```bash
python scripts/sync_skills.py codex export grill-me grilling
python scripts/sync_skills.py codex export grill-me grilling --apply
```

每个分区的完整安装方式、插件清单和技能来源见其 README。插件自带技能与本库的独立副本可按需选用，同一宿主避免重复加载。

## 补齐与同步

维护顺序是：**核对官方来源 → 补齐本地缺失文件 → 预览差异 → 同步对应 agent → 校验 → 提交推送**。本次已执行的来源核对与本地补齐见[完整性记录](plugins/completeness.md)及[机器可读报告](plugins/completeness.json)。

同步脚本只依赖 Python 3.10+，Windows 使用 `python`，macOS / Linux 可使用 `python3`。必须显式选择 agent 与方向：

```bash
# 本机 → 仓库，默认只预览
python scripts/sync_skills.py pi import grilling

# 明确写入
python scripts/sync_skills.py pi import grilling --apply

# 仓库 → 本机
python scripts/sync_skills.py codex export grill-me grilling --apply

# 指定本地目录
python scripts/sync_skills.py claude-code import grilling --skills-dir /path/to/local/skills
```

默认本地目录分别为 `~/.agents/skills`、`~/.claude/skills`、`~/.codex/skills`。可用 `--skills-dir` 或 `SKILLS_DIR` 覆盖；Claude Code 兼容旧的 `CLAUDE_SKILLS_DIR`。

不同内容会作为冲突拒绝写入；审阅后才加 `--replace --apply`。脚本保留目标独有文件，包括 LICENSE 和本地附加资源；不自动删除、不比较版本号，也不改写 skill 指令。目标 skill 若是指向其他安装的符号链接或 Windows junction，会拒绝写入，避免影响别的 agent。写入按单文件原子替换，多文件同步不是事务；执行失败时应查看已写入文件和 Git diff 后重试。

新加或移除技能时更新对应 plugins.json 和 README；Claude Code 还需更新 marketplace。通过旧版根 `skills/` 路径安装的用户应按上述分区重新选择来源；不要对整个仓库执行不区分 agent 的技能安装。

```bash
python scripts/check_consistency.py
python -m unittest discover -s scripts -p "test_*.py" -v
```

CI 在 Linux、Windows、macOS 上运行。检查覆盖目录、清单、marketplace、Pi 入口、文档链接及同步行为；它不等于真实宿主中的运行验证。

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

## 使用笔记

- [Claude Code](agents-learning/claude-code.md)：优先用本仓库 / 官方 marketplace 安装；附 `opusplan` / 子代理 model / `/advisor`、[子 agent 配置](agents-learning/claude-code.md#子-agent-配置)
- [Pi](agents-learning/pi.md)：使用手册 / 总稿（分层、省上下文、核心包、终端渲染、全栈加装、规划/执行分模型、[子 agent 配置](agents-learning/pi.md#子-agent-配置)）
- [Pi 自助 bootstrap](agents-learning/pi-bootstrap.md)：可直接丢给 Pi 的安装配置提示词
- [AGENTS.md / CLAUDE.md 写法](agents-learning/project-instructions.md)：短硬可验证的项目指令文件
- [自主持续迭代](agents-learning/autonomous-iteration.md)：可验证终点 + 落盘状态 + 循环（Pi goal / circadian、Claude Ralph）
- [跨 agent 调用](agents-learning/cross-agent.md)：跨 harness 把对方包成工具（CLI / MCP / 桥）
- [Hermes](agents-learning/hermes.md)：常用命令（模型配置、会话管理）

## 插件参考与来源

[插件参考目录](plugins/README.md) 保留其他工具和社区扩展的资料；当前三端实际记录以各自 plugins.json 为准。[首次盘点记录](plugins/local-sync.md) 保留来源比较的历史背景。

## 版权与许可证

根目录 [LICENSE](LICENSE) 覆盖本仓库原创文档、脚本、配置和原创内容。各 agent 的 skills 及独立扩展以各自许可证为准；目录迁移保留其作者、正文、脚本、资源与许可证。`concept-first-tutorial` 是本机自定义技能，没有独立许可证，已在完整性说明中注明。
