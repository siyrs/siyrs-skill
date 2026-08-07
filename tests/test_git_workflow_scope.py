from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from config_model import DEFAULT_CONFIG, load_config
from route_command import route


class GitWorkflowScopeTests(unittest.TestCase):
    def test_default_preflight_is_none(self):
        self.assertEqual(
            {"commit": "none", "sync_after_integration": "none", "pr": "none"},
            DEFAULT_CONFIG["testing"]["preflight"],
        )

    def test_legacy_preflight_values_warn(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".siyrs").mkdir()
            (root / ".siyrs/config.yaml").write_text(
                """version: 2
testing:
  preflight:
    commit: t1
    sync_after_integration: t1
    pr: t2
""",
                encoding="utf-8",
            )
            loaded = load_config(root)
            self.assertTrue(loaded["valid"], loaded["errors"])
            self.assertEqual(3, len([w for w in loaded["warnings"] if "deprecated and ignored" in w]))

    def test_no_test_flag_is_compatibility_noop(self):
        result = route("/siyk-git-sync --no-test", ROOT)
        self.assertTrue(result["valid"])
        self.assertIn("--no-test", result["flags"])
        self.assertTrue(any("already disable tests by default" in w for w in result["warnings"]))

    def test_git_docs_are_short_git_only_workflows(self):
        commit = (ROOT / "commands/git-commit.md").read_text(encoding="utf-8").casefold()
        sync = (ROOT / "commands/git-sync.md").read_text(encoding="utf-8").casefold()
        combined = commit + "\n" + sync

        for forbidden in (
            "promote-t1",
            "docs validate",
            "reachable large objects",
            "large-object inventory",
        ):
            self.assertNotIn(forbidden, combined)

        self.assertIn("quick privacy check", commit)
        self.assertIn("quick privacy check", sync)
        self.assertIn("git diff --cached", commit)
        self.assertIn("git push", sync)
        self.assertIn("opt-in only", commit)
        self.assertIn("opt-in only", sync)
        self.assertIn("do not run it during a normal save", commit)
        self.assertIn("do not run it during normal synchronization", sync)

    def test_git_docs_do_not_make_validation_decisions_for_user(self):
        combined = "\n".join(
            (ROOT / path).read_text(encoding="utf-8").casefold()
            for path in ("commands/git-commit.md", "commands/git-sync.md")
        )
        self.assertIn("user will", combined)
        for forbidden in ("execute t1", "execute t2", "execute t3", "execute uat"):
            self.assertNotIn(forbidden, combined)


if __name__ == "__main__":
    unittest.main()
