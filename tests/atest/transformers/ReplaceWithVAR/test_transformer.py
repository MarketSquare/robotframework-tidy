from tests.atest import TransformerAcceptanceTest


class TestReplaceWithVAR(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "ReplaceWithVAR"

    def test_transformer(self):
        self.compare(source="test.robot", expected="test.robot")
