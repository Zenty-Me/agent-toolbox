# Pi 插件快照与恢复

本页记录 2026-11-06 本机实际使用的 **9 个 Pi 包和 1 个自动加载的本地扩展**。宿主版本为 Pi 1.5.0、Node.js 24.11.0。版本、Git commit、npm integrity、源码快照校验值见 [installed.json](../installed.json)；跨工具比较见[同步记录](../local-sync.md)。

## 当前包

| 包 | 本机版本 | 用途 | 来源 |
|---|---|---|---|
| `pi-web-access` | 0.40.0 | 网页搜索、内容抓取、GitHub / PDF / 视频读取 | [nicobailon/pi-web-access](https://github.com/nicobailon/pi-web-access) |
| `pi-subagents` | 0.78.0 | 子代理、并行任务、脚本工作流与 council | [nicobailon/pi-subagents](https://github.com/nicobailon/pi-subagents) |
| `pi-vision-handoff` | 0.10.9 | 把图片交给视觉模型描述，再回传当前模型 | [monotykamary/pi-vision-handoff](https://github.com/monotykamary/pi-vision-handoff) |
| `pi-context-view` | 0.7.1 | 查看上下文、系统提示词、工具定义及扩展注入 | [dimk90/pi-context-view](https://github.com/dimk90/pi-context-view) |
| `pi-browser-use` | 0.12.12 | Chrome DevTools 浏览器自动化 | [0xPlayerOne/pi-browser-use](https://github.com/0xPlayerOne/pi-browser-use) |
| `pi-code-render` | 0.1.9 | 代码块卡片、复制与原文切换 | [chengyayu/pi-code-render](https://github.com/chengyayu/pi-code-render) |
| `pi-better-render` | 0.3.0 | Markdown、代码和公式渲染 | [JeffeyChou/pi-better-render](https://github.com/JeffeyChou/pi-better-render) |
| `pi-switch` | 0.4.0 + 本地未提交修复 | 按项目切换 Skills / MCP，支持对话建议与确认应用 | [本地源码快照](pi-switch/) · [原仓库](https://github.com/Zenty-Me/pi-switch) |
| `ponytail` | 5.3.3，commit `96608e0` | 最小完整实现、审查、审计与技术债记录 | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) |

## 在另一台机器恢复

在本仓库根目录执行下列命令。npm 包固定本次安装版本，Ponytail 固定实际 Git commit。Pi Switch 使用归档目录，以包含本地尚未提交的修复。

```bash
pi install npm:pi-web-access@0.40.0
pi install npm:pi-subagents@0.78.0
pi install npm:pi-vision-handoff@0.10.9
pi install npm:pi-context-view@0.7.1
pi install npm:pi-browser-use@0.12.12
pi install npm:pi-code-render@0.1.9
pi install npm:pi-better-render@0.3.0
pi install git:github.com/DietrichGebert/ponytail@96608e078b2d5ea607c5c3b8b5a54d1c1fba6846
pi install ./plugins/pi/pi-switch
pi install ./plugins/pi/local-extensions
```

`pi-browser-use` 需要 Node.js 24 和 Chrome。Pi Switch 需要 Pi 1.5.x、Node.js 22.19+；运行模块由 Pi 提供。npm 包的顶层版本已固定，传递依赖仍由包管理器按各包声明解析。

本地目录安装会引用该目录，保留仓库位置。已有相同插件或状态栏时先核对 `pi list` 与 `~/.pi/agent/extensions/`，每个扩展只加载一份。新机器分别完成模型、浏览器登录与所需服务认证，之后新开会话或 `/reload`。

## Pi Switch 源码快照

[pi-switch/](pi-switch/) 保存当前实际使用工作副本的 20 个受版本控制文件，包含实现、README、许可证、锁文件、类型检查配置及测试。

基线为 `c42da67734788095807535b1798297d865849927`。本机在此基础上修改了：

- `src/tool.ts`：兼容要求工具全部字段都存在的 provider，未使用字段接受 null，动作相关校验仍保留。
- `test/apply.test.ts`：补齐 provider 参数形状与确认边界回归测试。
- `CHANGELOG.md`：记录上述修复。

归档保留以上修改，未改变原工作副本。安装到 Pi 的另一个 Git 缓存停留在 `e1f1570`；当前设置实际引用本地工作副本，因此选用本地版本。直接从 GitHub 安装发布基线不包含这三份未提交改动。

本次验证：源工作副本 TypeScript 检查通过，48 个测试全部通过；归档文件与源文件逐项核对一致。

## 本地状态栏

[local-extensions/compact-status.ts](local-extensions/compact-status.ts) 来自 `~/.pi/agent/extensions/compact-status.ts`，通过旁边的 `package.json` 作为本地 Pi package 安装。

显示路径 / 分支、模型 / 思考级别、上下文占用、token / 缓存 / 费用，以及当前工具与等待状态。命令为 `/statusbar [on|off]`。关闭后恢复 Pi 默认底栏。

## 随插件提供的 skills

| 包 | 随包安装的 skills |
|---|---|
| `pi-subagents` | `pi-subagents`、`council-mode` |
| `pi-browser-use` | `browser-policy`、`auth-bootstrap`、`derive-client`、`dogfood`、`gmail-auth`、`playwright-handoff`、`triage-console`、`visual-qa` |
| `ponytail` | `ponytail`、`ponytail-review`、`ponytail-audit`、`ponytail-debt`、`ponytail-gain`、`ponytail-help` |

浏览器和子代理 skills 依赖对应插件工具，随固定版本包恢复。Ponytail 六个通用 skills 也收录在根目录 `skills/`，方便其他 agent 选择安装；Pi 已安装 Ponytail 原插件时沿用随包版本。

本目录的第三方/独立插件源码以各自许可证为准；插件设置、账户、认证信息和会话记录不在快照中。
