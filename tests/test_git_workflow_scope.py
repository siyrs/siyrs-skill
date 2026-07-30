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

    def test_git_docs_do_not_default_to_test_state(self):
        combined = "\n".join(
            (ROOT / path).read_text(encoding="utf-8").casefold()
            for path in ("commands/git-commit.md", "commands/git-sync.md")
        )
        for forbidden in ("promote-t1", "docs validate", "testing documentation/evidence updates"):
            self.assertNotIn(forbidden, combined)


if __name__ == "__main__":
    unittest.main()
