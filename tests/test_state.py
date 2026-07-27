from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from state import load, save, update_state


class StateTests(unittest.TestCase):
    def test_default_and_round_trip(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / ".siyrs" / "state.json"
            data = load(path)
            self.assertEqual(1, data["version"])
            updated = update_state(data, kind="full", mode="strict", commit="abc123")
            save(path, updated)
            loaded = load(path)
            self.assertEqual("abc123", loaded["last_full_test_commit"])
            self.assertEqual("strict", loaded["last_full_test_mode"])

    def test_update_requires_commit_or_fingerprint(self):
        with self.assertRaises(ValueError):
            update_state(load(Path("missing.json")), kind="incremental", mode="standard")

    def test_rejects_unsupported_version(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            path.write_text('{"version": 999}', encoding="utf-8")
            with self.assertRaises(ValueError):
                load(path)


if __name__ == "__main__":
    unittest.main()
