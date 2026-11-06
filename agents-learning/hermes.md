# Hermes 速查

> 命令以你本机安装的 Hermes 为准；版本不同可能略有差异。先试 `hermes --help` / `hermes <cmd> --help`。

## 配置

### 配置模型

```bash
hermes model
```

按提示选择或切换当前会话使用的模型。

## 会话管理

### 列出会话

```bash
hermes sessions list
```

### 交互式浏览 / 选择

```bash
hermes sessions browse
```

### 删除指定会话

```bash
hermes sessions delete <id>
```

### 按时间清理（prune）

```bash
hermes sessions prune              # 默认删除 90 天前的会话
hermes sessions prune --older-than 30  # 删除 30 天前的会话
```

### 存储统计

```bash
hermes sessions stats
```

## 实用提示

1. **先 browse 再 delete**：不确定 id 时用 `sessions browse`，避免误删。
2. **定期 prune**：本地会话多了会占磁盘；用 `stats` 看体量再决定 `--older-than`。
3. **与本仓库 skills**：Hermes 若支持 Agent Skills，可从 [Agent Toolbox](https://github.com/Zenty-Me/agent-toolbox) 选择合适的 skills 分区复制安装（见根 README）；Claude Code 用户优先用 marketplace。
4. **模型切不过时**：检查 API Key / 供应商配置是否仍有效，再跑 `hermes model`。

## 相关

- Claude Code 安装与插件：[claude-code.md](claude-code.md)
- 本仓库插件精选：[../plugins/README.md](../plugins/README.md)
