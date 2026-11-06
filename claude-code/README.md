# Claude Code 能力

本分区收录可跨项目复用的开发和日常能力。与其他 agent 出现同名 skill 是允许的；各分区独立维护，不自动互相覆盖。

当前 33 个 skills 的正文沿用整理前的原文，未手工改写。已验证的缺失资源先在本地补齐，再复制到本分区。技能文件与完整插件的 hooks、工具和自动启用功能是不同的安装内容，详见[完整性与依赖说明](../plugins/completeness.md)。

## 安装与更新

本仓库的 `agent-toolbox` marketplace 只指向 Claude Code 分区：

```text
/plugin marketplace add Zenty-Me/agent-toolbox
/plugin install planning@agent-toolbox
/plugin install ponytail-skills@agent-toolbox
```

可用组：coding-standards、code-quality、planning、frontend、backend、skill-dev、ponytail-skills。更新用 `/plugin marketplace update agent-toolbox`，然后按宿主提示重新加载。

Ponytail 六个技能和 grill-me / grilling 均保留。需要 Ponytail 的自动启用、状态栏和 hooks 时安装上游完整插件；已装完整插件时避免在同一 Claude 会话重复加载本库的同名技能。

也可以使用同步脚本复制本分区选定的技能：

```bash
python scripts/sync_skills.py claude-code export grill-me grilling
python scripts/sync_skills.py claude-code export grill-me grilling --apply
```

插件清单保留原机器的观察版本。`configuredEnabled` 为 null 表示没有显式启用记录，不作为新机器必须安装的清单。

<a id="marketplace-migration"></a>

## 旧 marketplace 迁移

marketplace 已从 `agent-dev-kit` 更名为 `agent-toolbox`。GitHub 地址重定向不会把已安装的 `插件组@agent-dev-kit` 自动改为新标识。更早的 `skills-prompts` 安装也按相同步骤迁移。

1. 在 Claude Code 的 `/plugin` 面板记录本库已安装的插件组、安装范围（用户或项目）和启用状态。
2. 卸载这些插件组的旧 `@agent-dev-kit` 或 `@skills-prompts` 安装，再移除对应的旧 marketplace。
3. 添加新 marketplace：`/plugin marketplace add Zenty-Me/agent-toolbox`。
4. 按原来的范围重装需要的插件组，例如 `/plugin install planning@agent-toolbox`，并恢复原启用状态。
5. 按宿主提示重新加载或新开会话，确认同名技能只加载一份。

只处理本库的旧安装；上游 Ponytail、Superpowers 等独立插件按各自的 marketplace 管理。该迁移说明不自动修改本机 Claude Code 配置。

## 插件清单

完整来源、Git commit、状态和安装方式见 [plugins.json](plugins.json)。记录的版本来自 2026-11-06 的本机盘点，不代表远端最新版。

| 插件 | 观察版本 | 状态 / 安装 |
|---|---|---|
| `code-review@claude-plugins-official` | fbe07fb6ce7d | 已登记 / 缓存，未确认启用 |
| `code-simplifier@claude-plugins-official` | 1.0.0 | 已登记 / 缓存，未确认启用 |
| `commit-commands@claude-plugins-official` | fbe07fb6ce7d | 已登记 / 缓存，未确认启用 |
| `context7@claude-plugins-official` | fbe07fb6ce7d | 已登记 / 缓存，未确认启用 |
| `debugging-toolkit@claude-code-workflows` | 1.2.1 | 已登记 / 缓存，未确认启用 |
| `feature-dev@claude-plugins-official` | fbe07fb6ce7d | 已登记 / 缓存，未确认启用 |
| `frontend-design@claude-plugins-official` | fbe07fb6ce7d | 已登记 / 缓存，未确认启用 |
| `mattpocock-skills@claude-plugins-official` | 1.2.3 | 显式开启 |
| `playwright@claude-plugins-official` | fbe07fb6ce7d | 已登记 / 缓存，未确认启用 |
| `ponytail@ponytail` | 5.1.0 | 显式开启 |
| `postgres-best-practices@supabase-agent-skills` | 544bfc56c89a | 已登记 / 缓存，未确认启用 |
| `pr-review-toolkit@claude-plugins-official` | fbe07fb6ce7d | 已登记 / 缓存，未确认启用 |
| `ralph-loop@claude-plugins-official` | 1.0.0 | 已登记 / 缓存，未确认启用 |
| `security-guidance@claude-plugins-official` | 2.0.8 | 已登记 / 缓存，未确认启用 |
| `skill-creator@claude-plugins-official` | fbe07fb6ce7d | 已登记 / 缓存，未确认启用 |
| `supabase@supabase-agent-skills` | 544bfc56c89a | 已登记 / 缓存，未确认启用 |
| `superpowers@claude-plugins-official` | 6.4.1 | 已登记 / 缓存，未确认启用 |
| `warp@claude-code-warp` | 2.4.0 | 显式开启 |
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
python scripts/sync_skills.py claude-code import grill-me grilling
python scripts/sync_skills.py claude-code import grill-me grilling --apply
```

以上命令从仓库根目录执行。已有文件内容不同会报冲突；审阅后才使用 `--replace --apply`。目标已有的额外文件会保留。新增技能需同步本分区 plugins.json 与本页 Skills 表；Claude Code 还需更新根 marketplace。
