from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate.py"
spec = importlib.util.spec_from_file_location("skill_validate", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)


def explicit_skill_dirs() -> list[Path]:
    return [
        path
        for path, explicit_child in validator.discover_skill_dirs(ROOT)
        if explicit_child
    ]


class SkillStructureTests(unittest.TestCase):
    def test_bundle_validates(self) -> None:
        self.assertEqual([], validator.validate(ROOT))

    def test_main_skill_stays_compact(self) -> None:
        lines = (ROOT / "SKILL.md").read_text(encoding="utf-8").splitlines()
        self.assertLess(len(lines), 130)

    def test_main_skill_keeps_public_name(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        agent = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("name: siyrs-skill", skill)
        self.assertIn('display_name: "Siyrs Skill"', agent)
        self.assertIn("$siyrs-skill", agent)
        self.assertNotIn("$siyrs-engineering", agent)

    def test_human_facing_brand_uses_full_skill_name(self) -> None:
        legacy_upper_brand = "SI" + "YRS"
        current_brand_files = (
            ROOT / "README.md",
            ROOT / "SKILL.md",
            ROOT / "agents" / "openai.yaml",
            ROOT / "references" / "principles.md",
            ROOT / "docs" / "README.md",
            ROOT / "docs" / "architecture.md",
            ROOT / "docs" / "plan.md",
            ROOT / "docs" / "CONTRIBUTING.md",
        )
        for path in current_brand_files:
            text = path.read_text(encoding="utf-8")
            self.assertNotIn(legacy_upper_brand, text, str(path))
            self.assertNotIn("Siyrs", text.replace("Siyrs Skill", ""), str(path))

        self.assertIn("# Siyrs Skill", (ROOT / "SKILL.md").read_text(encoding="utf-8"))
        self.assertIn(
            "# Siyrs Skill 第一性原则",
            (ROOT / "references" / "principles.md").read_text(encoding="utf-8"),
        )

    def test_primary_user_facing_copy_is_chinese(self) -> None:
        expectations = {
            ROOT / "SKILL.md": "聚焦完成软件仓库修改",
            ROOT / "agents" / "openai.yaml": "聚焦完成仓库修改",
            ROOT / "references" / "principles.md": "# Siyrs Skill 第一性原则",
            ROOT / "references" / "testing.md": "# 测试指南",
            ROOT / "references" / "testing-tiers.md": "# 测试分级执行合同",
            ROOT / "references" / "project-map.md": "# `.siyrs` 项目地图指南",
            ROOT / "references" / "git.md": "# Git 交付指南",
            ROOT / "docs" / "README.md": "# Siyrs Skill 文档",
            ROOT / "docs" / "architecture.md": "# Siyrs Skill 架构说明",
            ROOT / "docs" / "plan.md": "# Siyrs Skill 演化计划",
            ROOT / "docs" / "CONTRIBUTING.md": "# 贡献指南",
            ROOT / "docs" / "CHANGELOG.md": "# 更新日志",
            ROOT / "README.md": "Markdown-first",
        }
        for path, text in expectations.items():
            self.assertIn(text, path.read_text(encoding="utf-8"), str(path))

    def test_references_are_normative_and_docs_are_explanatory(self) -> None:
        principles = (ROOT / "references" / "principles.md").read_text(encoding="utf-8")
        main_skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        docs_index = (ROOT / "docs" / "README.md").read_text(encoding="utf-8")
        contributing = (ROOT / "docs" / "CONTRIBUTING.md").read_text(encoding="utf-8")

        self.assertIn("权威运行时规范来源", principles)
        self.assertIn("docs/*.md", principles)
        self.assertIn("README 只用于安装、概览和示例", main_skill)
        self.assertIn("README 是说明书", readme)
        self.assertIn("项目维护文档", readme)
        self.assertIn("不承载 Skill 运行时唯一规则", docs_index)
        self.assertIn("docs/*.md", contributing)

    def test_docs_layout_is_shallow_and_plan_is_generic(self) -> None:
        docs = ROOT / "docs"
        for name in (
            "README.md",
            "architecture.md",
            "plan.md",
            "CONTRIBUTING.md",
            "CHANGELOG.md",
        ):
            self.assertTrue((docs / name).is_file(), name)

        self.assertFalse((ROOT / "CONTRIBUTING.md").exists())
        self.assertFalse((ROOT / "CHANGELOG.md").exists())

        architecture = (docs / "architecture.md").read_text(encoding="utf-8")
        plan = (docs / "plan.md").read_text(encoding="utf-8")
        self.assertIn("Convention over Registration", architecture)
        self.assertIn("references/*.md", architecture)
        self.assertIn("真实项目实践", plan)
        self.assertIn("v1.0", plan)
        self.assertIn("当前阶段不为尚未定型的历史混合格式建立长期兼容负担", plan)
        self.assertNotIn("PMP", plan)

    def test_global_first_principles_are_shared(self) -> None:
        principles = (ROOT / "references" / "principles.md").read_text(encoding="utf-8")
        main_skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("Markdown-first", principles)
        self.assertIn("事实优先，不懂不猜", principles)
        self.assertIn("直接询问用户", principles)
        self.assertIn("禁止编造", principles)
        self.assertIn("references/principles.md", main_skill)

        for skill_dir in explicit_skill_dirs():
            text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("../../references/principles.md", text, skill_dir.name)

    def test_child_skills_are_auto_discovered_without_registry(self) -> None:
        validator_source = VALIDATOR_PATH.read_text(encoding="utf-8")
        tests_source = Path(__file__).read_text(encoding="utf-8")
        old_registry_name = "EXPLICIT_" + "SKILLS"
        self.assertNotIn(old_registry_name, validator_source)
        self.assertNotIn(old_registry_name, tests_source)

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            example = root / "skills" / "siyk-example"
            example.mkdir(parents=True)
            discovered = validator.discover_skill_dirs(root)
            self.assertIn((example, True), discovered)

    def test_markdown_first_testing_contract_is_preserved(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        testing = (ROOT / "references" / "testing.md").read_text(encoding="utf-8")

        for text in (skill, testing):
            self.assertIn("docs/testing/README.md", text)
            self.assertIn("standards/", text)
            self.assertIn("cases/", text)
            self.assertIn("reports/", text)

        self.assertIn("standards/priorities.md", testing)
        self.assertIn("standards/release-gate.md", testing)
        self.assertIn("测试代码跟着代码走", testing)
        self.assertIn("默认按业务模块而不是按 unit/integration/e2e 类型拆文件", testing)
        self.assertIn("Markdown-first 用例格式", testing)
        self.assertIn("P0 · T2 · E2E", testing)
        self.assertIn("pmp-vue/e2e/", testing)
        self.assertIn("不为了统一文档而搬迁", testing)

    def test_test_tier_contract_is_orthogonal_and_lightweight(self) -> None:
        tiers = (ROOT / "references" / "testing-tiers.md").read_text(encoding="utf-8")
        self.assertIn("两个正交维度", tiers)
        self.assertIn("T1 — 变更回归", tiers)
        self.assertIn("blast radius", tiers)
        self.assertIn("T2 — 标准 Smoke", tiers)
        self.assertIn("P0 · T2 · E2E", tiers)
        self.assertIn("T3 — 全量 / 发布验收", tiers)
        self.assertIn("docs/testing/reports/<date>-<scope>.md", tiers)
        self.assertIn("UAT 通过", tiers)
        self.assertIn("不自动等于 T3 通过", tiers)
        self.assertIn("默认不做", tiers)
        self.assertIn("创建 state、matrix、evidence registry 或运行时测试治理系统", tiers)
        self.assertNotIn("route_command.py", tiers)

    def test_test_run_skills_are_distinct(self) -> None:
        t1 = (ROOT / "skills" / "siyk-test-run-t1" / "SKILL.md").read_text(encoding="utf-8")
        t2 = (ROOT / "skills" / "siyk-test-run-t2" / "SKILL.md").read_text(encoding="utf-8")
        t3 = (ROOT / "skills" / "siyk-test-run-t3" / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("blast radius", t1)
        self.assertIn("不生成 `docs/testing/reports/`", t1)
        self.assertIn("固定 Smoke", t2)
        self.assertIn("显式 `T2` 标记", t2)
        self.assertIn("不生成 `docs/testing/reports/`", t2)
        self.assertIn("release gate", t3)
        self.assertIn("UAT", t3)
        self.assertIn("docs/testing/reports/<date>-<scope>.md", t3)
        for text in (t1, t2, t3):
            self.assertIn("默认不新增测试", text)
            self.assertIn("不修改业务代码", text)

    def test_project_map_contract_is_preserved(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        project_map = (ROOT / "references" / "project-map.md").read_text(encoding="utf-8")

        self.assertIn(".siyrs/README.md", skill)
        self.assertIn(".siyrs/README.md", project_map)
        self.assertIn("真实代码、构建配置、测试代码和项目文档始终优先", project_map)
        self.assertIn("commit SHA", project_map)
        self.assertIn("Secret 边界", project_map)
        self.assertIn("state.json", project_map)
        self.assertIn("registry.json", project_map)
        self.assertIn("cache/", project_map)

    def test_discovered_child_skills_are_real_explicit_skills(self) -> None:
        for skill_dir in explicit_skill_dirs():
            text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            agent = (skill_dir / "agents" / "openai.yaml").read_text(encoding="utf-8")
            self.assertIn(f"name: {skill_dir.name}", text)
            self.assertIn(f'display_name: "{skill_dir.name}"', agent)
            self.assertIn("allow_implicit_invocation: false", agent)
            self.assertIn(f"${skill_dir.name}", agent)

    def test_test_add_modes_and_scope(self) -> None:
        text = (ROOT / "skills" / "siyk-test-add" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("默认模式：补可执行测试", text)
        self.assertIn("/siyk-test-add e2e", text)
        self.assertIn("/siyk-test-add 集成测试", text)
        self.assertIn("`测试用例` 模式", text)
        self.assertIn("docs/testing/cases/<module>.md", text)
        self.assertIn("本轮相关 diff", text)
        self.assertIn("不要仅为了统一目录迁移", text)
        self.assertIn("默认不新增可执行测试代码", text)

    def test_init_is_markdown_project_map_only(self) -> None:
        text = (ROOT / "skills" / "siyk-init" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn(".siyrs/README.md", text)
        self.assertIn("commit SHA", text)
        self.assertIn("secret", text)
        self.assertIn("state.json", text)
        self.assertIn("registry.json", text)
        self.assertIn("cache/", text)
        self.assertIn("不迁移 E2E", text)

    def test_discovered_child_skills_stay_thin(self) -> None:
        for skill_dir in explicit_skill_dirs():
            lines = (skill_dir / "SKILL.md").read_text(encoding="utf-8").splitlines()
            self.assertLess(len(lines), 90, skill_dir.name)
        for path in ("adapters", "commands", "schemas", "release-manifest.json"):
            self.assertFalse((ROOT / path).exists(), path)

    def test_invalid_frontmatter_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = Path(tmp)
            (skill_dir / "SKILL.md").write_text("# no frontmatter\n", encoding="utf-8")
            errors = validator.validate_skill(skill_dir)
            self.assertTrue(any("frontmatter" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
