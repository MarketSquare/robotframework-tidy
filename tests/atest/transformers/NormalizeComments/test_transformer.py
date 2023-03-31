from .. import TransformerAcceptanceTest


class TestNormalizeComments(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "NormalizeComments"

    def test_transformer(self):
        self.compare(source="test.robot", expected="test.robot")
