from pathlib import Path
from tempfile import TemporaryDirectory
import shutil
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_bundle import validate


class BundleValidationTests(unittest.TestCase):
    def test_current_bundle_is_valid(self):
        result = validate(ROOT)
        self.assertTrue(result["valid"], result["errors"])
        self.assertEqual("0.1.5", result["version"])

    def test_version_drift_is_detected(self):
        with TemporaryDirectory() as tmp:
            copy = Path(tmp) / "skill"
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
            (copy / "VERSION").write_text("9.9.9\n", encoding="utf-8")
            result = validate(copy)
            self.assertFalse(result["valid"])

    def test_codex_entrypoint_name_drift_is_detected(self):
        with TemporaryDirectory() as tmp:
            copy = Path(tmp) / "skill"
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
            template = copy / "adapters/codex/entrypoints/siyk-test-full/SKILL.template.md"
            template.write_text(template.read_text(encoding="utf-8").replace("name: siyk-test-full", "name: wrong-name"), encoding="utf-8")
            result = validate(copy)
            self.assertFalse(result["valid"])
            self.assertTrue(any("Codex entrypoint name mismatch" in error for error in result["errors"]))


if __name__ == "__main__":
    unittest.main()
