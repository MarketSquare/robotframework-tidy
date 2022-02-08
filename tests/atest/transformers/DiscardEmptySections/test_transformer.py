from .. import run_tidy_and_compare


class TestDiscardEmptySections:
    TRANSFORMER_NAME = "DiscardEmptySections"

    def test_removes_empty_sections(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source="removes_empty_sections.robot", config=":allow_only_comments=False")

    def test_removes_empty_sections_except_comments(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source="removes_empty_sections.robot",
            expected="removes_empty_sections_except_comments.robot",
        )

    def test_remove_selected_empty_node(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source="removes_empty_sections.robot",
            expected="removes_selected_empty_section.robot",
            config=" --startline 17 --endline 18",
        )
