from .. import run_tidy_and_compare


class TestNormalizeReturns:
    TRANSFORMER_NAME = "NormalizeReturns"

    def test_transformer(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source="test.robot", expected="test.robot")

    def test_return_from_keyword(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source="return_from_keyword.robot", expected="return_from_keyword.robot")
