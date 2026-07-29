from pathlib import Path
from tempfile import TemporaryDirectory
import shutil,sys,unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from command_registry import load_registry,registry_document
class RegistryTests(unittest.TestCase):
 def test_registry_is_ordered_single_source(self):
  specs=load_registry(ROOT);self.assertEqual(['/siyk-test-add','/siyk-test-run-t1','/siyk-test-run-t2','/siyk-test-run-t3','/siyk-git-commit','/siyk-git-sync'],[s.command for s in specs]);self.assertEqual([10,20,30,40,50,60],[s.order for s in specs])
 def test_legacy_commands_are_registered(self):
  d=registry_document(ROOT);self.assertEqual(['/siyk-test-full','/siyk-test-new'],d['legacy_commands'])
 def test_tier_strength_contract(self):
  by={s.command:s for s in load_registry(ROOT)};self.assertEqual(('quick','standard','strict'),by['/siyk-test-add'].strengths)
  for c in ('/siyk-test-run-t1','/siyk-test-run-t2','/siyk-test-run-t3'):self.assertEqual((),by[c].strengths)
 def test_duplicate_order_is_rejected(self):
  with TemporaryDirectory() as tmp:
   copy=Path(tmp)/'skill';shutil.copytree(ROOT,copy,ignore=shutil.ignore_patterns('.git','__pycache__','*.pyc'))
   p=copy/'commands/test-run-t1.md';p.write_text(p.read_text().replace('order: 20','order: 10'),encoding='utf-8')
   with self.assertRaisesRegex(ValueError,'duplicate command order'):load_registry(copy)
if __name__=='__main__':unittest.main()
