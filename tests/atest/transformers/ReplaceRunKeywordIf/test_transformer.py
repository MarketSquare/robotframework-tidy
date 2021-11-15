from .. import run_tidy_and_compare


class TestReplaceRunKeywordIf:
    TRANSFORMER_NAME = "ReplaceRunKeywordIf"

    def test_run_keyword_if_replaced_selected(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source="tests.robot",
            expected="tests_selected.robot",
            config=" --startline 18 --endline 20",
        )

    def test_run_keyword_if_replaced(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source="tests.robot")

    def test_invalid_data(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source="invalid_data.robot")

    def test_golden_file(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source="golden.robot")

    def test_remove_useless_set_variable(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source="set_variable_workaround.robot")
