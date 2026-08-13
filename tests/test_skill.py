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


class SkillStructureTests(unittest.TestCase):
    def test_bundle_validates(self) -> None:
        self.assertEqual([], validator.validate(ROOT))

    def test_main_skill_stays_compact(self) -> None:
        lines = (ROOT / "SKILL.md").read_text(encoding="utf-8").splitlines()
        self.assertLess(len(lines), 140)

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
            ROOT / "references" / "git.md": "# Git 交付指南",
            ROOT / "CONTRIBUTING.md": "# 贡献指南",
            ROOT / "CHANGELOG.md": "# 更新日志",
            ROOT / "README.md": "中文优先",
        }
        for path, text in expectations.items():
            self.assertIn(text, path.read_text(encoding="utf-8"), str(path))

    def test_testing_workspace_contract_is_preserved(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        testing = (ROOT / "references" / "testing.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        for text in (skill, testing, readme):
            self.assertIn("docs/testing/README.md", text)

        self.assertIn("根 README 必须能发现测试入口", testing)
        self.assertIn("[测试文档](docs/testing/README.md)", testing)
        self.assertIn("文件名大小写不敏感", testing)
        self.assertIn("默认不要创建 `cases/`、`evidence/`、`matrix/`", testing)
        self.assertNotIn("默认**不要**创建 `docs/testing/`", testing)

    def test_shortcuts_are_real_skills(self) -> None:
        for name in ("siyk-git-commit", "siyk-git-sync"):
            skill_dir = ROOT / "skills" / name
            text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            agent = (skill_dir / "agents" / "openai.yaml").read_text(encoding="utf-8")
            self.assertIn(f"name: {name}", text)
            self.assertIn(f'display_name: "{name}"', agent)
            self.assertIn("allow_implicit_invocation: false", agent)

    def test_shortcut_user_facing_copy_is_chinese(self) -> None:
        expectations = {
            "siyk-git-commit": ("显式的轻量 Git 提交快捷 Skill", "将当前目标改动安全保存"),
            "siyk-git-sync": ("显式的轻量 Git 同步快捷 Skill", "保存必要本地改动"),
        }
        for name, (description_text, short_text) in expectations.items():
            skill_dir = ROOT / "skills" / name
            skill = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            agent = (skill_dir / "agents" / "openai.yaml").read_text(encoding="utf-8")
            self.assertIn(description_text, skill)
            self.assertIn(short_text, agent)
            self.assertIn("使用 $", agent)

    def test_shortcuts_stay_thin(self) -> None:
        for name in ("siyk-git-commit", "siyk-git-sync"):
            lines = (ROOT / "skills" / name / "SKILL.md").read_text(
                encoding="utf-8"
            ).splitlines()
            self.assertLess(len(lines), 40)
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
