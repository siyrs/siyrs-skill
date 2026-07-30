from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from testing_docs import ensure_workspace, index_workspace, resolve_workspace, validate_workspace


class TestingDocumentationTests(unittest.TestCase):
    def test_default_and_user_resolution_precedence(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            default = resolve_workspace(root)
            self.assertEqual("docs/testing", default.docs_root)
            self.assertEqual("docs/testing/README.md", default.entry)

            (root / ".siyrs").mkdir()
            (root / ".siyrs/config.yaml").write_text(
                """version: 2
testing:
  documentation:
    root: qa/contracts
    index: INDEX.md
    evidence_root: runs
""",
                encoding="utf-8",
            )
            configured = resolve_workspace(root)
            self.assertEqual("qa/contracts/INDEX.md", configured.entry)
            self.assertEqual("config", configured.source)
            explicit = resolve_workspace(root, entry="custom/tests/home.md")
            self.assertEqual("custom/tests/home.md", explicit.entry)
            self.assertEqual("user-entry", explicit.source)

    def test_case_insensitive_index_is_reused(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs/testing"
            docs.mkdir(parents=True)
            (docs / "readme.md").write_text("# Existing\n", encoding="utf-8")
            workspace = resolve_workspace(root)
            self.assertEqual("readme.md", workspace.index)
            ensure_workspace(root)
            entry_names = {path.name for path in docs.iterdir()}
            self.assertIn("readme.md", entry_names)
            self.assertNotIn("README.md", entry_names)

    def test_ensure_creates_minimum_workspace_and_managed_index(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = ensure_workspace(root)
            self.assertTrue((root / "docs/testing/README.md").is_file())
            self.assertTrue((root / "docs/testing/00-test-governance.md").is_file())
            self.assertTrue((root / "docs/testing/00-test-tiers.md").is_file())
            self.assertTrue((root / "docs/testing/evidence").is_dir())
            readme = (root / "docs/testing/README.md").read_text(encoding="utf-8")
            self.assertIn("Agent discovery contract", readme)
            self.assertIn("00-test-governance.md", readme)
            self.assertTrue(result["created"])

    def test_index_preserves_rich_content(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            ensure_workspace(root)
            readme = root / "docs/testing/README.md"
            readme.write_text(readme.read_text(encoding="utf-8") + "\n## Project-specific rich section\nKeep me.\n", encoding="utf-8")
            module = root / "docs/testing/01-account.md"
            module.write_text(
                """---
siyrs_testing_document: 1
document_type: case-module
title: "Account cases"
module: "account"
case_prefixes: ["TC-ACCOUNT"]
platforms: ["backend", "frontend", "android"]
indexed: true
---
# Account cases
""",
                encoding="utf-8",
            )
            index_workspace(root)
            text = readme.read_text(encoding="utf-8")
            self.assertIn("Project-specific rich section", text)
            self.assertIn("01-account.md", text)
            self.assertIn("backend, frontend, android", text)

    def test_validation_distinguishes_definitions_references_and_t2_debt(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            ensure_workspace(root)
            docs = root / "docs/testing"
            (docs / "01-account.md").write_text(
                """---
siyrs_testing_document: 1
document_type: case-module
module: account
case_prefixes: ["TC-ACCOUNT"]
platforms: ["backend", "frontend"]
indexed: true
---
# Account
| Case ID | Tier | Role | Scenario | Preconditions | Steps | Expected result | Evidence point |
|---|---|---|---|---|---|---|---|
| TC-ACCOUNT-001 | T2 | main-path | login | user | login | success | api/ui/db |
| TC-ACCOUNT-002 | T2 | boundary | denied | no permission | open | forbidden | api/audit |
""",
                encoding="utf-8",
            )
            (docs / "evidence/run.md").write_text(
                """---
siyrs_testing_document: 1
document_type: evidence
platforms: ["backend", "frontend"]
indexed: true
---
# Run
| Run ID | Case IDs | Environment | Result | Evidence |
|---|---|---|---|---|
| RUN-1 | TC-ACCOUNT-001, TC-ACCOUNT-002 | test | passed | report |
""",
                encoding="utf-8",
            )
            index_workspace(root)
            result = validate_workspace(root, strict=True)
            self.assertTrue(result["valid"], result)
            self.assertEqual(2, result["summary"]["canonical_cases"])
            self.assertFalse(result["debts"])

    def test_duplicate_definition_and_orphan_are_reported(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            ensure_workspace(root)
            docs = root / "docs/testing"
            body = """# Cases
| Case ID | Tier | Role | Scenario | Preconditions | Steps | Expected result | Evidence point |
|---|---|---|---|---|---|---|---|
| TC-DUP-001 |  | boundary | x | x | x | x | x |
"""
            for name in ("01-a.md", "02-b.md"):
                (docs / name).write_text(body, encoding="utf-8")
            result = validate_workspace(root)
            self.assertFalse(result["valid"])
            self.assertTrue(any("duplicate canonical" in item for item in result["errors"]))
            self.assertTrue(any("orphan" in item for item in result["debts"]))

    def test_broken_link_is_error(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            ensure_workspace(root)
            readme = root / "docs/testing/README.md"
            readme.write_text(readme.read_text(encoding="utf-8") + "\n[missing](./not-found.md)\n", encoding="utf-8")
            result = validate_workspace(root)
            self.assertFalse(result["valid"])
            self.assertTrue(any("broken relative link" in item for item in result["errors"]))


if __name__ == "__main__":
    unittest.main()
