from pathlib import Path

from .. import TransformerAcceptanceTest


class TestExternalTransformer(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "ExternalTransformer"

    def test_external_transformer_absolute_path(self):
        transformer_path = Path(Path(__file__).parent, "ExternalTransformer.py")
        self.run_tidy(args=f"--transform {transformer_path}:param=2".split(), source="tests.robot")
        self.compare_file("tests.robot")

    def test_external_transformer_relative_path(self):
        cwd = Path.cwd()
        transformer_abs_path = Path(Path(__file__).parent, "ExternalTransformer.py")
        transformer_path = transformer_abs_path.relative_to(cwd)
        self.run_tidy(args=f"--transform {transformer_path}:param=2".split(), source="tests.robot")
        self.compare_file("tests.robot")
