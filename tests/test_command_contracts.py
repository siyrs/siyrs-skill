from pathlib import Path
import sys,unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from command_registry import load_registry
class Contracts(unittest.TestCase):
 def text(self,p):return (ROOT/p).read_text(encoding='utf-8').lower()
 def test_every_command_has_registry_frontmatter(self):self.assertEqual(6,len(load_registry(ROOT)))
 def test_t2_requires_native_selector(self):
  t=self.text('commands/test-run-t2.md');self.assertIn('machine-selectable',t);self.assertIn('selector',t);self.assertIn('partially complete',t)
 def test_git_preflight_reuses_t1(self):
  self.assertIn('commands/test-run-t1.md',self.text('commands/git-commit.md'));self.assertIn('default is embedded t1',self.text('commands/git-sync.md'))
 def test_t1_avoids_redundant_confirmation(self):self.assertIn('continue automatically',self.text('commands/test-run-t1.md'))
 def test_t3_is_strict_release_gate(self):self.assertIn('always the strict full release gate',self.text('commands/test-run-t3.md'))
 def test_matrix_has_selector_columns(self):
  t=(ROOT/'assets/templates/TEST-MATRIX.template.md').read_text();self.assertIn('Tier',t);self.assertIn('Selector/Test ID',t);self.assertIn('Role',t)
 def test_git_security_contract_retained(self):
  t=self.text('commands/git-commit.md');self.assertIn('exact git index',t);self.assertIn('must not contact',t)
if __name__=='__main__':unittest.main()
