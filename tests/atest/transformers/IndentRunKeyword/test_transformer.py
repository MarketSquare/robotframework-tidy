from .. import TransformerAcceptanceTest


class TestIndentRunKeyword(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "IndentRunKeyword"

    def test_run_keyword(self):
        self.compare(source="run_keyword.robot")

    def test_run_keyword_in_settings(self):
        # TODO: remove not_modified when settings will be supported
        self.compare(source="settings.robot", not_modified=True)
