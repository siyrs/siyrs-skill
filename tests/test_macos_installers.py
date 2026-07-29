from pathlib import Path
import shutil,subprocess,unittest
ROOT=Path(__file__).resolve().parents[1]
class MacInstallerTests(unittest.TestCase):
    def test_bash_installers_avoid_bash4_and_gnu_find_only_features(self):
        for rel in ('adapters/claude-code/install.sh','adapters/codex/install.sh'):
            text=(ROOT/rel).read_text();self.assertNotIn('mapfile',text);self.assertNotIn('-mindepth',text);self.assertNotIn('-maxdepth',text)
    @unittest.skipUnless(shutil.which('bash'),'bash required')
    def test_bash_syntax(self):
        for rel in ('adapters/claude-code/install.sh','adapters/codex/install.sh'):subprocess.run(['bash','-n',str(ROOT/rel)],check=True)
if __name__=='__main__':unittest.main()
