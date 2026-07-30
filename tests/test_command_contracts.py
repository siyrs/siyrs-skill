from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Contracts(unittest.TestCase):
    def text(self, path):
        return (ROOT / path).read_text(encoding="utf-8").lower()

    def test_git_commit_is_audit_only_by_default(self):
        text = self.text("commands/git-commit.md")
        self.assertIn("--phase index", text)
        self.assertIn("does not run or author tests by default", text)
        self.assertIn("cannot trigger testing", text)
        self.assertNotIn("promote-t1", text)
        self.assertNotIn("default embedded t1", text)

    def test_git_sync_is_audit_only_by_default(self):
        text = self.text("commands/git-sync.md")
        self.assertIn("--phase outgoing", text)
        self.assertIn("does not run or author tests by default", text)
        self.assertIn("pr creation does not imply t2", text)
        self.assertNotIn("post-integration t1", text)
        self.assertNotIn("execute configured post-integration", text)

    def test_sync_branch_is_explicit(self):
        text = self.text("commands/git-sync.md")
        self.assertIn("--branch <branch>", text)
        self.assertIn("positional natural language is never treated as a branch", text)

    def test_config_plan_references(self):
        for path in ("commands/test-run-t1.md", "commands/test-run-t2.md", "commands/test-run-t3.md"):
            text = self.text(path)
            self.assertIn("siyk.py plan", text)
            self.assertIn("testing-documentation.md", text)
            self.assertIn("docs validate", text)

    def test_natural_language_full_and_uat_discovery(self):
        text = self.text("SKILL.md")
        self.assertIn("全量测试", text)
        self.assertIn("uat", text)
        self.assertIn("docs/testing/readme.md", text)


if __name__ == "__main__":
    unittest.main()
