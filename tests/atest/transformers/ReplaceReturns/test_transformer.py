import pytest

from .. import TransformerAcceptanceTest


class TestReplaceReturns(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "ReplaceReturns"

    @pytest.mark.parametrize(
        "source",
        [
            "return_from_keyword.robot",
            "return_from_keyword_if.robot",
            "test.robot",
        ],
    )
    def test_transformer(self, source):
        self.compare(source=source)

    @pytest.mark.parametrize(
        "source",
        [
            "errors.robot",
            "run_keyword_and_return.robot",
            "run_keyword_and_return_if.robot",
        ],
    )
    def test_should_not_modify(self, source):
        self.compare(source=source, not_modified=True)

    def test_return_selected(self):
        self.compare(
            source="test.robot",
            expected="test_selected.robot",
            config=" --startline 10 --endline 17",
        )

    def test_return_from_keyword_if_selected(self):
        self.compare(
            source="return_from_keyword_if.robot",
            expected="return_from_keyword_if_selected.robot",
            config=" --startline 11 --endline 15",
        )

    def test_disablers(self):
        self.compare(source="replace_returns_disablers.robot", not_modified=True)
