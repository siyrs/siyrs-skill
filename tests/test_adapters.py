from pathlib import Path
from tempfile import TemporaryDirectory
import os,re,shutil,subprocess,sys,unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from command_registry import registry_document
NAMES=registry_document(ROOT)['entrypoint_names'];LEGACY=registry_document(ROOT)['legacy_names']
class AdapterTests(unittest.TestCase):
 def test_exact_source_adapter_sets(self):
  self.assertEqual(set(NAMES),{p.stem for p in (ROOT/'adapters/claude-code/commands').glob('*.md')});self.assertEqual(set(NAMES),{p.name for p in (ROOT/'adapters/codex/entrypoints').iterdir() if p.is_dir()})
 def test_thin_codex_contracts(self):
  for n in NAMES:
   t=(ROOT/f'adapters/codex/entrypoints/{n}/SKILL.template.md').read_text();m=(ROOT/f'adapters/codex/entrypoints/{n}/agents/openai.yaml').read_text();self.assertRegex(t,rf'(?m)^name:\s*{re.escape(n)}\s*$');self.assertIn('<skills-root>/siyrs-skill/SKILL.md',t);self.assertIn('allow_implicit_invocation: false',m)
 @unittest.skipUnless(shutil.which('bash'),'bash required')
 def test_claude_upgrade_removes_legacy(self):
  with TemporaryDirectory() as tmp:
   home=Path(tmp)/'claude';(home/'commands').mkdir(parents=True)
   for n in LEGACY:(home/'commands'/f'{n}.md').write_text('---\nsiyrs-skill-command-adapter: true\n---\n')
   env=os.environ.copy();env['CLAUDE_HOME']=str(home);subprocess.run(['bash',str(ROOT/'adapters/claude-code/install.sh')],env=env,cwd=ROOT,check=True,capture_output=True,text=True);subprocess.run(['bash',str(ROOT/'adapters/claude-code/install.sh')],env=env,cwd=ROOT,check=True,capture_output=True,text=True)
   for n in NAMES:self.assertTrue((home/'commands'/f'{n}.md').is_file())
   for n in LEGACY:self.assertFalse((home/'commands'/f'{n}.md').exists())
 @unittest.skipUnless(shutil.which('bash'),'bash required')
 def test_codex_upgrade_archives_legacy(self):
  with TemporaryDirectory() as tmp:
   root=Path(tmp);home=root/'skills';archive=root/'archive'
   for n in LEGACY:(home/n).mkdir(parents=True);(home/n/'SKILL.md').write_text(f'---\nname: {n}\n---\n')
   env=os.environ.copy();env['SIYRS_CODEX_SKILLS_HOME']=str(home);env['SIYRS_CODEX_SKILL_BACKUPS_HOME']=str(archive)
   subprocess.run(['bash',str(ROOT/'adapters/codex/install.sh')],env=env,cwd=ROOT,check=True,capture_output=True,text=True);subprocess.run(['bash',str(ROOT/'adapters/codex/install.sh')],env=env,cwd=ROOT,check=True,capture_output=True,text=True)
   for n in NAMES:self.assertTrue((home/n/'SKILL.md').is_file())
   for n in LEGACY:self.assertFalse((home/n).exists())
   self.assertGreaterEqual(len(list(archive.rglob('SKILL.md'))),len(LEGACY))
if __name__=='__main__':unittest.main()
