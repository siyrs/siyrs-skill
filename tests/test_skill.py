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


def active_human_facing_files() -> list[Path]:
    paths = [
        ROOT / "README.md",
        ROOT / "SKILL.md",
        ROOT / "agents" / "openai.yaml",
    ]
    paths.extend(sorted((ROOT / "references").glob("*.md")))
    for skill_dir in explicit_skill_dirs():
        paths.append(skill_dir / "SKILL.md")
        paths.append(skill_dir / "agents" / "openai.yaml")
    paths.extend(
        path
        for path in sorted((ROOT / "docs").glob("*.md"))
        if path.name != "CHANGELOG.md"
    )
    return [path for path in paths if path.is_file()]


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

    def test_all_active_human_facing_files_use_full_brand_name(self) -> None:
        legacy_upper_brand = "SI" + "YRS"
        for path in active_human_facing_files():
            text = path.read_text(encoding="utf-8")
            self.assertNotIn(legacy_upper_brand, text, str(path))
            self.assertNotIn("Siyrs", text.replace("Siyrs Skill", ""), str(path))

    def test_primary_user_facing_copy_is_chinese(self) -> None:
        expectations = {
            ROOT / "SKILL.md": "聚焦完成软件仓库修改",
            ROOT / "agents" / "openai.yaml": "聚焦完成仓库修改",
            ROOT / "references" / "principles.md": "# Siyrs Skill 第一性原则",
            ROOT / "references" / "testing.md": "# 测试指南",
            ROOT / "references" / "testing-tiers.md": "# 测试分级执行合同",
            ROOT / "references" / "testing-t3-design.md": "# T3 深度业务测试设计",
            ROOT / "references" / "project-map.md": "# `.siyrs` 项目地图指南",
            ROOT / "references" / "git.md": "# Git 交付指南",
            ROOT / "docs" / "README.md": "# Siyrs Skill 文档",
            ROOT / "docs" / "architecture.md": "# Siyrs Skill 架构说明",
            ROOT / "docs" / "plan.md": "# Siyrs Skill 演化计划",
            ROOT / "docs" / "CONTRIBUTING.md": "# 贡献指南",
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
        self.assertNotIn("PMP", plan)

    def test_global_first_principles_are_shared(self) -> None:
        principles = (ROOT / "references" / "principles.md").read_text(encoding="utf-8")
        self.assertIn("Markdown-first", principles)
        self.assertIn("事实优先，不懂不猜", principles)
        self.assertIn("禁止编造", principles)

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
            self.assertIn((example, True), validator.discover_skill_dirs(root))

    def test_shared_domain_rules_are_delegated_to_references(self) -> None:
        init = (ROOT / "skills" / "siyk-init" / "SKILL.md").read_text(encoding="utf-8")
        commit = (ROOT / "skills" / "siyk-git-commit" / "SKILL.md").read_text(encoding="utf-8")
        sync = (ROOT / "skills" / "siyk-git-sync" / "SKILL.md").read_text(encoding="utf-8")
        t3_add = (ROOT / "skills" / "siyk-test-add-t3" / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("../../references/project-map.md", init)
        self.assertIn("../../references/git.md", commit)
        self.assertIn("../../references/git.md", sync)
        self.assertNotIn("siyk-git-commit", sync)
        self.assertIn("../../references/testing-t3-design.md", t3_add)
        self.assertLess(len(t3_add.splitlines()), 55)

    def test_markdown_first_testing_contract_is_preserved(self) -> None:
        testing = (ROOT / "references" / "testing.md").read_text(encoding="utf-8")
        self.assertIn("docs/testing/README.md", testing)
        self.assertIn("standards/", testing)
        self.assertIn("cases/", testing)
        self.assertIn("reports/", testing)
        self.assertIn("默认按业务模块而不是按 unit/integration/e2e 类型拆文件", testing)
        self.assertIn("Markdown-first 用例格式", testing)
        self.assertIn("P0 · T2 · E2E", testing)
        self.assertIn("不要为测试设计建立额外 JSON/YAML state、matrix、registry", testing)

    def test_test_tier_contract_has_authoring_and_execution_views(self) -> None:
        tiers = (ROOT / "references" / "testing-tiers.md").read_text(encoding="utf-8")
        self.assertIn("设计与执行是两个视角", tiers)
        self.assertIn("T1 — 变更回归", tiers)
        self.assertIn("T2 — 标准 Smoke", tiers)
        self.assertIn("T3 — 深度业务验收 / 发布级验证", tiers)
        self.assertIn("testing-t3-design.md", tiers)
        self.assertIn("只有用户明确要求全项目", tiers)
        self.assertIn("UAT 通过", tiers)
        self.assertIn("不自动等于 T3 通过", tiers)

    def test_t3_design_contract_is_deep_grounded_and_markdown_first(self) -> None:
        text = (ROOT / "references" / "testing-t3-design.md").read_text(encoding="utf-8")
        for expected in (
            "全局理解，但不自动全局测试",
            "Business Invariants",
            "Test Oracle",
            "不要把模型直觉",
            "Impact Propagation",
            "Impact Isolation",
            "从业务事件设计，而不是从按钮设计",
            "多角色与连续业务旅程",
            "Test Critic",
            "子代理是推理策略，不是运行依赖",
            "docs/testing/cases/<module>.md",
            "Case + Manual / UAT",
            "不要为 T3 设计新增 command router、state、schema、matrix runtime",
        ):
            self.assertIn(expected, text)

    def test_test_add_auto_selects_tier_and_delegates_t3(self) -> None:
        text = (ROOT / "skills" / "siyk-test-add" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("先判断需要的测试深度", text)
        self.assertIn("不要用关键词脚本", text)
        self.assertIn("UAT", text)
        self.assertIn("测试用例", text)
        self.assertIn("../../references/testing-t3-design.md", text)
        self.assertIn("委托给共享设计合同", text)
        self.assertIn("docs/testing/cases/<module>.md", text)

    def test_t3_add_skill_is_thin_explicit_authoring_entry(self) -> None:
        text = (ROOT / "skills" / "siyk-test-add-t3" / "SKILL.md").read_text(encoding="utf-8")
        agent = (ROOT / "skills" / "siyk-test-add-t3" / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("../../references/testing-t3-design.md", text)
        self.assertIn("完整 T3 设计语义", text)
        self.assertIn("全局理解不等于全局测试", text)
        self.assertIn("不负责执行完整 T3 发布级验证", text)
        self.assertIn("allow_implicit_invocation: false", agent)
        self.assertIn("$siyk-test-add-t3", agent)

    def test_t3_runner_is_scope_aware_and_does_not_author_cases(self) -> None:
        t3 = (ROOT / "skills" / "siyk-test-run-t3" / "SKILL.md").read_text(encoding="utf-8")
        agent = (ROOT / "skills" / "siyk-test-run-t3" / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("# SIYK T3 发布级验证", t3)
        self.assertIn("确定 Scope", t3)
        self.assertIn("只有用户明确要求全项目", t3)
        self.assertIn("模块 T3 通过不等于全项目 T3 通过", t3)
        self.assertIn("docs/testing/reports/<date>-<scope>.md", t3)
        self.assertNotIn("testing-t3-design.md", t3)
        self.assertIn("当前或指定 Scope", agent)

    def test_project_map_contract_lives_in_reference(self) -> None:
        project_map = (ROOT / "references" / "project-map.md").read_text(encoding="utf-8")
        init = (ROOT / "skills" / "siyk-init" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn(".siyrs/README.md", project_map)
        self.assertIn("真实代码、构建配置、测试代码和项目文档始终优先", project_map)
        self.assertIn("Secret 边界", project_map)
        self.assertIn("state.json", project_map)
        self.assertIn("registry.json", project_map)
        self.assertIn("cache/", project_map)
        self.assertIn("../../references/project-map.md", init)

    def test_git_shortcuts_delegate_to_git_reference(self) -> None:
        git = (ROOT / "references" / "git.md").read_text(encoding="utf-8")
        commit = (ROOT / "skills" / "siyk-git-commit" / "SKILL.md").read_text(encoding="utf-8")
        sync = (ROOT / "skills" / "siyk-git-sync" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("保留无关", git)
        self.assertIn("force push", git)
        self.assertIn("../../references/git.md", commit)
        self.assertIn("../../references/git.md", sync)

    def test_discovered_child_skills_are_real_explicit_skills(self) -> None:
        for skill_dir in explicit_skill_dirs():
            text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            agent = (skill_dir / "agents" / "openai.yaml").read_text(encoding="utf-8")
            self.assertIn(f"name: {skill_dir.name}", text)
            self.assertIn(f'display_name: "{skill_dir.name}"', agent)
            self.assertIn("allow_implicit_invocation: false", agent)
            self.assertIn(f"${skill_dir.name}", agent)

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
