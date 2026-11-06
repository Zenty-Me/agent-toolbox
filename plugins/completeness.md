# 本地完整性核对与同步

本页记录 2026-11-06 的处理顺序：先找到远程来源并补齐本地缺失文件，再把这些资源同步到 Pi、Claude Code、Codex 各分区。完整明细见 [completeness.json](completeness.json)。

## 已完成

- 按 `.agents/.skill-lock.json` 中的 Git tree 核对 15 个有明确来源的技能；只有正文匹配对应来源时才补缺失文件，现有本地变体不覆盖。
- 按锁定 npm 发布包与 SHA-512 integrity 核对 7 个 Pi npm 插件，共 1,640 个发布文件；没有发现缺文件或内容差异。
- 检查 Claude Code 插件声明的 26 个资源路径、Codex 插件声明的 16 个资源路径，均存在。
- 本地补齐 47 个文件：许可证、Vercel 元数据、grill-me / grilling 的 agent 配置，以及 Next.js 引用所需文件。正文未手工改写。
- 向三套分区补入共 114 个原先缺失的资源文件；已存在且相同的文件不重复写入。
- 下载完整的 ag-kit 与 Superpowers 源码到本地独立来源目录，未启用额外 hooks、未改认证和宿主开关，未混装同名技能。

## 官方来源与版本

| 能力 | 来源 | 本次核对依据 |
|---|---|---|
| clean-code 及配套检查工具 | [vudovn/ag-kit](https://github.com/vudovn/ag-kit) | commit `549ba3dc2eb1d40fccb5b6d792eba4101c80cd69`；clean-code tree 与本机锁定值一致 |
| 规划 / 调试完整流程 | [obra/superpowers](https://github.com/obra/superpowers) | 源码 7.0.2，commit `22f0b463e7a5e579904dd6211a520321035526f7`；原 Claude 插件 6.4.1 的完整 skills 已存在 |
| grill-me / grilling | [mattpocock/skills](https://github.com/mattpocock/skills) | commit `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`；正文与本机一致，补 agent 配置 |
| Next.js 历史参考知识 | [vercel-labs/next-skills](https://github.com/vercel-labs/next-skills) | 迁移前 commit `dc1de9caf7612d73f56a8dec3cb1bd6c9ec096b9`；逐文件核对内容 / Git blob |
| Next.js 当前工作流 | [vercel/next.js skills](https://github.com/vercel/next.js/tree/canary/skills) | 上游已迁移；保留本机旧版包装层，不将其伪装成最新版 |
| Ponytail | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | 保留既有安装版本与六个 skills |
| Pi Switch | [Zenty-Me/pi-switch](https://github.com/Zenty-Me/pi-switch) | 本库只保留来源与安装方式；实现回独立项目维护 |

## 完整文件与运行依赖的区别

### clean-code / ag-kit

本机 clean-code 的配套命令来自 ag-kit 的整套 `.agents/` 工程布局。其 `frontend-design` 与当前 Anthropic 同名技能不是同一实现，所以没有把两者拼在一起。

完整源码已放在本机 `~/.agents/vendor/ag-kit`，保留所有配套检查脚本、技能、角色与来源 Git 记录；新设备可从项目地址克隆。需要实际使用该套工具时，按上游 README 在目标工程安装。把工具包源码下载完整，不代表在任意项目中都能直接执行 `.agents/skills/...` 相对路径。

### Superpowers

原 Claude Code 的 Superpowers 6.4.1 已包含 writing-plans、verification-before-completion 等技能；缺口主要是单独复制一个 skill 时没有带上完整插件。

新核对的 7.0.2 源码保存在本机 `~/.agents/vendor/superpowers`，上游现已提供 Pi 包。需要完整命名空间与启动逻辑时，按各宿主的官方安装方式使用整个插件；没有自动开启它，以免改变当前工作方式。不要把不同来源的同名 TDD / brainstorming 目录直接合并。

### grill-me 与 Ponytail

grill-me 的 `Skill` 工具入口就是上游原文，本次不做宿主适配改写。没有同名工具的宿主可以直接加载旁边的 grilling；能力是否可用应以宿主真实工具为准。

本库保留 Ponytail 全套六个技能。自动启用、状态栏、环境变量解析和 hooks 属于完整插件功能；独立 Markdown 技能不会实现这些运行逻辑。`ponytail-gain` 的基准来自上游，报告可在[对应 commit](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/benchmarks/results/2026-10-07-agentic.md)查阅，不是当前项目节省量。

### 自定义技能与来源不确定的变体

`concept-first-tutorial` 没有独立 LICENSE 与公开上游，保留其本机原文，不凭空补许可证或宣称来自官方。其他正文与锁定来源不匹配的本地变体也保持原样。报告中 `variantPreserved` 会标明这些情况。

## 后续维护

1. 有明确来源时先检查锁定版本与本地目录，再从对应官方版本补文件。
2. 同名不同来源的能力独立保留，不拼装，不为消除告警擅改正文。
3. 下载插件源码与启用插件是两件事；涉及 hooks、认证、自动运行或宿主配置时分别确认。
4. 补齐本地后，使用同步脚本导入对应 agent 分区并预览差异。
5. 真实跨宿主运行仍需要在各端验证；文件完整性检查不代替安装与功能测试。
