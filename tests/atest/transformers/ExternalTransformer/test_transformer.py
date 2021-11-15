from pathlib import Path

from .. import run_tidy, compare_file


class TestExternalTransformer:
    def test_external_transformer_works(self):
        transformer_path = Path(Path(__file__).parent, "ExternalTransformer.py")
        run_tidy("ExternalTransformer", args=f"--transform {transformer_path}:param=2".split(), source="tests.robot")
        compare_file("ExternalTransformer", "tests.robot")
