from pathlib import Path

from tests.atest import MultipleConfigsTest


class TestMultipleConfigs(MultipleConfigsTest):
    TEST_DIR = Path(__file__).parent.name

    def test(self, tmpdir):
        self.run_tidy(tmpdir)
        self.compare_files(tmpdir, "expected")
