from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class AdapterTests(unittest.TestCase):
    def test_claude_command_adapters_exist(self):
        command_dir = ROOT / "adapters" / "claude-code" / "commands"
        for name in ("siyk-test-full", "siyk-test-new", "siyk-git-commit", "siyk-git-sync"):
            path = command_dir / f"{name}.md"
            self.assertTrue(path.is_file())
            text = path.read_text(encoding="utf-8")
            self.assertIn("siyrs-skill", text)
            self.assertIn(f"/{name}", text)
            self.assertIn("$ARGUMENTS", text)

    def test_installers_exist_and_exclude_git_metadata(self):
        bash = ROOT / "adapters/claude-code/install.sh"
        powershell = ROOT / "adapters/claude-code/install.ps1"
        self.assertTrue(bash.is_file())
        self.assertTrue(powershell.is_file())
        self.assertIn('"${temp_target}/.git"', bash.read_text(encoding="utf-8"))
        self.assertIn('".git"', powershell.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
