from tests.atest import TransformerAcceptanceTest


class TestReplaceEmptyValues(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "ReplaceEmptyValues"

    def test_transformer(self):
        self.compare(source="test.robot", expected="test.robot")

    def test_skip_section(self):
        self.compare(source="test.robot", config=" --skip-sections=variables", not_modified=True)
