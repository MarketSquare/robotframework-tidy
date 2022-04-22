from .. import TransformerAcceptanceTest


class TestInlineIf(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "InlineIf"

    def test_transformer(self):
        self.compare(source="test.robot")

    def test_transformer_skip_else(self):
        self.compare(source="test.robot", expected="test_skip_else.robot", config=":skip_else=True:line_length=120")

    def test_invalid_if(self):
        self.compare(source="invalid_if.robot", not_modified=True)

    def test_invalid_inline_if(self):
        self.compare(source="invalid_inline_if.robot", not_modified=True, config=":line_length=120")

    def test_disablers(self):
        self.compare(source="test_disablers.robot")
