from pathlib import Path
import tempfile
import unittest

from check_consistency import broken_links


class DocumentationLinksTests(unittest.TestCase):
    def test_frontmatter_patterns_and_code_are_not_links(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "SKILL.md"
            path.write_text('''---
name: sample
pattern: "[abc](next/server)"
---
# Skill

```python
pattern = "[abc](missing-code-path)"
```
[Reference](missing.md)
''', encoding="utf-8")
            self.assertEqual(list(broken_links(path)), [(10, "missing.md")])

    def test_existing_encoded_path_and_remote_links_pass(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "a b.md").write_text("# Reference")
            path = root / "README.md"
            path.write_text("[Local](a%20b.md#anchor)\n[Remote](https://example.com/x)\n", encoding="utf-8")
            self.assertEqual(list(broken_links(path)), [])


if __name__ == "__main__":
    unittest.main()
