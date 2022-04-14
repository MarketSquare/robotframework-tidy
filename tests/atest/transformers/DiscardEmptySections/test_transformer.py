from .. import TransformerAcceptanceTest


class TestDiscardEmptySections(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "DiscardEmptySections"

    def test_removes_empty_sections(self):
        self.compare(source="removes_empty_sections.robot", config=":allow_only_comments=False")

    def test_removes_empty_sections_except_comments(self):
        self.compare(
            source="removes_empty_sections.robot",
            expected="removes_empty_sections_except_comments.robot",
        )

    def test_remove_selected_empty_node(self):
        self.compare(
            source="removes_empty_sections.robot",
            expected="removes_selected_empty_section.robot",
            config=" --startline 17 --endline 18",
        )

    def test_disablers(self):
        self.compare(source="removes_empty_sections_disablers.robot")
