from .. import TransformerAcceptanceTest


class TestInlineIf(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "InlineIf"

    def test_transformer(self):
        self.compare(source="test.robot")

    def test_transformer_skip_else(self):
        self.compare(source="test.robot", expected="test_skip_else.robot", config=":skip_else=True")
