from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CommandContractTests(unittest.TestCase):
    def test_manifest_routes_all_commands(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        for command in ("/siyk-test-full", "/siyk-test-new", "/siyk-git-commit", "/siyk-git-sync"):
            self.assertIn(command, text)

    def test_command_docs_have_completion_language(self):
        for rel in ("commands/test-full.md", "commands/test-new.md", "commands/git-commit.md", "commands/git-sync.md"):
            text = (ROOT / rel).read_text(encoding="utf-8").lower()
            self.assertTrue("completion" in text or "report" in text)

    def test_only_one_skill_manifest(self):
        manifests = [p for p in ROOT.rglob("*") if p.is_file() and p.name.lower() == "skill.md"]
        self.assertEqual(1, len(manifests))

    def test_bundled_helpers_use_skill_dir_placeholder(self):
        for rel in ("SKILL.md", "commands/test-full.md", "commands/test-new.md", "commands/git-commit.md", "commands/git-sync.md"):
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertNotIn("python scripts/", text)
        self.assertIn("<skill-dir>/scripts/detect_project.py", (ROOT / "SKILL.md").read_text(encoding="utf-8"))

    def test_local_commit_command_forbids_remote_mutation(self):
        text = (ROOT / "commands/git-commit.md").read_text(encoding="utf-8").lower()
        self.assertIn("local-only", text)
        self.assertIn("must not fetch", text)
        self.assertIn("remote result: not contacted and not modified", text)


if __name__ == "__main__":
    unittest.main()
