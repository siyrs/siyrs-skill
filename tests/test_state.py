from pathlib import Path
from tempfile import TemporaryDirectory
import json,sys,unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from state import default_state,load,migrate_v1,save,update_state

class StateTests(unittest.TestCase):
    def test_default_v2(self):
        state=default_state();self.assertEqual(2,state['version']);self.assertIn('promotion',state['last_t1_run'])
    def test_migrate_v1_preserves_unknown(self):
        old={'version':1,'last_full_test_commit':'abc','last_incremental_test_commit':'def'}
        state=migrate_v1(old);self.assertEqual('unknown',state['last_t3_run']['status']);self.assertEqual('def',state['last_authoring']['commit'])
    def test_update_t1_supports_tree_oid(self):
        state=update_state(default_state(),kind='t1',status='complete',fingerprint='fp',tree_oid='tree',case_ids=['C1','C1'])
        self.assertEqual('tree',state['last_t1_run']['tree_oid']);self.assertEqual(['C1'],state['last_t1_run']['case_ids'])
    def test_t2_requires_selector(self):
        with self.assertRaisesRegex(ValueError,'selector'):update_state(default_state(),kind='t2',status='complete',commit='abc')
    def test_t3_pass_requires_commit(self):
        with self.assertRaisesRegex(ValueError,'durable commit'):update_state(default_state(),kind='t3',status='complete',fingerprint='fp',release_gate='passed')
        state=update_state(default_state(),kind='t3',status='complete',fingerprint='fp',release_gate='provisional');self.assertEqual('provisional',state['last_release_gate']['decision'])
    def test_atomic_save(self):
        with TemporaryDirectory() as tmp:
            path=Path(tmp)/'.siyrs/state.json';save(path,default_state());self.assertEqual(2,json.loads(path.read_text())['version'])
if __name__=='__main__':unittest.main()
