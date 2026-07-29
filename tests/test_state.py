from pathlib import Path
from tempfile import TemporaryDirectory
import json,sys,unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from state import default_state,load,migrate_v1,save,update_state
class StateTests(unittest.TestCase):
 def test_default_v2(self):
  s=default_state();self.assertEqual(2,s['version']);self.assertIn('last_t1_run',s);self.assertIn('last_release_gate',s)
 def test_migrate_v1_preserves_unknown(self):
  old={'version':1,'last_full_test_commit':'abc','last_full_test_mode':'strict','last_incremental_test_commit':'def','last_incremental_test_mode':'standard','last_results_file':'r.md','updated_at':'2026-01-01T00:00:00+00:00'}
  s=migrate_v1(old);self.assertEqual(2,s['version']);self.assertEqual('abc',s['last_t3_run']['commit']);self.assertEqual('unknown',s['last_t3_run']['status']);self.assertEqual('def',s['last_authoring']['commit']);self.assertEqual(1,s['migration']['from_version'])
 def test_load_auto_migrates(self):
  with TemporaryDirectory() as tmp:
   p=Path(tmp)/'state.json';p.write_text(json.dumps({'version':1,'last_full_test_commit':'abc'}));self.assertEqual(2,load(p)['version'])
 def test_update_t1(self):
  s=update_state(default_state(),kind='t1',status='complete',commit='abc',baseline_commit='base',case_ids=['C1','C1'],modules=['m'],expanded_modules=['shared'])
  self.assertEqual(['C1'],s['last_t1_run']['case_ids']);self.assertEqual('base',s['last_t1_run']['baseline_commit'])
 def test_t2_requires_selector(self):
  with self.assertRaisesRegex(ValueError,'selector'):update_state(default_state(),kind='t2',status='complete',commit='abc')
 def test_t3_updates_release_gate(self):
  s=update_state(default_state(),kind='t3',status='complete',commit='abc',release_gate='passed',coverage=91.2);self.assertEqual('passed',s['last_release_gate']['decision'])
 def test_atomic_save(self):
  with TemporaryDirectory() as tmp:
   p=Path(tmp)/'.siyrs/state.json';save(p,default_state());self.assertEqual(2,json.loads(p.read_text())['version']);self.assertFalse(p.with_suffix('.json.tmp').exists())
if __name__=='__main__':unittest.main()
