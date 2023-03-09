from .. import TransformerAcceptanceTest


class TestBrowserDeprecateClick(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "BrowserDeprecateClick"

    def test_transformer(self):
        self.compare(source="test.robot", expected="test.robot")
