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

EXPLICIT_SKILLS = (
    "siyk-init",
    "siyk-test-add",
    "siyk-git-commit",
    "siyk-git-sync",
)


class SkillStructureTests(unittest.TestCase):
    def test_bundle_validates(self) -> None:
        self.assertEqual([], validator.validate(ROOT))

    def test_main_skill_stays_compact(self) -> None:
        lines = (ROOT / "SKILL.md").read_text(encoding="utf-8").splitlines()
        self.assertLess(len(lines), 160)

    def test_main_skill_keeps_public_name(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        agent = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("name: siyrs-skill", skill)
        self.assertIn('display_name: "SIYRS Skill"', agent)
        self.assertIn("$siyrs-skill", agent)
        self.assertNotIn("$siyrs-engineering", agent)

    def test_primary_user_facing_copy_is_chinese(self) -> None:
        expectations = {
            ROOT / "SKILL.md": "聚焦完成软件仓库修改",
            ROOT / "agents" / "openai.yaml": "聚焦完成仓库修改",
            ROOT / "references" / "testing.md": "# 测试指南",
            ROOT / "references" / "project-map.md": "# `.siyrs` 项目地图指南",
            ROOT / "references" / "git.md": "# Git 交付指南",
            ROOT / "CONTRIBUTING.md": "# 贡献指南",
            ROOT / "CHANGELOG.md": "# 更新日志",
            ROOT / "README.md": "Markdown-first",
        }
        for path, text in expectations.items():
            self.assertIn(text, path.read_text(encoding="utf-8"), str(path))

    def test_markdown_first_testing_contract_is_preserved(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        testing = (ROOT / "references" / "testing.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        for text in (skill, testing, readme):
            self.assertIn("docs/testing/README.md", text)
            self.assertIn("standards/", text)
            self.assertIn("cases/", text)
            self.assertIn("reports/", text)

        self.assertIn("standards/priorities.md", testing)
        self.assertIn("standards/release-gate.md", testing)
        self.assertIn("测试代码跟着代码走", testing)
        self.assertIn("默认按业务模块而不是按 unit/integration/e2e 类型拆文件", testing)
        self.assertIn("Markdown-first 用例格式", testing)
        self.assertIn("pmp-vue/e2e/", testing)
        self.assertIn("不为了统一文档而搬迁", testing)
        self.assertIn("不需要强制每条用例都使用", testing)

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

    def test_explicit_skills_are_real_skills(self) -> None:
        for name in EXPLICIT_SKILLS:
            skill_dir = ROOT / "skills" / name
            text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            agent = (skill_dir / "agents" / "openai.yaml").read_text(encoding="utf-8")
            self.assertIn(f"name: {name}", text)
            self.assertIn(f'display_name: "{name}"', agent)
            self.assertIn("allow_implicit_invocation: false", agent)
            self.assertIn(f"${name}", agent)

    def test_test_add_modes_and_scope(self) -> None:
        text = (ROOT / "skills" / "siyk-test-add" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("默认模式：补可执行测试", text)
        self.assertIn("/siyk-test-add e2e", text)
        self.assertIn("/siyk-test-add 集成测试", text)
        self.assertIn("`测试用例` 模式", text)
        self.assertIn("docs/testing/cases/<module>.md", text)
        self.assertIn("本轮相关 diff", text)
        self.assertIn("不要仅为了统一目录迁移", text)
        self.assertIn("默认不新增可执行测试代码", text)

    def test_init_is_markdown_project_map_only(self) -> None:
        text = (ROOT / "skills" / "siyk-init" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(".siyrs/README.md", text)
        self.assertIn("commit SHA", text)
        self.assertIn("secret", text)
        self.assertIn("state.json", text)
        self.assertIn("registry.json", text)
        self.assertIn("cache/", text)
        self.assertIn("不迁移 E2E", text)

    def test_explicit_skills_stay_thin(self) -> None:
        for name in EXPLICIT_SKILLS:
            lines = (ROOT / "skills" / name / "SKILL.md").read_text(
                encoding="utf-8"
            ).splitlines()
            self.assertLess(len(lines), 90, name)
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
