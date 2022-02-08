from pathlib import Path

from .. import TransformerAcceptanceTest


class TestExternalTransformer(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "ExternalTransformer"

    def test_external_transformer_works(self):
        transformer_path = Path(Path(__file__).parent, "ExternalTransformer.py")
        self.run_tidy(args=f"--transform {transformer_path}:param=2".split(), source="tests.robot")
        self.compare_file("tests.robot")
