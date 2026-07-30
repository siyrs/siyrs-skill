from pathlib import Path
import sys,unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from route_command import route
class RouteTests(unittest.TestCase):
    def test_explicit_branch_flag(self):
        result=route('/siyk-git-sync --branch feature/test --pr note',ROOT);self.assertTrue(result['valid']);self.assertEqual('feature/test',result['branch']);self.assertEqual('note',result['extra'])
    def test_positional_natural_language_is_not_branch(self):
        result=route('/siyk-git-sync 同步这次权限修改',ROOT);self.assertIsNone(result['branch']);self.assertEqual('同步这次权限修改',result['extra'])
    def test_invalid_branch_rejected(self):
        result=route('/siyk-git-sync --branch bad..name',ROOT);self.assertFalse(result['valid']);self.assertTrue(any('invalid Git branch' in x for x in result['warnings']))
    def test_no_test_is_compatibility_warning(self):
        result=route('/siyk-git-commit --no-test',ROOT);self.assertTrue(result['valid']);self.assertTrue(any('already disable tests by default' in x for x in result['warnings']))
    def test_tier_strength_rejected(self):self.assertFalse(route('/siyk-test-run-t2 quick',ROOT)['valid'])
    def test_legacy_routes(self):self.assertEqual('/siyk-test-add',route('/siyk-test-new',ROOT)['command'])
if __name__=='__main__':unittest.main()
