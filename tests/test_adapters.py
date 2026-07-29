from pathlib import Path
from tempfile import TemporaryDirectory
import os
import re
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
NAMES = ("siyk-test-full", "siyk-test-new", "siyk-git-commit", "siyk-git-sync")


class AdapterTests(unittest.TestCase):
    def test_claude_command_adapters_exist(self):
        command_dir = ROOT / "adapters" / "claude-code" / "commands"
        for name in NAMES:
            path = command_dir / f"{name}.md"
            self.assertTrue(path.is_file())
            text = path.read_text(encoding="utf-8")
            self.assertIn("siyrs-skill", text)
            self.assertIn(f"/{name}", text)
            self.assertIn("$ARGUMENTS", text)

    def test_codex_entrypoints_are_thin_explicit_skills(self):
        entrypoints = ROOT / "adapters" / "codex" / "entrypoints"
        for name in NAMES:
            template = entrypoints / name / "SKILL.template.md"
            metadata = entrypoints / name / "agents" / "openai.yaml"
            self.assertTrue(template.is_file(), name)
            self.assertTrue(metadata.is_file(), name)
            text = template.read_text(encoding="utf-8")
            self.assertRegex(text, rf"(?m)^name:\s*{re.escape(name)}\s*$")
            self.assertIn("<skills-root>/siyrs-skill/SKILL.md", text)
            self.assertIn(f"/{name}", text)
            self.assertIn("thin discovery adapter", text)
            meta = metadata.read_text(encoding="utf-8")
            self.assertIn(f'display_name: "/{name}"', meta)
            self.assertIn("allow_implicit_invocation: false", meta)

    def test_installers_exist_and_use_current_codex_location(self):
        claude_bash = ROOT / "adapters" / "claude-code" / "install.sh"
        claude_ps = ROOT / "adapters" / "claude-code" / "install.ps1"
        codex_bash = ROOT / "adapters" / "codex" / "install.sh"
        codex_ps = ROOT / "adapters" / "codex" / "install.ps1"
        for path in (claude_bash, claude_ps, codex_bash, codex_ps):
            self.assertTrue(path.is_file(), path)
        self.assertIn('"${temp_target}/.git"', claude_bash.read_text(encoding="utf-8"))
        self.assertIn('".git"', claude_ps.read_text(encoding="utf-8"))
        bash_text = codex_bash.read_text(encoding="utf-8")
        ps_text = codex_ps.read_text(encoding="utf-8")
        self.assertIn("${HOME}/.agents/skills", bash_text)
        self.assertIn('".agents\\skills"', ps_text)
        self.assertNotIn(".codex/prompts", bash_text)
        for name in NAMES:
            self.assertIn(name, bash_text)
            self.assertIn(name, ps_text)

    @unittest.skipUnless(shutil.which("bash"), "bash is required for installer smoke test")
    def test_codex_bash_installer_is_idempotent(self):
        with TemporaryDirectory() as tmp:
            target = Path(tmp) / "agents-skills"
            env = os.environ.copy()
            env["SIYRS_CODEX_SKILLS_HOME"] = str(target)
            script = ROOT / "adapters" / "codex" / "install.sh"
            subprocess.run(["bash", str(script)], cwd=ROOT, env=env, check=True, capture_output=True, text=True)
            subprocess.run(["bash", str(script)], cwd=ROOT, env=env, check=True, capture_output=True, text=True)
            self.assertTrue((target / "siyrs-skill" / "SKILL.md").is_file())
            for name in NAMES:
                installed = target / name
                self.assertTrue((installed / "SKILL.md").is_file(), name)
                self.assertTrue((installed / "agents" / "openai.yaml").is_file(), name)
                self.assertFalse((installed / "SKILL.template.md").exists(), name)
                text = (installed / "SKILL.md").read_text(encoding="utf-8")
                self.assertRegex(text, rf"(?m)^name:\s*{re.escape(name)}\s*$")
            self.assertFalse((target / "siyrs-skill" / ".git").exists())


if __name__ == "__main__":
    unittest.main()
