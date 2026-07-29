from pathlib import Path
from tempfile import TemporaryDirectory
import os
import re
import shutil
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from command_registry import registry_document

NAMES = registry_document(ROOT)['entrypoint_names']
LEGACY = registry_document(ROOT)['legacy_names']


class AdapterTests(unittest.TestCase):
    def test_exact_sets(self):
        self.assertEqual(
            set(NAMES),
            {path.stem for path in (ROOT / 'adapters/claude-code/commands').glob('*.md')},
        )
        self.assertEqual(
            set(NAMES),
            {path.name for path in (ROOT / 'adapters/codex/entrypoints').iterdir() if path.is_dir()},
        )

    def test_thin_codex(self):
        for name in NAMES:
            text = (ROOT / f'adapters/codex/entrypoints/{name}/SKILL.template.md').read_text(encoding='utf-8')
            metadata = (ROOT / f'adapters/codex/entrypoints/{name}/agents/openai.yaml').read_text(encoding='utf-8')
            self.assertRegex(text, rf'(?m)^name:\s*{re.escape(name)}\s*$')
            self.assertIn('<skills-root>', text)
            self.assertIn('allow_implicit_invocation: false', metadata)

    @unittest.skipIf(os.name == 'nt', 'Bash installers are exercised by Linux/macOS jobs; Windows uses PowerShell installers')
    @unittest.skipUnless(shutil.which('bash'), 'bash required')
    def test_upgrade_installers(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            claude = root / 'claude'
            (claude / 'commands').mkdir(parents=True)
            for name in LEGACY:
                (claude / 'commands' / f'{name}.md').write_text(
                    '---\nsiyrs-skill-command-adapter: true\n---\n', encoding='utf-8'
                )
            env = os.environ.copy()
            env['CLAUDE_HOME'] = str(claude)
            subprocess.run(
                ['bash', str(ROOT / 'adapters/claude-code/install.sh')],
                env=env,
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            for name in NAMES:
                self.assertTrue((claude / 'commands' / f'{name}.md').exists())

            skills = root / 'skills'
            archive = root / 'archive'
            for name in LEGACY:
                (skills / name).mkdir(parents=True)
                (skills / name / 'SKILL.md').write_text(f'---\nname: {name}\n---\n', encoding='utf-8')
            env['SIYRS_CODEX_SKILLS_HOME'] = str(skills)
            env['SIYRS_CODEX_SKILL_BACKUPS_HOME'] = str(archive)
            subprocess.run(
                ['bash', str(ROOT / 'adapters/codex/install.sh')],
                env=env,
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            for name in NAMES:
                self.assertTrue((skills / name / 'SKILL.md').exists())
            for name in LEGACY:
                self.assertFalse((skills / name).exists())


if __name__ == '__main__':
    unittest.main()
