from pathlib import Path
from tempfile import TemporaryDirectory
import shutil,sys,unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from validate_bundle import validate
class ValidationTests(unittest.TestCase):
 def copy(self,tmp):
  p=Path(tmp)/'skill';shutil.copytree(ROOT,p,ignore=shutil.ignore_patterns('.git','__pycache__','*.pyc'));return p
 def test_current_valid(self):
  r=validate(ROOT);self.assertTrue(r['valid'],r['errors']);self.assertEqual('0.2.2',r['version']);self.assertEqual(6,len(r['commands']))
 def test_version_drift(self):
  with TemporaryDirectory() as tmp:
   p=self.copy(tmp);(p/'VERSION').write_text('9.9.9\n');self.assertFalse(validate(p)['valid'])
 def test_stale_claude_adapter_detected(self):
  with TemporaryDirectory() as tmp:
   p=self.copy(tmp);(p/'adapters/claude-code/commands/siyk-test-new.md').write_text('stale');r=validate(p);self.assertFalse(r['valid']);self.assertTrue(any('Claude adapter set mismatch' in x for x in r['errors']))
 def test_ci_legacy_reference_detected(self):
  with TemporaryDirectory() as tmp:
   p=self.copy(tmp);f=p/'.github/workflows/ci.yml';f.write_text(f.read_text()+'\n# bad smoke\npython scripts/siyk.py route "/siyk-test-new"\n');r=validate(p);self.assertTrue(any('deprecated command' in x for x in r['errors']))
 def test_schema_v1_detected(self):
  with TemporaryDirectory() as tmp:
   p=self.copy(tmp);f=p/'schemas/config.schema.json';f.write_text(f.read_text().replace('"const": 2','"const": 1',1));self.assertFalse(validate(p)['valid'])
 def test_registry_drift_detected(self):
  with TemporaryDirectory() as tmp:
   p=self.copy(tmp);f=p/'commands/test-run-t1.md';f.write_text(f.read_text().replace('order: 20','order: 10'));self.assertFalse(validate(p)['valid'])
if __name__=='__main__':unittest.main()
