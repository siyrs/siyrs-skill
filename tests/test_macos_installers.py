from pathlib import Path
import os
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


class MacInstallerTests(unittest.TestCase):
    def test_bash_installers_avoid_bash4_and_gnu_find_only_features(self):
        for relative in ('adapters/claude-code/install.sh', 'adapters/codex/install.sh'):
            text = (ROOT / relative).read_text(encoding='utf-8')
            self.assertNotIn('mapfile', text)
            self.assertNotIn('-mindepth', text)
            self.assertNotIn('-maxdepth', text)

    @unittest.skipIf(os.name == 'nt', 'Bash syntax is validated by Linux/macOS jobs; Windows uses PowerShell')
    @unittest.skipUnless(shutil.which('bash'), 'bash required')
    def test_bash_syntax(self):
        for relative in ('adapters/claude-code/install.sh', 'adapters/codex/install.sh'):
            subprocess.run(['bash', '-n', str(ROOT / relative)], check=True)


if __name__ == '__main__':
    unittest.main()
