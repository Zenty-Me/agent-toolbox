#!/usr/bin/env python3
"""Check per-agent skill inventories, documentation, entry points and local links."""

import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

AGENTS = ("pi", "claude-code", "codex")


def broken_links(path):
    text = path.read_text(encoding="utf-8")
    header = re.match(r"\A---\n.*?\n---(?:\n|$)", text, re.S)
    lines = text.splitlines()
    first_body_line = text[:header.end()].count("\n") if header else 0
    fenced = False
    for number, line in enumerate(lines, 1):
        if number <= first_body_line:
            continue
        if line.lstrip().startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if fenced:
            continue
        for target in re.findall(r"\[[^\]\n]+\]\(([^)]+)\)", line):
            target = target.strip().strip("<>")
            if urlsplit(target).scheme or target.startswith("#") or any(c in target for c in "$*{}|"):
                continue
            relative = unquote(target.split("#", 1)[0])
            if relative and not (path.parent / relative).exists():
                yield number, target


def check(root):
    errors = []
    warnings = []
    documents = [root / "README.md", *sorted((root / "agents-learning").glob("*.md")),
                 *sorted((root / "plugins").rglob("*.md"))]
    inventories = {}
    for agent in AGENTS:
        folder = root / agent
        manifest = json.loads((folder / "plugins.json").read_text(encoding="utf-8"))
        listed = manifest["skills"]
        disk = {p.name for p in (folder / "skills").iterdir() if p.is_dir()}
        inventories[agent] = disk
        if manifest.get("agent") != agent or len(set(listed)) != len(listed) or set(listed) != disk:
            errors.append(f"{agent}: skill directories and plugins.json do not agree")
        identifiers = [p.get("id", p.get("name")) for p in manifest["plugins"]]
        if None in identifiers or len(set(identifiers)) != len(identifiers):
            errors.append(f"{agent}: plugin identifiers are missing or duplicated")
        readme = folder / "README.md"
        text = readme.read_text(encoding="utf-8")
        section = re.search(r"## Skills\n(.*?)(?=\n## |\Z)", text, re.S)
        documented = set(re.findall(r"`([a-z0-9][a-z0-9-]*)`", section[1])) if section else set()
        if documented != disk:
            errors.append(f"{agent}: README Skills list does not agree with its inventory")
        documents.append(readme)
        for name in sorted(disk):
            path = folder / "skills" / name / "SKILL.md"
            if not path.is_file():
                errors.append(f"{agent}/{name}: SKILL.md is missing")
                continue
            content = path.read_text(encoding="utf-8")
            header = re.match(r"\A---\n(.*?)\n---(?:\n|$)", content, re.S)
            declared = re.search(r"^name:\s*[\"']?([^\"'\n]+)", header[1], re.M) if header else None
            if not declared or declared[1].strip() != name:
                errors.append(f"{agent}/{name}: frontmatter name does not match the directory")
            if not header or len(content[header.end():].strip()) < (10 if name == "grill-me" else 120):
                errors.append(f"{agent}/{name}: missing or incomplete skill body")
            if not list(path.parent.glob("LICENSE*")):
                warnings.append(f"{agent}/{name}: no standalone LICENSE; see compatibility notes")
            documents.append(path)
        print(f"{agent}: {len(disk)} skills, {len(identifiers)} plugin records")

    market = json.loads((root / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    paths = [path for plugin in market["plugins"] for path in plugin.get("skills", [])]
    if any(not path.startswith("./claude-code/skills/") for path in paths):
        errors.append("Claude marketplace points outside claude-code/skills")
    if len(paths) != len(set(paths)) or {Path(path).name for path in paths} != inventories["claude-code"]:
        errors.append("Claude marketplace and Claude skill inventory do not agree")
    for path in paths:
        if not (root / path / "SKILL.md").is_file():
            errors.append(f"Missing marketplace skill: {path}")
    pi = json.loads((root / "pi/package.json").read_text(encoding="utf-8"))
    if pi.get("pi", {}).get("skills") != ["./skills"]:
        errors.append("Pi package must load its own skills directory")
    extension = root / "pi/extensions/compact-status"
    package = json.loads((extension / "package.json").read_text(encoding="utf-8"))
    for entry in package["pi"]["extensions"]:
        if not (extension / entry).is_file():
            errors.append(f"Missing local Pi extension: {entry}")
    for path in documents:
        for number, target in broken_links(path):
            errors.append(f"{path.relative_to(root)}:{number}: missing local link {target}")
    for message in warnings:
        print(f"WARN: {message}")
    for message in errors:
        print(f"FAIL: {message}", file=sys.stderr)
    if not errors:
        print("PASS: per-agent inventories, marketplace, Pi entries and documentation links agree.")
    return 1 if errors else 0


if __name__ == "__main__":
    try:
        sys.exit(check(Path(__file__).resolve().parent.parent))
    except (OSError, ValueError, KeyError) as error:
        sys.exit(f"FAIL: {error}")
