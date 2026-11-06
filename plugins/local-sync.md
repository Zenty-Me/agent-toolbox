# 本机开发工具同步记录

扫描日期：2026-11-06。先将本仓库快进到远端 `102cd90`，再比较本机 Pi、Claude Code、Codex 的安装内容。此记录以本机安装版本为依据；本次未升级这些工具的安装，也未查询全部插件的远端最新版本。

## 当前目录与历史范围

本页是首次盘点的历史记录；后续整理已将能力分为 [Pi](../pi/README.md)、[Claude Code](../claude-code/README.md)、[Codex](../codex/README.md)。每区保存独立 skills 与 plugins.json，开发和日常使用内容均保留。来源核对与先补齐本地再同步的结果见[完整性说明](completeness.md)。

首次盘点曾保存 Pi Switch 工作副本；按后续确认现已移除重复源码，仅保留[项目地址](https://github.com/Zenty-Me/pi-switch)与安装记录，旧快照可从提交 `061e55c` 恢复。

## 本次文件同步

| 动作 | 内容 | 本机来源 |
|---|---|---|
| 新增 | `ponytail`、`ponytail-review`、`ponytail-audit`、`ponytail-debt`、`ponytail-gain`、`ponytail-help` | Pi 安装的 Ponytail 5.3.3，commit `96608e078b2d5ea607c5c3b8b5a54d1c1fba6846` |
| 新增 | `find-skills` | `~/.agents/skills/find-skills`；来源 vercel-labs/skills |
| 新增 | `concept-first-tutorial`，含 agent 配置与讲解样例 | `~/.codex/skills/concept-first-tutorial`；本机自定义，上游未记录 |
| 更新 | `grilling` | `~/.agents/skills/grilling`；补充使用 fresh context window 获取事实的要求 |
| 归档 | Pi Switch 0.4.0 的 20 个源码、配置与测试文件，包含 3 个本地修改文件 | Pi 当前配置引用的本地工作副本，基线 `c42da67` |
| 归档 | `compact-status.ts`，附本地安装 manifest | `~/.pi/agent/extensions/compact-status.ts` |

已同步根目录 README、marketplace 1.3.0 与插件入口文档。新增 `ponytail-skills@agent-dev-kit` 安装组；原来的 `coding-standards` 增加技术教程 skill，`skill-dev` 增加 find-skills。

## 同名 skills 比较

比较目录包括 `~/.agents/skills`、`~/.claude/skills`、`~/.codex/skills`，以及 Claude Code 已登记安装插件内的 skills。比较实际文件内容；忽略 CRLF/LF 差异，保留仓库已有许可证和已确认的本地修复。

| Skill / 情况 | 比较结果与处理 |
|---|---|
| Ponytail | Pi 5.3.3、Claude Code 5.1.0、Codex 缓存 4.10.0。通用技能取 Pi 当前安装版本 |
| `grilling` | 共享目录有新措辞，已同步；Claude 插件缓存内容较旧 |
| `grill-me` | 本机与仓库入口相同，保留仓库许可证 |
| `clean-code`、`frontend-design` | 仓库与 Claude Code 版本相同；共享 / Codex 副本较旧，保留仓库版本 |
| `drawio-skill` | 仓库已有较新的 diagram IR / MCP 修复；本机三套副本均不覆盖这些修复 |
| `nextjs` | 保留仓库的 references 路径修复与 overlay |
| `karpathy-guidelines` | 仅文件结尾换行不同，保留仓库版本 |
| `brainstorming` | 仓库已收录较新的上游内容，保留仓库版本 |
| `test-driven-development` | 仓库使用 addyosmani/agent-skills；Claude Superpowers 中的同名 skill 是另一套实现，分别保留来源 |
| `systematic-debugging` | Claude Superpowers 缓存存在另一版本，保留仓库现有内容与配套引用 |
| `skill-creator` | 本机 Anthropic 版本与仓库相同；Codex `.system/skill-creator` 是另一实现，不覆盖 |
| 旧 `react-best-practices` | 远端已去重，沿用 `vercel-react-best-practices`，不恢复旧目录 |
| 其他同名通用 skills | 未发现需要覆盖仓库的内容更新；补充许可证、元数据等仓库文件继续保留 |

`code-review` 本机编排入口要求配套的 `code-review-*` skills；当前配套 `code-review-testing` 写死 Codex 源码仓库的 Rust / core/suite 测试约定。这组未作为通用 skills 收录。通用审查使用现有 code-reviewer 与本次新增的 Ponytail review / audit。

## Claude Code

以下 **18 项**来自 `installed_plugins.json`。配置中显式开启 3 项。其余标为“已登记安装”；仅凭安装登记或缓存目录无法确认是否正在加载。

| 插件 | 安装版本 | 配置状态 |
|---|---|---|
| `mattpocock-skills@claude-plugins-official` | 1.2.3 | 显式开启 |
| `ponytail@ponytail` | 5.1.0 | 显式开启 |
| `warp@claude-code-warp` | 2.4.0 | 显式开启 |
| `superpowers@claude-plugins-official` | 6.4.1 | 已登记安装 |
| `ralph-loop@claude-plugins-official` | 1.0.0 | 已登记安装 |
| `skill-creator@claude-plugins-official` | `fbe07fb6ce7d` | 已登记安装 |
| `frontend-design@claude-plugins-official` | `fbe07fb6ce7d` | 已登记安装 |
| `playwright@claude-plugins-official` | `fbe07fb6ce7d` | 已登记安装 |
| `context7@claude-plugins-official` | `fbe07fb6ce7d` | 已登记安装 |
| `code-simplifier@claude-plugins-official` | 1.0.0 | 已登记安装 |
| `code-review@claude-plugins-official` | `fbe07fb6ce7d` | 已登记安装 |
| `feature-dev@claude-plugins-official` | `fbe07fb6ce7d` | 已登记安装 |
| `pr-review-toolkit@claude-plugins-official` | `fbe07fb6ce7d` | 已登记安装 |
| `security-guidance@claude-plugins-official` | 2.0.8 | 已登记安装 |
| `commit-commands@claude-plugins-official` | `fbe07fb6ce7d` | 已登记安装 |
| `supabase@supabase-agent-skills` | `544bfc56c89a` | 已登记安装 |
| `postgres-best-practices@supabase-agent-skills` | `544bfc56c89a` | 已登记安装 |
| `debugging-toolkit@claude-code-workflows` | 1.2.1 | 已登记安装 |

本次补充了 Matt Pocock Skills 和 Warp 的清单入口。完整 Git SHA 与 marketplace 来源见 JSON。

```text
/plugin marketplace add warpdotdev/claude-code-warp
/plugin install warp@claude-code-warp
/plugin install mattpocock-skills@claude-plugins-official
```

## Codex

从 `config.toml` 与 `~/.codex/plugins/cache` 比较出以下 **9 项通用开发插件条目**。桌面内置插件由 Codex 自身分发与管理；本仓库记录名称、版本、许可证与配置状态。

| 插件 | 本机版本 | 配置状态 |
|---|---|---|
| `browser@openai-bundled` | 26.1023.50603 | 显式开启 |
| `chrome@openai-bundled` | 26.1023.50603 | 显式开启 |
| `codex-app-tools@openai-bundled` | 26.1023.50603 | 显式开启 |
| `computer-use@openai-bundled` | 26.1023.50603 | 显式开启 |
| `unified-computer-use@openai-bundled` | 26.1023.50603 | 显式开启 |
| `visualize@openai-bundled` | 1.0.57 | 显式开启 |
| `plugin-management@openai-curated-remote` | 0.1.0 | 仅发现缓存，未显式配置 |
| `sites@openai-curated-remote` | 1.1.2 | 仅发现缓存，未显式配置 |
| `ponytail@ponytail` | 4.10.0 | 仅发现缓存，未显式配置 |

这次从 Codex 的通用 skills 中收录了 `concept-first-tutorial`。其余同名副本按上表比较，保留仓库版本。

## 来源与校验

新增 skills 和本地扩展均从明确选定的目录复制，源文件逐项校验。JSON 的树摘要按相对路径排序，对文件统一 CRLF 为 LF 后计算 SHA-256，便于 Windows / Linux checkout 复核。Ponytail 六个 skill 额外补入原项目 MIT LICENSE；find-skills 的本机安装仅有 SKILL.md，其 MIT LICENSE 从 [Vercel 原仓库](https://raw.githubusercontent.com/vercel-labs/skills/main/LICENSE) 补齐。源树与仓库树因此可以有不同摘要。

`concept-first-tutorial` 的本机目录没有独立 LICENSE、上游地址或版本号；按本机自定义内容记录，未给它编造上游版本或许可证。

首次归档时，Pi Switch 的类型检查和 48 个测试通过；当前源码由独立项目维护。后续目录整理和缺失资源补齐均未改写原有 skill 正文。
