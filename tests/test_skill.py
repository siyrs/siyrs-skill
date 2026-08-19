from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import install  # noqa: E402
import sync_references  # noqa: E402
import validate  # noqa: E402

EXPECTED_SKILLS = {
    "siyrs-skill",
    "siyk-init",
    "siyk-test-add",
    "siyk-test-add-t3",
    "siyk-test-run-t1",
    "siyk-test-run-t2",
    "siyk-test-run-t3",
    "siyk-git-commit",
    "siyk-git-sync",
}


def skill_dirs(root: Path = ROOT) -> list[Path]:
    return sync_references.discover_skill_dirs(root)


def frontmatter(skill_path: Path) -> dict[str, str]:
    return validate.parse_frontmatter(skill_path.read_text(encoding="utf-8"))


class NativeCollectionTests(unittest.TestCase):
    def test_collection_validates(self) -> None:
        self.assertEqual([], validate.validate(ROOT))

    def test_collection_root_is_not_a_runtime_skill(self) -> None:
        for path in ("SKILL.md", "agents", "references", ".claude-plugin"):
            self.assertFalse((ROOT / path).exists(), path)

    def test_exact_peer_skill_set_is_discovered(self) -> None:
        self.assertEqual(EXPECTED_SKILLS, {path.name for path in skill_dirs()})

    def test_each_skill_is_standalone_and_named_after_parent(self) -> None:
        for skill_dir in skill_dirs():
            skill_path = skill_dir / "SKILL.md"
            meta = frontmatter(skill_path)
            self.assertEqual(skill_dir.name, meta["name"])
            self.assertTrue(meta["description"])
            self.assertTrue((skill_dir / "references").is_dir(), skill_dir.name)
            self.assertTrue((skill_dir / "agents" / "openai.yaml").is_file())
            self.assertFalse((skill_dir / "skills").exists())
            self.assertNotIn("../../", skill_path.read_text(encoding="utf-8"))

    def test_source_frontmatter_is_strict_agent_skills(self) -> None:
        for skill_dir in skill_dirs():
            meta = frontmatter(skill_dir / "SKILL.md")
            self.assertTrue(set(meta).issubset(validate.ALLOWED_FRONTMATTER_FIELDS))
            self.assertNotIn("disable-model-invocation", meta)

    def test_main_and_explicit_descriptions_are_asymmetric(self) -> None:
        main = frontmatter(ROOT / "skills" / "siyrs-skill" / "SKILL.md")
        self.assertIn("软件仓库", main["description"])
        self.assertIn("Git", main["description"])
        for skill_dir in skill_dirs():
            if not skill_dir.name.startswith("siyk-"):
                continue
            description = frontmatter(skill_dir / "SKILL.md")["description"]
            self.assertLessEqual(len(description), 80, skill_dir.name)

    def test_openai_invocation_policy_is_correct(self) -> None:
        for skill_dir in skill_dirs():
            text = (skill_dir / "agents" / "openai.yaml").read_text(encoding="utf-8")
            expected = "true" if skill_dir.name == "siyrs-skill" else "false"
            self.assertIn(f"allow_implicit_invocation: {expected}", text, skill_dir.name)
            self.assertIn(f"${skill_dir.name}", text, skill_dir.name)

    def test_shared_references_are_fully_materialized(self) -> None:
        self.assertEqual([], sync_references.reference_sync_errors(ROOT))
        for skill_dir in skill_dirs():
            required = sync_references.required_reference_paths(ROOT, skill_dir)
            actual = {
                path.relative_to(skill_dir / "references")
                for path in (skill_dir / "references").glob("*.md")
            }
            self.assertEqual(required, actual, skill_dir.name)

    def test_materialized_references_match_canonical_source(self) -> None:
        shared = ROOT / "shared" / "references"
        for skill_dir in skill_dirs():
            for copied in (skill_dir / "references").glob("*.md"):
                canonical = shared / copied.name
                self.assertEqual(canonical.read_bytes(), copied.read_bytes(), str(copied))

    def test_runtime_markdown_links_stay_inside_each_skill(self) -> None:
        for skill_dir in skill_dirs():
            self.assertEqual([], validate._validate_markdown_links(skill_dir), skill_dir.name)

    def test_markdown_first_and_fact_first_contract_survives(self) -> None:
        text = (ROOT / "shared" / "references" / "principles.md").read_text(encoding="utf-8")
        self.assertIn("Markdown-first", text)
        self.assertIn("事实优先，不懂不猜", text)
        self.assertIn("不得依赖 Skill 根目录之外", text)

    def test_testing_contract_survives_collection_refactor(self) -> None:
        testing = (ROOT / "shared" / "references" / "testing.md").read_text(encoding="utf-8")
        tiers = (ROOT / "shared" / "references" / "testing-tiers.md").read_text(encoding="utf-8")
        for expected in (
            "docs/testing/README.md",
            "默认按业务模块而不是按 unit/integration/e2e 类型拆文件",
            "P0 · T2 · E2E",
            "不要为测试设计建立额外 JSON/YAML state、matrix、registry",
        ):
            self.assertIn(expected, testing)
        self.assertIn("T1 — 变更回归", tiers)
        self.assertIn("T2 — 标准 Smoke", tiers)
        self.assertIn("T3 — 深度业务验收 / 发布级验证", tiers)
        self.assertIn("UAT 通过", tiers)
        self.assertIn("不自动等于 T3 通过", tiers)

    def test_t3_deep_design_contract_survives(self) -> None:
        text = (ROOT / "shared" / "references" / "testing-t3-design.md").read_text(encoding="utf-8")
        for expected in (
            "全局理解，但不自动全局测试",
            "Business Invariants",
            "Test Oracle",
            "Impact Propagation",
            "Impact Isolation",
            "从业务事件设计，而不是从按钮设计",
            "多角色与连续业务旅程",
            "Test Critic",
            "子代理是推理策略，不是运行依赖",
            "Markdown-first 沉淀",
        ):
            self.assertIn(expected, text)

    def test_claude_variant_is_generated_from_same_skills(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "skills"
            built = install.build_claude_skills(ROOT, output)
            self.assertEqual(EXPECTED_SKILLS, {path.name for path in built})
            for skill_dir in built:
                meta = frontmatter(skill_dir / "SKILL.md")
                if skill_dir.name == "siyrs-skill":
                    self.assertNotIn("disable-model-invocation", meta)
                else:
                    self.assertEqual("true", meta.get("disable-model-invocation"))
                self.assertFalse((skill_dir / "agents").exists())
                self.assertEqual([], validate._validate_markdown_links(skill_dir))

    def test_claude_generation_does_not_modify_source(self) -> None:
        before = {
            path: path.read_bytes()
            for path in ROOT.glob("skills/*/SKILL.md")
        }
        with tempfile.TemporaryDirectory() as tmp:
            install.build_claude_skills(ROOT, Path(tmp) / "skills")
        after = {path: path.read_bytes() for path in before}
        self.assertEqual(before, after)

    def test_install_creates_nine_peer_links_for_both_hosts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            results = install.install(ROOT, home, target="all")
            self.assertEqual(18, len(results))
            self.assertEqual([], install.check_install(ROOT, home, target="all"))
            for name in EXPECTED_SKILLS:
                self.assertTrue((home / ".agents" / "skills" / name / "SKILL.md").is_file())
                self.assertTrue((home / ".claude" / "skills" / name / "SKILL.md").is_file())

    def test_install_refuses_collection_inside_host_search_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            source = home / ".agents" / "skills" / "collection"
            source.mkdir(parents=True)
            with self.assertRaises(RuntimeError):
                install.ensure_neutral_source(source, home)

    def test_install_does_not_replace_real_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "target"
            link = root / "link"
            target.mkdir()
            link.mkdir()
            with self.assertRaises(RuntimeError):
                install.ensure_link(link, target, repair_links=True)

    def test_check_detects_legacy_claude_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            install.install(ROOT, home, target="all")
            command = home / ".claude" / "commands" / "siyk-init.md"
            command.parent.mkdir(parents=True)
            command.write_text("legacy", encoding="utf-8")
            errors = install.check_install(ROOT, home, target="claude")
            self.assertTrue(any("旧 command" in error for error in errors))

    def test_check_detects_project_level_duplicate_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            project = Path(tmp) / "project"
            install.install(ROOT, home, target="all")
            duplicate = project / ".claude" / "skills" / "duplicate"
            duplicate.mkdir(parents=True)
            duplicate.joinpath("SKILL.md").write_text(
                "---\nname: siyk-init\ndescription: duplicate\n---\n",
                encoding="utf-8",
            )
            errors = install.check_install(
                ROOT,
                home,
                target="claude",
                project_root=project,
            )
            self.assertTrue(any("重复 Skill siyk-init" in error for error in errors))

    def test_reference_sync_repairs_drift_and_transitive_dependencies(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shared = root / "shared" / "references"
            skill = root / "skills" / "example"
            refs = skill / "references"
            shared.mkdir(parents=True)
            refs.mkdir(parents=True)
            skill.joinpath("SKILL.md").write_text(
                "---\nname: example\ndescription: example\n---\n"
                "See [A](references/a.md).\n",
                encoding="utf-8",
            )
            shared.joinpath("a.md").write_text("See [B](b.md).\n", encoding="utf-8")
            shared.joinpath("b.md").write_text("B\n", encoding="utf-8")
            refs.joinpath("a.md").write_text("stale\n", encoding="utf-8")
            self.assertTrue(sync_references.reference_sync_errors(root))
            sync_references.sync_references(root)
            self.assertEqual([], sync_references.reference_sync_errors(root))
            self.assertTrue(refs.joinpath("b.md").is_file())

    def test_readme_documents_native_collection_installation(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Agent Skills Collection", readme)
        self.assertIn("$HOME/.siyrs/siyrs-skill", readme)
        self.assertIn("scripts/install.py", readme)
        self.assertIn("不把整个 Collection clone", readme)
        self.assertIn("/siyrs-skill", readme)
        self.assertIn("$siyrs-skill", readme)

    def test_docs_and_version_are_aligned(self) -> None:
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual("0.7.0", version)
        self.assertIn("v0.7.0", (ROOT / "README.md").read_text(encoding="utf-8"))
        self.assertIn("## 0.7.0", (ROOT / "docs" / "CHANGELOG.md").read_text(encoding="utf-8"))
        for name in ("README.md", "architecture.md", "CONTRIBUTING.md", "plan.md", "CHANGELOG.md"):
            self.assertTrue((ROOT / "docs" / name).is_file(), name)

    def test_no_runtime_framework_is_reintroduced(self) -> None:
        for path in (
            "adapters",
            "commands",
            "schemas",
            "release-manifest.json",
            ".claude-plugin",
        ):
            self.assertFalse((ROOT / path).exists(), path)


if __name__ == "__main__":
    unittest.main()
