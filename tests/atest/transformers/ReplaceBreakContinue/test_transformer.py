from .. import TransformerAcceptanceTest


class TestReplaceBreakContinue(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "ReplaceBreakContinue"

    def test_transformer(self):
        self.compare(source="test.robot")

    def test_with_errors(self):
        self.compare(source="errors.robot", not_modified=True)
