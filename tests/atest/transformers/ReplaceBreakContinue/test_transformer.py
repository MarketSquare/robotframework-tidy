import pytest

from .. import run_tidy_and_compare


class TestReplaceBreakContinue:
    TRANSFORMER_NAME = "ReplaceBreakContinue"

    @pytest.mark.parametrize("source", ["test.robot", "errors.robot"])
    def test_transformer(self, source):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source=source)
