import pytest

from .. import run_tidy_and_compare


class TestAlignSettingsSection:
    TRANSFORMER_NAME = "AlignSettingsSection"

    def test_align(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source="test.robot")

    def test_align_all_columns(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME, source="test.robot", expected="all_columns.robot", config=":up_to_column=0"
        )

    def test_align_three_columns(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME, source="test.robot", expected="three_columns.robot", config=":up_to_column=3"
        )

    def test_align_selected_whole(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source="test.robot",
            expected="selected_whole.robot",
            config=" --startline 1 --endline 25",
        )

    def test_align_selected_part(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source="test.robot",
            expected="selected_part.robot",
            config=" --startline 9 --endline 14",
        )

    def test_empty_lines_inside_statement(self):
        # bug from #75
        run_tidy_and_compare(self.TRANSFORMER_NAME, source="empty_lines.robot")

    def test_continued_statement_style(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source="multiline_keywords.robot")

    def test_continued_statement_style_all_columns(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source="multiline_keywords.robot",
            expected="multiline_keywords_all_col.robot",
            config=":up_to_column=3",
        )

    @pytest.mark.parametrize("indent", (0, 2, 20))
    def test_continued_statement_style_all_columns_configure_indent(self, indent):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source="multiline_keywords.robot",
            expected=f"multiline_keywords_{indent}indent.robot",
            config=f":up_to_column=3:argument_indent={indent}",
        )

    def test_multiline_with_blank_line(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source="blank_line_doc.robot")

    def test_doc_multiline_and_whitespace(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source="blank_line_and_whitespace.robot")
