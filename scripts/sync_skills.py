#!/usr/bin/env python3
"""Preview or apply one agent's skill import/export without deleting target files."""

import argparse
import json
import os
from pathlib import Path
import re
import stat
import tempfile

AGENTS = ("pi", "claude-code", "codex")
LOCAL_DIRS = {"pi": ".agents", "claude-code": ".claude", "codex": ".codex"}
IGNORE = {".git", "node_modules", "__pycache__", ".cache", ".DS_Store", "Thumbs.db"}


def comparable(data):
    if b"\0" in data:
        return data
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return data
    return data.replace(b"\r\n", b"\n")


def linked(path):
    return path.is_symlink() or (os.name == "nt" and path.exists()
                                 and path.lstat().st_reparse_tag == stat.IO_REPARSE_TAG_MOUNT_POINT)


def source_files(directory):
    directory = directory.resolve(strict=True)
    for current, directories, names in os.walk(directory):
        directories[:] = sorted(name for name in directories if name not in IGNORE)
        for name in directories + sorted(names):
            path = Path(current) / name
            if name in IGNORE or path.suffix in {".pyc", ".log", ".tmp"}:
                continue
            if linked(path):
                raise ValueError(f"Nested source symlink or junction is not copied: {path}")
            if path.is_file():
                yield path.relative_to(directory), path


def check_target(path, destination):
    for parent in [path, *path.parents]:
        if parent == destination:
            break
        if linked(parent):
            raise ValueError(f"Target symlink or junction would affect another installation: {parent}")
        if parent != path and parent.exists() and not parent.is_dir():
            raise ValueError(f"Target parent is not a directory: {parent}")
    if path.exists() and not path.is_file():
        raise ValueError(f"Target is not a regular file: {path}")


def sync(root, agent, direction, names, local_dir, *, apply=False, replace=False):
    if agent not in AGENTS or direction not in {"import", "export"}:
        raise ValueError("Choose an agent and import/export direction.")
    manifest = json.loads((root / agent / "plugins.json").read_text(encoding="utf-8"))
    listed = manifest["skills"]
    explicit = bool(names)
    names = names or listed
    if len(set(names)) != len(names):
        raise ValueError("Skill names must not repeat.")
    for name in names:
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", name):
            raise ValueError(f"Invalid skill name: {name}")
        if direction == "export" and name not in listed:
            raise ValueError(f"Skill is not listed for {agent}: {name}")

    repo_dir = root / agent / "skills"
    source, destination = (local_dir, repo_dir) if direction == "import" else (repo_dir, local_dir)
    destination = destination.expanduser().resolve()
    source = source.expanduser().resolve()
    if source == destination or source in destination.parents or destination in source.parents:
        raise ValueError("Source and destination skill roots must not overlap.")
    changes = []
    for name in names:
        skill = source / name
        if not (skill / "SKILL.md").is_file():
            if explicit:
                raise ValueError(f"Source has no SKILL.md: {skill}")
            print(f"SKIP {name}: source is not installed")
            continue
        text = (skill / "SKILL.md").read_text(encoding="utf-8")
        header = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.S)
        declared = re.search(r"^name:\s*[\"']?([^\"'\n]+)", header[1], re.M) if header else None
        if not declared or declared[1].strip() != name:
            raise ValueError(f"Skill frontmatter name does not match {name}: {skill}")
        for relative, path in source_files(skill):
            target = destination / name / relative
            check_target(target, destination)
            data = path.read_bytes()
            previous = target.read_bytes() if target.exists() else None
            if previous is None or comparable(previous) != comparable(data):
                changes.append((target, data, path.stat().st_mode, previous is not None))

    for target, _, _, conflict in changes:
        action = "REPLACE" if conflict and replace else "CONFLICT" if conflict else "ADD"
        print(f"{action} {target.relative_to(destination).as_posix()}")
    if any(conflict for _, _, _, conflict in changes) and not replace:
        raise ValueError("Conflicts found; nothing written. Review the differences before using --replace.")
    if apply:
        for target, data, source_mode, _ in changes:
            target.parent.mkdir(parents=True, exist_ok=True)
            mode = target.stat().st_mode if target.exists() else source_mode
            temporary = None
            try:
                with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as output:
                    temporary = Path(output.name)
                    output.write(data)
                temporary.chmod(stat.S_IMODE(mode))
                os.replace(temporary, target)
            finally:
                if temporary is not None and temporary.exists():
                    temporary.unlink()
    print(f"{'APPLIED' if apply else 'PREVIEW'} {agent} {direction}: {len(changes)} file(s); target-only files preserved.")
    return len(changes)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("agent", choices=AGENTS)
    parser.add_argument("direction", choices=("import", "export"))
    parser.add_argument("names", nargs="*")
    parser.add_argument("--skills-dir", type=Path, help="Local skill root; defaults to the selected agent's directory")
    parser.add_argument("--apply", action="store_true", help="Write the previewed changes")
    parser.add_argument("--replace", action="store_true", help="Allow reviewed conflicting files to be replaced")
    args = parser.parse_args()
    configured = os.environ.get("SKILLS_DIR")
    if not configured and args.agent == "claude-code":
        configured = os.environ.get("CLAUDE_SKILLS_DIR")
    local = args.skills_dir or (Path(configured) if configured else Path.home() / LOCAL_DIRS[args.agent] / "skills")
    try:
        sync(Path(__file__).resolve().parent.parent, args.agent, args.direction,
             args.names, local, apply=args.apply, replace=args.replace)
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, f"ERROR: {error}\n")


if __name__ == "__main__":
    main()
