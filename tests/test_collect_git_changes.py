from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from collect_git_changes import collect


def git(root: Path, *args: str) -> str:
    cp = subprocess.run(
        ["git", *args], cwd=root, text=True, encoding="utf-8",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
    )
    return cp.stdout.strip()


def init_repo(root: Path) -> None:
    git(root, "init")
    git(root, "config", "user.email", "test@example.com")
    git(root, "config", "user.name", "Test")


class CollectGitChangesTests(unittest.TestCase):
    def test_collects_staged_unstaged_untracked_and_space_paths(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_repo(root)
            (root / "a file.txt").write_text("one\n", encoding="utf-8")
            git(root, "add", "a file.txt")
            git(root, "commit", "-m", "initial")
            head = git(root, "rev-parse", "HEAD")

            (root / "a file.txt").write_text("two\n", encoding="utf-8")
            (root / "staged.txt").write_text("staged\n", encoding="utf-8")
            git(root, "add", "staged.txt")
            (root / "未跟踪 文件.txt").write_text("new\n", encoding="utf-8")

            result = collect(root, head)
            self.assertTrue(result["is_git_repository"])
            self.assertEqual(head, result["baseline"])
            self.assertIn("a file.txt", result["changed_files"])
            self.assertIn("staged.txt", result["changed_files"])
            self.assertIn("未跟踪 文件.txt", result["untracked_files"])
            self.assertTrue(any(item["path"] == "staged.txt" for item in result["staged_changes"]))
            self.assertTrue(any(item["path"] == "a file.txt" for item in result["unstaged_changes"]))

    def test_unborn_repository_is_reported(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_repo(root)
            (root / "first.txt").write_text("x", encoding="utf-8")
            result = collect(root)
            self.assertTrue(result["is_git_repository"])
            self.assertTrue(result["unborn_head"])
            self.assertIsNone(result["head"])
            self.assertIn("first.txt", result["untracked_files"])

    def test_invalid_explicit_baseline_is_reported(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_repo(root)
            (root / "a.txt").write_text("one", encoding="utf-8")
            git(root, "add", "a.txt")
            git(root, "commit", "-m", "initial")
            result = collect(root, "does-not-exist")
            self.assertIsNone(result["baseline"])
            self.assertIn("not a commit", result["baseline_error"])

    def test_non_git_directory(self):
        with TemporaryDirectory() as tmp:
            result = collect(Path(tmp))
            self.assertFalse(result["is_git_repository"])


if __name__ == "__main__":
    unittest.main()
