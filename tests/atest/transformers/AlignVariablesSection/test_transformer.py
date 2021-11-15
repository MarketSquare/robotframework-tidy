from .. import run_tidy_and_compare


class TestAlignVariablesSection:
    TRANSFORMER_NAME = "AlignVariablesSection"

    def test_align_variables(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source="tests.robot")

    def test_align_three_columns(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME, source="tests.robot", expected="three_columns.robot", config=":up_to_column=3"
        )

    def test_align_all_columns(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME, source="tests.robot", expected="all_columns.robot", config=":up_to_column=0"
        )

    def test_align_with_optional_equal_signs(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source="optional_equal_sign.robot")

    def test_align_with_long_comment(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source="long_comment.robot")

    def test_align_selected_whole(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source="align_selected.robot",
            expected="align_selected_whole.robot",
            config=" --startline 5 --endline 17",
        )

    def test_align_selected_part(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source="align_selected.robot",
            expected="align_selected_part.robot",
            config=" --startline 10 --endline 12",
        )

    def test_multiline_with_blank(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source="multiline_with_blank.robot")
