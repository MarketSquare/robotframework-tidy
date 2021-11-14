from .. import run_tidy_and_compare


class TestAddMissingEnd:
    TRANSFORMER_NAME = "AddMissingEnd"

    def test_transformer(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source="test.robot", expected="test.robot")

    def test_selected(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source="test.robot",
            expected="test_selected.robot",
            config=" --startline 161 --endline 183",
        )
