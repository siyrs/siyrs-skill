from pathlib import Path
from tempfile import TemporaryDirectory
import sys, unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from config_model import ConfigError, load_config, parse_yaml_subset
from test_plan import resolve_plan

class ConfigPlanTests(unittest.TestCase):
    def test_yaml_subset_parses_module_overrides(self):
        data=parse_yaml_subset('''version: 2
project:
  modules:
    - name: backend
      path: backend
      testing:
        tiers:
          t2:
            commands:
              - argv: ["python", "-m", "unittest"]
testing:
  tiers:
    t2:
      selector_id: smoke-v1
      commands: []
      required_per_module:
        main_path: 1
        boundary: 1
''')
        self.assertEqual('backend',data['project']['modules'][0]['name'])
        self.assertEqual(['python','-m','unittest'],data['project']['modules'][0]['testing']['tiers']['t2']['commands'][0]['argv'])

    def test_validate_and_resolve_module_plan(self):
        with TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'backend').mkdir();(root/'.siyrs').mkdir()
            (root/'.siyrs/config.yaml').write_text('''version: 2
project:
  modules:
    - name: backend
      path: backend
      testing:
        tiers:
          t2:
            commands:
              - id: backend-smoke
                argv: ["python", "-m", "unittest"]
                timeout_seconds: 60
testing:
  tiers:
    t2:
      selector_id: smoke-v1
      commands: []
      required_per_module:
        main_path: 1
        boundary: 1
''')
            loaded=load_config(root);self.assertTrue(loaded['valid'],loaded['errors'])
            plan=resolve_plan(root,'t2');self.assertTrue(plan['valid'],plan)
            self.assertEqual('backend-smoke',plan['steps'][0]['id']);self.assertEqual('backend',plan['steps'][0]['cwd'])
            self.assertEqual('smoke-v1',plan['selector_id'])
            self.assertEqual('docs/testing/README.md',plan['documentation']['workspace']['entry'])

    def test_missing_commands_is_plan_debt(self):
        with TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'.siyrs').mkdir();(root/'.siyrs/config.yaml').write_text('version: 2\n')
            plan=resolve_plan(root,'t2');self.assertFalse(plan['valid']);self.assertTrue(any('no machine-selectable' in x or 'no configured' in x for x in plan['debts']))

    def test_invalid_module_path_is_rejected(self):
        with TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'.siyrs').mkdir();(root/'.siyrs/config.yaml').write_text('''version: 2
project:
  modules:
    - name: escape
      path: ../outside
''')
            loaded=load_config(root);self.assertFalse(loaded['valid']);self.assertTrue(any('safe relative path' in x for x in loaded['errors']))

if __name__=='__main__':unittest.main()
