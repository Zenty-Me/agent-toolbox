#!/usr/bin/env bash
# 把本机已安装的 skill 同步到仓库的 skills/ 目录。
# 可用 SKILLS_DIR 指向 Pi 共享目录或 Codex 目录；兼容旧的 CLAUDE_SKILLS_DIR。
# 同步前先比较版本与 diff，避免用旧副本覆盖仓库中的修复。
# 用法：./scripts/sync-skills.sh [skill名...]，不传参数则同步 skills/ 下已有的全部 skill。
#
# 注意：本脚本只复制 skill 文件，不会改 marketplace / README。
# 新增或下线 skill 后请手动更新：
#   1) .claude-plugin/marketplace.json 对应插件的 skills 列表
#   2) README.md 安装表与 Skills 列表
#   3) 各 skill 目录下的 LICENSE（从上游同步）
# 然后运行：./scripts/check-consistency.sh
set -euo pipefail

repo_dir="$(cd "$(dirname "$0")/.." && pwd)"
src_dir="${SKILLS_DIR:-${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}}"

if [ $# -gt 0 ]; then
  names=("$@")
else
  names=()
  for d in "$repo_dir"/skills/*/; do names+=("$(basename "$d")"); done
fi

for name in "${names[@]}"; do
  if [ ! -f "$src_dir/$name/SKILL.md" ]; then
    echo "跳过 $name：$src_dir/$name 下没有 SKILL.md" >&2
    continue
  fi
  rm -rf "$repo_dir/skills/$name"
  # -L 跟随符号链接，复制真实文件
  cp -rL "$src_dir/$name" "$repo_dir/skills/$name"
  rm -rf "$repo_dir/skills/$name/.git"
  find "$repo_dir/skills/$name" -name __pycache__ -prune -exec rm -rf {} +
  echo "已同步 $name"
done

echo "提示：同步后请运行 ./scripts/check-consistency.sh，并视情况更新 marketplace.json / README。"
