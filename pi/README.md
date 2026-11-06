# Pi 能力

本分区收录可跨项目复用的开发和日常能力。与其他 agent 出现同名 skill 是允许的；各分区独立维护，不自动互相覆盖。

当前 33 个 skills 的正文沿用整理前的原文，未手工改写。已验证的缺失资源先在本地补齐，再复制到本分区。技能文件与完整插件的 hooks、工具和自动启用功能是不同的安装内容，详见[完整性与依赖说明](../plugins/completeness.md)。

## 安装与更新

在本仓库根目录安装本分区的 skills：

```bash
pi install ./pi
```

它引用本地仓库目录；以后更新仓库并在 Pi 中 `/reload`。此包只加载 skills；外部插件按下表分别安装。本地状态栏可单独安装：

```bash
pi install ./pi/extensions/compact-status
```

[Pi Switch](https://github.com/Zenty-Me/pi-switch) 的源码在独立项目维护，本库仅记录来源、已观察版本与安装方式：

```bash
pi install git:github.com/Zenty-Me/pi-switch
```

插件的 npm 顶层版本和 Ponytail commit 已固定在清单里。Pi Switch 地址安装可能与原机器的本地开发版本不同。模型与浏览器认证需在新设备分别完成；每个扩展在同一宿主只加载一份。

## 插件清单

完整来源、Git commit、状态和安装方式见 [plugins.json](plugins.json)。记录的版本来自 2026-11-06 的本机盘点，不代表远端最新版。

| 插件 | 观察版本 | 状态 / 安装 |
|---|---|---|
| `pi-web-access` | 0.40.0 | `pi install npm:pi-web-access@0.40.0` |
| `pi-subagents` | 0.78.0 | `pi install npm:pi-subagents@0.78.0` |
| `pi-vision-handoff` | 0.10.9 | `pi install npm:pi-vision-handoff@0.10.9` |
| `pi-context-view` | 0.7.1 | `pi install npm:pi-context-view@0.7.1` |
| `pi-browser-use` | 0.12.12 | `pi install npm:pi-browser-use@0.12.12` |
| `pi-code-render` | 0.1.9 | `pi install npm:pi-code-render@0.1.9` |
| `pi-better-render` | 0.3.0 | `pi install npm:pi-better-render@0.3.0` |
| `pi-switch` | 0.4.0 | `pi install git:github.com/Zenty-Me/pi-switch` |
| `ponytail` | 5.3.3 | `pi install git:github.com/DietrichGebert/ponytail@96608e078b2d5ea607c5c3b8b5a54d1c1fba6846` |

另保留本地扩展 [compact-status](extensions/compact-status/compact-status.ts)，命令 `/statusbar [on|off]`。它使用 Pi 1.5.x 提供的运行模块。

## Skills

| 分类 | Skill | 说明 | 来源 |
|---|---|---|---|
| 编码与写作准则 | [`karpathy-guidelines`](skills/karpathy-guidelines/SKILL.md) | 基于 Andrej Karpathy 观察总结的 LLM 编码行为准则 | forrestchang/andrej-karpathy-skills |
| | [`clean-code`](skills/clean-code/SKILL.md) | 简洁直接的编码规范，不过度设计 | vudovn/ag-kit |
| | [`humanizer`](skills/humanizer/SKILL.md) | 去掉文字里的 AI 腔，读起来像本人写的，不改变原意 | blader/humanizer |
| | [`concept-first-tutorial`](skills/concept-first-tutorial/SKILL.md) | 用解释、小例子与最小代码编写技术教程 | 本机 Codex 自定义 skill |
| 代码质量 | [`code-reviewer`](skills/code-reviewer/SKILL.md) | 关注安全、性能和最佳实践的代码审查 | awesome-llm-apps（Shubhamsaboo 等） |
| | [`refactor-advisor`](skills/refactor-advisor/SKILL.md) | 识别代码坏味道并给出重构方案 | 本仓库原创 |
| | [`security-best-practices`](skills/security-best-practices/SKILL.md) | 按语言和框架做安全最佳实践审查 | openai/skills |
| | [`security-threat-model`](skills/security-threat-model/SKILL.md) | 基于仓库证据的威胁建模（信任边界、滥用路径、缓解） | openai/skills |
| | [`code-simplification`](skills/code-simplification/SKILL.md) | 在不改变行为的前提下简化代码、提升可读性 | addyosmani/agent-skills |
| | [`test-driven-development`](skills/test-driven-development/SKILL.md) | 红绿重构驱动开发与缺陷修复 | addyosmani/agent-skills |
| | [`systematic-debugging`](skills/systematic-debugging/SKILL.md) | 先根因再修复的系统化调试流程 | obra/superpowers |
| 设计与规划 | [`brainstorming`](skills/brainstorming/SKILL.md) | 动手前的头脑风暴与需求澄清 | obra/superpowers |
| | [`grill-me`](skills/grill-me/SKILL.md) | 手动触发入口（`/grill-me`）；内部调用 [[`grilling`](skills/grilling/SKILL.md)](skills/grilling/SKILL.md) | mattpocock/skills |
| | `grilling` | 按设计树多轮追问，打磨方案或决策 | mattpocock/skills |
| | [`drawio-skill`](skills/drawio-skill/SKILL.md) | 生成可编辑的 draw.io 架构图、UML、ERD、时序图 | Agents365-ai/drawio-skill |
| 前端 | [`frontend-design`](skills/frontend-design/SKILL.md) | 有辨识度的前端视觉设计 | anthropics/skills |
| | [`nextjs`](skills/nextjs/SKILL.md) | Next.js App Router 开发指导（含本地 overlay） | openai/plugins（vercel/nextjs） |
| | [`vercel-react-best-practices`](skills/vercel-react-best-practices/SKILL.md) | Vercel 的 React/Next.js 性能优化指南 | vercel-labs/agent-skills |
| | [`vercel-composition-patterns`](skills/vercel-composition-patterns/SKILL.md) | React 组件组合模式 | vercel-labs/agent-skills |
| | [`web-design-guidelines`](skills/web-design-guidelines/SKILL.md) | 按 Web Interface Guidelines 审查 UI/可访问性/UX | vercel-labs/agent-skills |
| | [`vercel-react-view-transitions`](skills/vercel-react-view-transitions/SKILL.md) | React View Transition API 与路由/共享元素动画 | vercel-labs/agent-skills |
| 后端与数据库 | [`supabase`](skills/supabase/SKILL.md) | Supabase 开发 | supabase/agent-skills |
| | [`supabase-postgres-best-practices`](skills/supabase-postgres-best-practices/SKILL.md) | Postgres 最佳实践 | supabase/agent-skills |
| | [`python-performance-optimization`](skills/python-performance-optimization/SKILL.md) | Python 性能分析与优化 | wshobson/agents |
| Skill 开发 | [`skill-creator`](skills/skill-creator/SKILL.md) | 创建、改进、评测 skill | anthropics/skills |
| | [`mcp-builder`](skills/mcp-builder/SKILL.md) | 设计并实现高质量 MCP server（Python/TS） | anthropics/skills |
| | [`find-skills`](skills/find-skills/SKILL.md) | 查找并安装可复用的 agent skills | vercel-labs/skills |
| 最小实现与审查 | [`ponytail`](skills/ponytail/SKILL.md) | 用最小完整改动完成开发任务 | DietrichGebert/ponytail 5.3.3 |
| | [`ponytail-review`](skills/ponytail-review/SKILL.md) | 审查变更的正确性、安全、负载与代码精简空间 | DietrichGebert/ponytail 5.3.3 |
| | [`ponytail-audit`](skills/ponytail-audit/SKILL.md) | 按风险审计整个仓库 | DietrichGebert/ponytail 5.3.3 |
| | [`ponytail-debt`](skills/ponytail-debt/SKILL.md) | 汇总 shortcut / ponytail 注释中的技术债 | DietrichGebert/ponytail 5.3.3 |
| | [`ponytail-gain`](skills/ponytail-gain/SKILL.md) | 展示上游发布的基准测试结果 | DietrichGebert/ponytail 5.3.3 |
| | [`ponytail-help`](skills/ponytail-help/SKILL.md) | 模式、技能与命令速查 | DietrichGebert/ponytail 5.3.3 |

## 维护

先按官方来源核对、补齐本地资源，再导入本分区：

```bash
python scripts/sync_skills.py pi import grill-me grilling
python scripts/sync_skills.py pi import grill-me grilling --apply
```

以上命令从仓库根目录执行。已有文件内容不同会报冲突；审阅后才使用 `--replace --apply`。目标已有的额外文件会保留。新增技能需同步本分区 plugins.json 与本页 Skills 表；Claude Code 还需更新根 marketplace。
