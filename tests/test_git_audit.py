from pathlib import Path
from tempfile import TemporaryDirectory
import json,subprocess,sys,unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from git_audit import audit_index,audit_outgoing

def git(repo,*args):return subprocess.run(['git',*args],cwd=repo,check=True,stdout=subprocess.PIPE,text=True).stdout.strip()
def commit(repo,msg):git(repo,'add','-A');git(repo,'commit','-m',msg);return git(repo,'rev-parse','HEAD')
class GitAuditTests(unittest.TestCase):
    def repo(self,tmp):
        repo=Path(tmp);git(repo,'init');git(repo,'config','user.email','test@example.com');git(repo,'config','user.name','Test');(repo/'a.txt').write_text('safe\n');base=commit(repo,'initial');return repo,base
    def secret(self):return 'sk-'+'A'*24
    def test_index_reads_staged_not_worktree(self):
        with TemporaryDirectory() as tmp:
            repo,_=self.repo(tmp);secret=self.secret();(repo/'a.txt').write_text('token='+secret+'\n');git(repo,'add','a.txt');(repo/'a.txt').write_text('safe worktree\n')
            result=audit_index(repo);self.assertTrue(result['high_confidence_block']);payload=json.dumps(result);self.assertNotIn(secret,payload);self.assertTrue(any(f['classification']=='introduced' for f in result['findings']))
    def test_outgoing_finds_added_then_removed_history(self):
        with TemporaryDirectory() as tmp:
            repo,base=self.repo(tmp);secret=self.secret();(repo/'a.txt').write_text(secret+'\n');commit(repo,'introduce');(repo/'a.txt').write_text('safe\n');commit(repo,'remove')
            result=audit_outgoing(repo,base=base);self.assertTrue(any(f['classification']=='historical-introduction' for f in result['findings']));self.assertNotIn(secret,json.dumps(result))
    def test_ids_are_stable_for_same_index(self):
        with TemporaryDirectory() as tmp:
            repo,_=self.repo(tmp);(repo/'a.txt').write_text(self.secret());git(repo,'add','a.txt');a=audit_index(repo);b=audit_index(repo);self.assertEqual([(f['id'],f['evidence_fingerprint']) for f in a['findings']],[(f['id'],f['evidence_fingerprint']) for f in b['findings']])
if __name__=='__main__':unittest.main()
