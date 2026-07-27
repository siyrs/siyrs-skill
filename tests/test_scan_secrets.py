# siyk-secret-scan: allow-test-fixture
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from scan_secrets import scan


class SecretScanTests(unittest.TestCase):
    def test_private_key_blocks(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "bad.pem").write_text("-----BEGIN PRIVATE KEY-----\nabc", encoding="utf-8")
            result = scan(root, changed_only=False)
            self.assertTrue(result["high_confidence_block"])
            self.assertTrue(any(f["kind"] == "private-key" for f in result["findings"]))

    def test_allow_fixture_marker_only_suppresses_test_fixture(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture = root / "tests" / "fixtures" / "fixture.py"
            fixture.parent.mkdir(parents=True)
            fixture.write_text(
                "# siyk-secret-scan: allow-test-fixture\n-----BEGIN PRIVATE KEY-----\nabc",
                encoding="utf-8",
            )
            result = scan(root, changed_only=False)
            self.assertFalse(result["high_confidence_block"])
            self.assertEqual([], result["findings"])

    def test_marker_outside_fixture_does_not_bypass(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "app.py"
            path.write_text(
                "# siyk-secret-scan: allow-test-fixture\n-----BEGIN PRIVATE KEY-----\nabc",
                encoding="utf-8",
            )
            result = scan(root, changed_only=False)
            self.assertTrue(result["high_confidence_block"])
            kinds = {item["kind"] for item in result["findings"]}
            self.assertIn("invalid-fixture-allow-marker", kinds)
            self.assertIn("private-key", kinds)

    def test_known_token_pattern_blocks(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "bad.txt").write_text("sk-1234567890abcdefghijklmnop", encoding="utf-8")
            result = scan(root, changed_only=False)
            self.assertTrue(result["high_confidence_block"])
            self.assertTrue(any(f["kind"] == "openai-style-key" for f in result["findings"]))

    def test_git_changes_supports_space_paths(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init"], cwd=root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (root / "space file.txt").write_text("hello", encoding="utf-8")
            result = scan(root, changed_only=True)
            self.assertEqual(1, result["files_scanned"])

    def test_normal_source_is_clean(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "app.py").write_text("print('hello')\n", encoding="utf-8")
            result = scan(root, changed_only=False)
            self.assertFalse(result["high_confidence_block"])
            self.assertEqual([], result["findings"])


if __name__ == "__main__":
    unittest.main()
