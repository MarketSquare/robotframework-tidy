import pytest

from .. import run_tidy_and_compare


class TestReplaceReturns:
    TRANSFORMER_NAME = "ReplaceReturns"

    @pytest.mark.parametrize(
        "source",
        [
            "errors.robot",
            "return_from_keyword.robot",
            "return_from_keyword_if.robot",
            "run_keyword_and_return.robot",
            "run_keyword_and_return_if.robot",
            "test.robot",
        ],
    )
    def test_transformer(self, source):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source=source)

    def test_return_selected(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source="test.robot",
            expected="test_selected.robot",
            config=" --startline 10 --endline 17",
        )

    def test_return_from_keyword_if_selected(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source="return_from_keyword_if.robot",
            expected="return_from_keyword_if_selected.robot",
            config=" --startline 11 --endline 15",
        )
