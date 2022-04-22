from .. import TransformerAcceptanceTest


class TestRenameTestCases(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "RenameTestCases"

    def test_transformer(self):
        self.compare(source="test.robot", expected="test.robot")

    def test_test_without_name(self):
        self.compare(source="empty_test_name.robot", not_modified=True)

    def test_replace_pattern_to_empty(self):
        self.compare(
            source="test.robot",
            expected="replace_pattern_empty.robot",
            config=r":replace_pattern=[A-Z]+-\d{1,}",
        )

    def test_replace_pattern_to_placeholder(self):
        self.compare(
            source="test.robot",
            expected="replace_pattern_placeholder.robot",
            config=r":replace_pattern=[A-Z]+-\d{1,}:replace_to=PLACEHOLDER",
        )

    def test_replace_pattern_special_chars(self):
        self.compare(
            source="test.robot",
            expected="replace_pattern_special_chars.robot",
            config=r":replace_pattern=[\:?$@]",
        )

    def test_selected_lines(self):
        self.compare(source="test.robot", expected="selected.robot", config=" --startline 5 --endline 5")

    def test_invalid_pattern(self):
        result = self.run_tidy(
            args=rf"--transform {self.TRANSFORMER_NAME}:replace_pattern=[\911]".split(),
            source="test.robot",
            exit_code=1,
        )
        expected_output = (
            rf"Error: {self.TRANSFORMER_NAME}: Invalid 'replace_pattern' parameter value: '[\911]'. "
            "It should be a valid regex expression. Regex error: 'bad escape \\9'\n"
        )
        assert expected_output == result.output

    def test_disablers(self):
        self.compare(source="disablers.robot", not_modified=True)
