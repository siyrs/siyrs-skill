from pathlib import Path
import sys,unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from route_command import route
class RouteTests(unittest.TestCase):
 def test_authoring_depth(self):
  r=route('/siyk-test-add strict 权限',ROOT);self.assertTrue(r['valid']);self.assertEqual('strict',r['strength']);self.assertEqual('权限',r['extra'])
 def test_tiers_have_no_strength(self):
  for c in ('t1','t2','t3'):
   r=route(f'/siyk-test-run-{c}',ROOT);self.assertTrue(r['valid']);self.assertIsNone(r['strength'])
 def test_invalid_tier_strength_is_rejected(self):
  r=route('/siyk-test-run-t2 strict',ROOT);self.assertFalse(r['valid']);self.assertIn('not supported',r['warnings'][0])
 def test_alias_casefold(self):
  self.assertEqual('/siyk-test-run-t1',route('跑T1',ROOT)['command']);self.assertEqual('/siyk-test-run-t2',route('RUN SMOKE 模块A',ROOT)['command']);self.assertEqual('/siyk-test-run-t3',route('Release Gate',ROOT)['command'])
 def test_broad_english_does_not_misroute(self):
  self.assertFalse(route('full stack 项目设计',ROOT)['matched']);self.assertFalse(route('smoke detector feature',ROOT)['matched']);self.assertFalse(route('regression analysis report',ROOT)['matched'])
 def test_exact_broad_aliases_work(self):
  self.assertEqual('/siyk-test-run-t3',route('full',ROOT)['command']);self.assertEqual('/siyk-test-run-t2',route('smoke',ROOT)['command']);self.assertEqual('/siyk-test-run-t1',route('regression',ROOT)['command'])
 def test_legacy_new(self):
  r=route('/siyk-test-new quick 新增功能',ROOT);self.assertEqual('/siyk-test-add',r['command']);self.assertEqual('quick',r['strength']);self.assertTrue(r['warnings']);self.assertTrue(r['source'].startswith('legacy:'))
 def test_legacy_full_ignores_strength(self):
  r=route('/siyk-test-full quick',ROOT);self.assertEqual('/siyk-test-run-t3',r['command']);self.assertTrue(r['valid']);self.assertIsNone(r['strength']);self.assertTrue(any('ignored' in x for x in r['warnings']))
 def test_git_flags(self):
  r=route('/siyk-git-sync main --pr --allow-risk=all --no-test',ROOT);self.assertTrue(r['valid']);self.assertEqual('main',r['branch']);self.assertEqual(['--pr','--allow-risk=all','--no-test'],r['flags'])
 def test_unknown_flag_invalid(self):
  self.assertFalse(route('/siyk-git-sync --force',ROOT)['valid'])
if __name__=='__main__':unittest.main()
