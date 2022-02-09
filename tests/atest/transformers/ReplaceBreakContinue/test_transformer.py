import pytest

from .. import TransformerAcceptanceTest


class TestReplaceBreakContinue(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "ReplaceBreakContinue"

    @pytest.mark.parametrize("source", ["test.robot", "errors.robot"])
    def test_transformer(self, source):
        self.compare(source=source)
