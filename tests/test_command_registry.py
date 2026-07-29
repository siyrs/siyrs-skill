from pathlib import Path
from tempfile import TemporaryDirectory
import shutil
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from command_registry import load_registry, registry_document


class RegistryTests(unittest.TestCase):
    def test_registry_order(self):
        self.assertEqual([10, 20, 30, 40, 50, 60], [item.order for item in load_registry(ROOT)])

    def test_legacy(self):
        self.assertEqual(
            ['/siyk-test-full', '/siyk-test-new'],
            registry_document(ROOT)['legacy_commands'],
        )

    def test_duplicate_order(self):
        with TemporaryDirectory() as tmp:
            copy = Path(tmp) / 'skill'
            shutil.copytree(
                ROOT,
                copy,
                ignore=shutil.ignore_patterns('.git', '__pycache__', '*.pyc'),
            )
            path = copy / 'commands/test-run-t1.md'
            path.write_text(
                path.read_text(encoding='utf-8').replace('order: 20', 'order: 10'),
                encoding='utf-8',
            )
            with self.assertRaisesRegex(ValueError, 'duplicate command order'):
                load_registry(copy)


if __name__ == '__main__':
    unittest.main()
