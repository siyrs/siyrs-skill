from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from fingerprint import fingerprint


def git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


class FingerprintTests(unittest.TestCase):
    def test_plain_directory_changes_fingerprint(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            file = root / "a.txt"
            file.write_text("one", encoding="utf-8")
            first = fingerprint(root)["sha256"]
            file.write_text("two", encoding="utf-8")
            second = fingerprint(root)["sha256"]
            self.assertNotEqual(first, second)

    def test_excluded_directory_does_not_change_plain_fingerprint(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.txt").write_text("one", encoding="utf-8")
            first = fingerprint(root)["sha256"]
            (root / "node_modules").mkdir()
            (root / "node_modules/x.js").write_text("noise", encoding="utf-8")
            second = fingerprint(root)["sha256"]
            self.assertEqual(first, second)

    def test_git_staged_and_untracked_space_path_change_fingerprint(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            git(root, "init")
            git(root, "config", "user.email", "test@example.com")
            git(root, "config", "user.name", "Test")
            (root / "a.txt").write_text("one", encoding="utf-8")
            git(root, "add", "a.txt")
            git(root, "commit", "-m", "initial")
            first = fingerprint(root)["sha256"]
            (root / "space file.txt").write_text("new", encoding="utf-8")
            second = fingerprint(root)["sha256"]
            self.assertNotEqual(first, second)
            git(root, "add", "space file.txt")
            third = fingerprint(root)["sha256"]
            self.assertNotEqual(second, third)


if __name__ == "__main__":
    unittest.main()
