from pathlib import Path

import pytest

from .. import TransformerAcceptanceTest


@pytest.fixture(scope="session")
def transformer_relative_path():
    cwd = Path.cwd()
    transformer_abs_path = Path(Path(__file__).parent, "ExternalTransformer.py")
    return transformer_abs_path.relative_to(cwd)


@pytest.fixture(scope="session")
def disabled_transformer_relative_path():
    cwd = Path.cwd()
    transformer_abs_path = Path(Path(__file__).parent, "ExternalDisabledTransformer.py")
    return transformer_abs_path.relative_to(cwd)


@pytest.fixture(scope="session")
def transformer_absolute_path():
    return Path(Path(__file__).parent, "ExternalTransformer.py")


@pytest.fixture(scope="session")
def disabled_transformer_absolute_path():
    return Path(Path(__file__).parent, "ExternalDisabledTransformer.py")


class TestExternalTransformer(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "ExternalTransformer"

    def test_transform_absolute_path(self, transformer_absolute_path):
        self.run_tidy(args=f"--transform {transformer_absolute_path}:param=2".split(), source="tests.robot")
        self.compare_file("tests.robot")

    def test_transform_relative_path(self, transformer_relative_path):
        self.run_tidy(args=f"--transform {transformer_relative_path}:param=2".split(), source="tests.robot")
        self.compare_file("tests.robot")

    def test_load_absolute_path(self, transformer_absolute_path):
        self.run_tidy(args=f"--load-transformers {transformer_absolute_path}:param=2".split(), source="tests.robot")
        self.compare_file("tests.robot", expected_name="tests_with_defaults.robot")

    def test_load_relative_path(self, transformer_relative_path):
        self.run_tidy(args=f"--load-transformers {transformer_relative_path}:param=2".split(), source="tests.robot")
        self.compare_file("tests.robot", expected_name="tests_with_defaults.robot")

    def test_transform_disabled_absolute_path(self, disabled_transformer_absolute_path):
        self.run_tidy(args=f"--transform {disabled_transformer_absolute_path}".split(), source="tests.robot")
        self.compare_file("tests.robot", expected_name="tests_lowercase.robot")

    def test_transform_disabled_relative_path(self, disabled_transformer_relative_path):
        self.run_tidy(args=f"--transform {disabled_transformer_relative_path}".split(), source="tests.robot")
        self.compare_file("tests.robot", expected_name="tests_lowercase.robot")

    def test_load_disabled_absolute_path(self, disabled_transformer_absolute_path):
        self.run_tidy(args=f"--load-transformers {disabled_transformer_absolute_path}".split(), source="tests.robot")
        self.compare_file("tests.robot", expected_name="tests_only_defaults.robot")

    def test_load_disabled_relative_path(self, disabled_transformer_relative_path):
        self.run_tidy(args=f"--load-transformers {disabled_transformer_relative_path}".split(), source="tests.robot")
        self.compare_file("tests.robot", expected_name="tests_only_defaults.robot")
