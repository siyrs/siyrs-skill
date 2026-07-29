from pathlib import Path
import sys, unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from route_command import route

class RouteCommandTests(unittest.TestCase):
    def test_test_defaults_and_aliases(self):
        self.assertEqual("strict", route("/siyk-test-run-t3")["strength"])
        self.assertEqual("quick", route("/siyk-test-run-t2")["strength"])
        self.assertIsNone(route("/siyk-test-run-t1")["strength"])
        self.assertEqual("standard", route("/siyk-test-add")["strength"])
        self.assertEqual("standard", route("沉淀测试 新功能")["strength"])
    def test_tier_aliases(self):
        self.assertEqual("/siyk-test-run-t1", route("跑t1")["command"])
        self.assertEqual("/siyk-test-run-t2", route("冒烟")["command"])
        self.assertEqual("/siyk-test-run-t3", route("全量")["command"])
    def test_commit_flags(self):
        r=route("/siyk-git-commit --no-test --allow-risk=RISK-001 feat: 保存")
        self.assertEqual(["--no-test","--allow-risk=RISK-001"],r["flags"])
        self.assertEqual("feat: 保存",r["extra"])
    def test_commit_bare_allow_risk(self):
        self.assertEqual(["--allow-risk"],route("/siyk-git-commit --allow-risk")["flags"])
    def test_alias_preserves_allow_risk_flag(self):
        r=route("本地保存 --allow-risk=RISK-002 feat: 保存")
        self.assertEqual(["--allow-risk=RISK-002"],r["flags"])
        self.assertEqual("alias:本地保存",r["source"])
    def test_sync_flags_and_branch(self):
        r=route("/siyk-git-sync main --pr --allow-risk=all --no-test")
        self.assertEqual("main",r["branch"])
        self.assertEqual(["--pr","--allow-risk=all","--no-test"],r["flags"])
    def test_unknown_flag_warns(self):
        self.assertEqual(["unknown flag: --force"],route("/siyk-git-sync --force")["warnings"])
    def test_unrelated_does_not_route(self):
        self.assertFalse(route("帮我写测试")["matched"])
if __name__=="__main__": unittest.main()
