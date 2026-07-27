from pathlib import Path
from tempfile import TemporaryDirectory
import json
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from detect_project import detect


class DetectProjectTests(unittest.TestCase):
    def test_detects_android(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "app/src/main").mkdir(parents=True)
            (root / "app/src/main/AndroidManifest.xml").write_text("<manifest/>", encoding="utf-8")
            (root / "build.gradle.kts").write_text("plugins {}", encoding="utf-8")
            result = detect(root)
            self.assertIn("android", result["types"])
            self.assertEqual("high", result["confidence"])

    def test_detects_fullstack_from_java_and_frontend(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "src/components").mkdir(parents=True)
            (root / "src/components/App.tsx").write_text("export default 1", encoding="utf-8")
            (root / "package.json").write_text(json.dumps({"dependencies": {"react": "1"}}), encoding="utf-8")
            (root / "pom.xml").write_text("<project/>", encoding="utf-8")
            result = detect(root)
            self.assertIn("java-backend-or-library", result["types"])
            self.assertIn("full-stack-web", result["types"])

    def test_detects_nested_manifests_and_monorepo(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "frontend").mkdir()
            (root / "backend").mkdir()
            (root / "frontend/package.json").write_text("{}", encoding="utf-8")
            (root / "backend/pyproject.toml").write_text("[project]\nname='x'", encoding="utf-8")
            result = detect(root)
            self.assertIn("possible-monorepo", result["types"])
            self.assertIn("backend", result["module_roots"])
            self.assertIn("frontend", result["module_roots"])

    def test_unknown_project(self):
        with TemporaryDirectory() as tmp:
            result = detect(Path(tmp))
            self.assertEqual(["unknown-custom"], result["types"])
            self.assertEqual("low", result["confidence"])


if __name__ == "__main__":
    unittest.main()
