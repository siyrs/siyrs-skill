from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]

class CommandContractTests(unittest.TestCase):
    def text(self, rel): return (ROOT/rel).read_text(encoding="utf-8").lower()
    def test_one_skill_manifest(self):
        self.assertEqual(1,len([p for p in ROOT.rglob("*") if p.is_file() and p.name.lower()=="skill.md"]))
    def test_git_commit_is_local_and_index_authoritative(self):
        t=self.text("commands/git-commit.md")
        self.assertIn("local-only",t); self.assertIn("git index",t); self.assertIn("must not contact",t)
        self.assertNotIn("scan_secrets.py --root <repo> --git-changes",t)
    def test_sync_reuses_commit_and_scans_history(self):
        t=self.text("commands/git-sync.md")
        self.assertIn("commands/git-commit.md",t)
        self.assertIn("outgoing history",t)
        self.assertIn("shared risk authorization ledger",t)
    def test_risk_override_is_scanned_and_audited(self):
        t=self.text("references/risk-authorization.md")
        self.assertIn("still run the scan",t)
        self.assertIn("--allow-risk",t)
        self.assertIn("do not ask the user again",t)
    def test_common_testing_policy_is_loaded(self):
        for rel in ("commands/test-add.md","commands/test-run-t1.md","commands/test-run-t2.md","commands/test-run-t3.md"):
            self.assertIn("references/testing-common.md",(ROOT/rel).read_text(encoding="utf-8"))
    def test_tier_policy_is_loaded(self):
        for rel in ("commands/test-add.md","commands/test-run-t1.md","commands/test-run-t2.md","commands/test-run-t3.md"):
            self.assertIn("references/testing-tiers.md",(ROOT/rel).read_text(encoding="utf-8"))
    def test_bundled_helpers_use_skill_dir_placeholder(self):
        for rel in ("SKILL.md","commands/test-add.md","commands/test-run-t1.md","commands/test-run-t2.md","commands/test-run-t3.md","commands/git-commit.md","commands/git-sync.md"):
            self.assertNotIn("python scripts/",(ROOT/rel).read_text(encoding="utf-8"))
if __name__=="__main__": unittest.main()
