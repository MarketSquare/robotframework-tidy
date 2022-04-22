from .. import TransformerAcceptanceTest


class TestAlignVariablesSection(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "AlignVariablesSection"

    def test_align_variables(self):
        self.compare(source="tests.robot")

    def test_align_three_columns(self):
        self.compare(source="tests.robot", expected="three_columns.robot", config=":up_to_column=3")

    def test_align_all_columns(self):
        self.compare(source="tests.robot", expected="all_columns.robot", config=":up_to_column=0")

    def test_align_with_optional_equal_signs(self):
        self.compare(source="optional_equal_sign.robot")

    def test_align_with_long_comment(self):
        self.compare(source="long_comment.robot")

    def test_align_selected_whole(self):
        self.compare(
            source="align_selected.robot",
            expected="align_selected_whole.robot",
            config=" --startline 5 --endline 17",
        )

    def test_align_selected_part(self):
        self.compare(
            source="align_selected.robot",
            expected="align_selected_part.robot",
            config=" --startline 10 --endline 12",
        )

    def test_multiline_with_blank(self):
        self.compare(source="multiline_with_blank.robot")

    def test_align_variables_skip(self):
        self.compare(source="tests.robot", expected="tests_skip.robot", config=":skip_types=dict,list")

    def test_align_variables_skip_scalar(self):
        self.compare(
            source="align_selected.robot",
            expected="align_selected_skip.robot",
            config=":skip_types=scalar",
        )

    def test_multiline_skip(self):
        self.compare(source="multiline_skip.robot", config=":skip_types=list,dict")

    def test_fixed_tests(self):
        self.compare(source="tests.robot", expected="tests_fixed.robot", config=":min_width=30")

    def test_fixed_tests_zero(self):
        self.compare(source="tests.robot", expected="tests_fixed_one.robot", config=":min_width=1")

    def test_fixed_all_columns(self):
        self.compare(
            source="tests.robot",
            expected="all_columns_fixed.robot",
            config=":min_width=20:up_to_column=0",
        )

    def test_disablers(self):
        self.compare(source="tests_disablers.robot")
