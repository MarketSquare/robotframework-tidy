from pathlib import Path

from tests.atest import MultipleConfigsTest


class TestMultipleConfigs(MultipleConfigsTest):
    TEST_DIR = Path(__file__).parent.name

    def test(self, tmpdir):
        self.run_tidy(tmpdir)
        self.compare_files(tmpdir, "expected")

    def test_with_config_option(self, tmpdir):
        """Config option should stop from loading other configuration files."""
        config_path = tmpdir / self.TEST_DIR / "root" / "pyproject.toml"
        args = ["--config", str(config_path)]
        self.run_tidy(tmpdir, args)
        self.compare_files(tmpdir, "expected_config_option")
