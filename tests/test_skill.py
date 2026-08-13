from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate.py"
spec = importlib.util.spec_from_file_location("skill_validate", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)


class SkillStructureTests(unittest.TestCase):
    def test_canonical_skill_validates(self) -> None:
        self.assertEqual([], validator.validate(ROOT))

    def test_skill_stays_compact(self) -> None:
        lines = (ROOT / "SKILL.md").read_text(encoding="utf-8").splitlines()
        self.assertLess(len(lines), 200)

    def test_legacy_runtime_layers_are_gone(self) -> None:
        for path in ("adapters", "commands", "schemas", "release-manifest.json"):
            self.assertFalse((ROOT / path).exists(), path)

    def test_git_shortcuts_are_thin_skill_contracts(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        git = (ROOT / "references" / "git.md").read_text(encoding="utf-8")
        for shortcut in ("siyk-git-commit", "siyk-git-sync"):
            self.assertIn(shortcut, skill)
            self.assertIn(shortcut, git)
        self.assertFalse((ROOT / "commands").exists())
        self.assertFalse((ROOT / "adapters").exists())

    def test_invalid_frontmatter_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "SKILL.md").write_text("# no frontmatter\n", encoding="utf-8")
            errors = validator.validate(root)
            self.assertTrue(any("frontmatter" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
