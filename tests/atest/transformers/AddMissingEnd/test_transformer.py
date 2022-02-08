from .. import TransformerAcceptanceTest


class TestAddMissingEnd(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "AddMissingEnd"

    def test_transformer(self):
        self.compare(source="test.robot", expected="test.robot")

    def test_selected(self):
        self.compare(
            source="test.robot",
            expected="test_selected.robot",
            config=" --startline 166 --endline 188",
        )
