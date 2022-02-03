from .. import run_tidy_and_compare


class TestInlineIf:
    TRANSFORMER_NAME = "InlineIf"

    def test_transformer(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source="test.robot")

    def test_transformer_skip_else(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME, source="test.robot", expected="test_skip_else.robot", config=":skip_else=True"
        )
