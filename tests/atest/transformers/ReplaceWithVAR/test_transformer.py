from tests.atest import TransformerAcceptanceTest


class TestReplaceWithVAR(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "ReplaceWithVAR"

    def test_transformer(self):
        self.compare(source="test.robot", expected="test.robot")

    def test_too_long(self):
        self.compare(source="too_long.robot", config=f"-c {self.TRANSFORMER_NAME}:enabled=True", run_all=True)
