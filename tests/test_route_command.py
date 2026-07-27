from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from route_command import route


class RouteCommandTests(unittest.TestCase):
    def test_literal_test_full_defaults_to_strict(self):
        result = route("/siyk-test-full")
        self.assertTrue(result["matched"])
        self.assertEqual("/siyk-test-full", result["command"])
        self.assertEqual("strict", result["strength"])

    def test_literal_test_new_keeps_extra(self):
        result = route("/siyk-test-new quick 权限管理")
        self.assertEqual("quick", result["strength"])
        self.assertEqual("权限管理", result["extra"])
        self.assertEqual("/siyk-test-new quick 权限管理", result["normalized"])

    def test_chinese_aliases(self):
        full = route("全量沉淀测试 登录流程")
        self.assertEqual("/siyk-test-full", full["command"])
        self.assertEqual("strict", full["strength"])
        new = route("沉淀测试 新增功能")
        self.assertEqual("/siyk-test-new", new["command"])
        self.assertEqual("standard", new["strength"])
        sync = route("保存并同步远程仓库")
        self.assertEqual("/siyk-git-sync", sync["command"])

    def test_git_sync_parses_branch_and_flags(self):
        result = route("/siyk-git-sync main --pr --no-test 发布首版")
        self.assertEqual("main", result["branch"])
        self.assertEqual(["--pr", "--no-test"], result["flags"])
        self.assertEqual("发布首版", result["extra"])

    def test_unrelated_text_does_not_route(self):
        self.assertFalse(route("请帮我写一个测试") ["matched"])


if __name__ == "__main__":
    unittest.main()
