from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess,sys,unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from state import default_state,promote_t1,update_state

def git(repo,*args):return subprocess.run(['git',*args],cwd=repo,check=True,stdout=subprocess.PIPE,text=True).stdout.strip()
class PromotionTests(unittest.TestCase):
    def repo(self,tmp):
        repo=Path(tmp);git(repo,'init');git(repo,'config','user.email','test@example.com');git(repo,'config','user.name','Test');(repo/'a').write_text('one');git(repo,'add','a');git(repo,'commit','-m','initial');return repo
    def test_fingerprint_promotes_when_commit_tree_matches(self):
        with TemporaryDirectory() as tmp:
            repo=self.repo(tmp);(repo/'a').write_text('two');git(repo,'add','a');tree=git(repo,'write-tree')
            state=update_state(default_state(),kind='t1',status='complete',fingerprint='fp-1',tree_oid=tree)
            git(repo,'commit','-m','change');promoted=promote_t1(repo,state)
            self.assertEqual(git(repo,'rev-parse','HEAD'),promoted['last_t1_run']['commit']);self.assertEqual('fp-1',promoted['last_t1_run']['promotion']['from_fingerprint'])
    def test_tree_mismatch_blocks_promotion(self):
        with TemporaryDirectory() as tmp:
            repo=self.repo(tmp);(repo/'a').write_text('two');git(repo,'add','a');tree=git(repo,'write-tree');state=update_state(default_state(),kind='t1',status='complete',fingerprint='fp',tree_oid=tree)
            (repo/'a').write_text('three');git(repo,'add','a');git(repo,'commit','-m','different')
            with self.assertRaisesRegex(ValueError,'does not match tested candidate tree'):promote_t1(repo,state)
if __name__=='__main__':unittest.main()
