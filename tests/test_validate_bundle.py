from pathlib import Path
from tempfile import TemporaryDirectory
import json,shutil,sys,unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from validate_bundle import validate
class ValidationTests(unittest.TestCase):
    def test_current_bundle(self):
        result=validate(ROOT);self.assertTrue(result['valid'],result['errors']);self.assertEqual('0.2.7',result['version'])
    def test_state_schema_has_no_broken_allof(self):
        schema=json.loads((ROOT/'schemas/state.schema.json').read_text())
        for name in ('authoringRecord','t1Record','t2Record','t3Record'):self.assertNotIn('allOf',schema['$defs'][name]);self.assertFalse(schema['$defs'][name]['additionalProperties'])
    def test_mapfile_drift_detected(self):
        with TemporaryDirectory() as tmp:
            copy=Path(tmp)/'skill';shutil.copytree(ROOT,copy,ignore=shutil.ignore_patterns('.git','__pycache__','*.pyc'));p=copy/'adapters/claude-code/install.sh';p.write_text(p.read_text()+'\nmapfile -t x\n');self.assertFalse(validate(copy)['valid'])
if __name__=='__main__':unittest.main()
