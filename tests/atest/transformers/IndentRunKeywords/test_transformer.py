from .. import TransformerAcceptanceTest


class TestIndentRunKeywords(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "IndentRunKeywords"

    def test_run_keyword(self):
        self.compare(source="run_keyword.robot")

    def test_indent_and(self):
        self.compare(source="run_keyword.robot", expected="indent_and.robot", config=":indent_and=True")

    def test_comments(self):
        self.compare(source="comments.robot")

    def test_run_keyword_in_settings(self):
        self.compare(source="settings.robot")

    def test_skip_settings(self):
        self.compare(source="settings.robot", not_modified=True, config=":skip_settings=True")
