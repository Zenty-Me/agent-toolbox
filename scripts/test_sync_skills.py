import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from sync_skills import AGENTS, sync


class SkillSyncTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "repo"
        self.local = Path(self.temporary.name) / "local"
        self.local.mkdir()
        for agent in AGENTS:
            (self.root / agent / "skills").mkdir(parents=True)
            (self.root / agent / "plugins.json").write_text(json.dumps({"skills": ["sample"]}))

    def put(self, directory, name="sample", body="original"):
        path = directory / name / "SKILL.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"---\nname: {name}\n---\n{body}\n", encoding="utf-8", newline="\n")
        return path

    def run_sync(self, agent="pi", direction="import", names=None, **options):
        with contextlib.redirect_stdout(io.StringIO()):
            return sync(self.root, agent, direction, names or ["sample"], self.local, **options)

    def test_preview_never_writes(self):
        self.put(self.local)
        self.assertEqual(self.run_sync(), 1)
        self.assertFalse((self.root / "pi/skills/sample").exists())

    def test_any_conflict_stops_all_writes(self):
        target = self.put(self.root / "pi/skills", body="repository fix")
        self.put(self.local, body="older installed version")
        self.put(self.local, name="another")
        with self.assertRaisesRegex(ValueError, "Conflicts"):
            self.run_sync(names=["sample", "another"], apply=True)
        self.assertIn("repository fix", target.read_text())
        self.assertFalse((self.root / "pi/skills/another").exists())

    def test_explicit_replace_preserves_license_and_other_agents(self):
        target = self.put(self.root / "pi/skills", body="repository fix")
        license_file = target.parent / "LICENSE"
        license_file.write_text("preserved upstream license")
        other = self.put(self.root / "codex/skills", body="independent Codex version")
        self.put(self.local, body="reviewed local change")
        self.run_sync(apply=True, replace=True)
        self.assertIn("reviewed local change", target.read_text())
        self.assertEqual(license_file.read_text(), "preserved upstream license")
        self.assertIn("independent Codex version", other.read_text())

    def test_export_copies_resources_and_leaves_target_only_files(self):
        source = self.put(self.root / "claude-code/skills")
        (source.parent / "resources").mkdir()
        (source.parent / "resources/data.bin").write_bytes(b"\x00\xff\r\n")
        local = self.put(self.local)
        (local.parent / "local-note.txt").write_text("keep")
        self.run_sync("claude-code", "export", apply=True)
        self.assertEqual((local.parent / "resources/data.bin").read_bytes(), b"\x00\xff\r\n")
        self.assertEqual((local.parent / "local-note.txt").read_text(), "keep")

    def test_invalid_name_and_mismatched_frontmatter_are_rejected(self):
        for name in ["../pi", "other/sample", "", "Sample"]:
            with self.subTest(name=name), self.assertRaises(ValueError):
                self.run_sync(names=[name], apply=True)
        path = self.put(self.local)
        path.write_text("---\nname: another\n---\nbody\n")
        with self.assertRaisesRegex(ValueError, "frontmatter"):
            self.run_sync(apply=True)

    def test_missing_explicit_source_and_unknown_export_fail(self):
        with self.assertRaisesRegex(ValueError, "no SKILL.md"):
            self.run_sync(apply=True)
        with self.assertRaisesRegex(ValueError, "not listed"):
            self.run_sync(direction="export", names=["unlisted"], apply=True)

    def test_only_line_endings_differ_so_no_replacement(self):
        source = self.put(self.local)
        target = self.put(self.root / "pi/skills")
        windows_bytes = source.read_bytes().replace(b"\n", b"\r\n")
        target.write_bytes(windows_bytes)
        self.assertEqual(self.run_sync(apply=True), 0)
        self.assertEqual(target.read_bytes(), windows_bytes)

    def test_target_symlink_never_changes_shared_installation(self):
        shared = self.local / "shared"
        self.put(shared)
        self.put(self.root / "pi/skills", body="exported")
        try:
            (self.local / "sample").symlink_to(shared / "sample", target_is_directory=True)
        except OSError:
            self.skipTest("Creating symlinks requires platform permission")
        with self.assertRaisesRegex(ValueError, "Target symlink"):
            self.run_sync(direction="export", apply=True, replace=True)
        self.assertIn("original", (shared / "sample/SKILL.md").read_text())

    @unittest.skipUnless(os.name == "nt", "Windows junction check")
    def test_windows_junction_does_not_modify_shared_installation(self):
        shared = self.local / "shared"
        original = self.put(shared)
        self.put(self.root / "pi/skills", body="exported")
        junction = self.local / "sample"
        result = subprocess.run(["cmd.exe", "/d", "/c", "mklink", "/J", str(junction), str(original.parent)],
                                capture_output=True)
        if result.returncode:
            self.skipTest("Creating junctions is unavailable")
        with self.assertRaisesRegex(ValueError, "junction"):
            self.run_sync(direction="export", apply=True, replace=True)
        self.assertIn("original", original.read_text())
        junction.rmdir()

    def test_binary_line_endings_are_not_treated_as_equal(self):
        source = self.put(self.local)
        target = self.put(self.root / "pi/skills")
        (source.parent / "data.bin").write_bytes(b"\0a\r\n")
        (target.parent / "data.bin").write_bytes(b"\0a\n")
        with self.assertRaisesRegex(ValueError, "Conflicts"):
            self.run_sync(apply=True)


if __name__ == "__main__":
    unittest.main()
