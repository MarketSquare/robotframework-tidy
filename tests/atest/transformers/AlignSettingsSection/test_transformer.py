import pytest

from .. import TransformerAcceptanceTest


class TestAlignSettingsSection(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "AlignSettingsSection"

    def test_align(self):
        self.compare(source="test.robot")

    def test_align_all_columns(self):
        self.compare(source="test.robot", expected="all_columns.robot", config=":up_to_column=0")

    def test_align_three_columns(self):
        self.compare(source="test.robot", expected="three_columns.robot", config=":up_to_column=3")

    def test_align_selected_whole(self):
        self.compare(
            source="test.robot",
            expected="selected_whole.robot",
            config=" --startline 1 --endline 25",
        )

    def test_align_selected_part(self):
        self.compare(
            source="test.robot",
            expected="selected_part.robot",
            config=" --startline 9 --endline 14",
        )

    def test_empty_lines_inside_statement(self):
        # bug from #75
        self.compare(source="empty_lines.robot")

    def test_continued_statement_style(self):
        self.compare(source="multiline_keywords.robot")

    def test_continued_statement_style_all_columns(self):
        self.compare(
            source="multiline_keywords.robot",
            expected="multiline_keywords_all_col.robot",
            config=":up_to_column=3",
        )

    @pytest.mark.parametrize("indent", (0, 2, 20))
    def test_continued_statement_style_all_columns_configure_indent(self, indent):
        self.compare(
            source="multiline_keywords.robot",
            expected=f"multiline_keywords_{indent}indent.robot",
            config=f":up_to_column=3:argument_indent={indent}",
        )

    def test_multiline_with_blank_line(self):
        self.compare(source="blank_line_doc.robot")

    def test_doc_multiline_and_whitespace(self):
        self.compare(source="blank_line_and_whitespace.robot")

    def test_fixed_test(self):
        self.compare(source="test.robot", expected="test_fixed.robot", config=":min_width=35")

    def test_fixed_all_columns(self):
        self.compare(
            source="test.robot",
            expected="all_columns_fixed.robot",
            config=":min_width=20:up_to_column=0",
        )

    def test_disablers(self):
        self.compare(source="test_disablers.robot")

    def test_argument_indents(self):
        self.compare(source="argument_indents.robot")
