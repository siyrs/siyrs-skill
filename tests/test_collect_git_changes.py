from pathlib import Path
from tempfile import TemporaryDirectory
import json,subprocess,sys,unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from collect_git_changes import collect

def git(repo,*args): return subprocess.run(['git',*args],cwd=repo,check=True,stdout=subprocess.PIPE,text=True).stdout.strip()
def commit(repo,msg): git(repo,'add','-A');git(repo,'commit','-m',msg);return git(repo,'rev-parse','HEAD')
class CollectTests(unittest.TestCase):
 def repo(self,tmp):
  p=Path(tmp);git(p,'init');git(p,'config','user.email','test@example.com');git(p,'config','user.name','Test');return p
 def test_t1_prefers_state_baseline(self):
  with TemporaryDirectory() as tmp:
   r=self.repo(tmp);(r/'a.txt').write_text('1');c1=commit(r,'one');(r/'a.txt').write_text('2');c2=commit(r,'two');(r/'a.txt').write_text('3');commit(r,'three')
   (r/'.siyrs').mkdir();(r/'.siyrs/state.json').write_text(json.dumps({'version':2,'last_t1_run':{'commit':c1},'last_t3_run':{},'last_authoring':{},'last_t2_run':{}}))
   out=collect(r,purpose='t1');self.assertEqual(c1,out['baseline']);self.assertEqual('state:last_t1_run',out['baseline_source']);self.assertTrue(out['committed_changes'])
 def test_add_prefers_authoring(self):
  with TemporaryDirectory() as tmp:
   r=self.repo(tmp);(r/'a').write_text('1');c1=commit(r,'one');(r/'a').write_text('2');commit(r,'two');(r/'.siyrs').mkdir();(r/'.siyrs/state.json').write_text(json.dumps({'version':2,'last_authoring':{'commit':c1},'last_t1_run':{},'last_t2_run':{},'last_t3_run':{}}));self.assertEqual('state:last_authoring',collect(r,purpose='add')['baseline_source'])
 def test_uncommitted_and_untracked_are_included(self):
  with TemporaryDirectory() as tmp:
   r=self.repo(tmp);(r/'a').write_text('1');commit(r,'one');(r/'a').write_text('2');(r/'中 文.txt').write_text('x');out=collect(r,purpose='t1');self.assertIn('a',out['changed_files']);self.assertIn('中 文.txt',out['untracked_files'])
 def test_non_repo(self):
  with TemporaryDirectory() as tmp:self.assertFalse(collect(Path(tmp))['is_git_repository'])
if __name__=='__main__':unittest.main()
