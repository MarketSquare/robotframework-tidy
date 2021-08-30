from .. import run_tidy_and_compare, run_tidy


class TestRenameTestCases:
    TRANSFORMER_NAME = 'RenameTestCases'

    def test_transformer(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source='test.robot', expected='test.robot')

    def test_test_without_name(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source='empty_test_name.robot', expected='empty_test_name.robot')

    def test_replace_pattern_to_empty(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source='test.robot',
            expected='replace_pattern_empty.robot',
            config=r':replace_pattern=[A-Z]+-\d{1,}'
        )

    def test_replace_pattern_to_placeholder(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source='test.robot',
            expected='replace_pattern_placeholder.robot',
            config=r':replace_pattern=[A-Z]+-\d{1,}:replace_to=PLACEHOLDER'
        )

    def test_replace_pattern_special_chars(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source='test.robot',
            expected='replace_pattern_special_chars.robot',
            config=r':replace_pattern=[\:?$@]'
        )

    def test_selected_lines(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source='test.robot',
            expected='selected.robot',
            config=' --startline 5 --endline 5'
        )

    def test_invalid_pattern(self):
        result = run_tidy(
            self.TRANSFORMER_NAME,
            args=rf'--transform {self.TRANSFORMER_NAME}:replace_pattern=[\911]'.split(),
            source='test.robot',
            exit_code=1
        )
        expected_output = f"Importing 'robotidy.transformers.{self.TRANSFORMER_NAME}' failed: " \
                          "Creating instance failed: BadOptionUsage: Invalid configurable value: " \
                          rf"'[\911]' for replace_pattern in {self.TRANSFORMER_NAME} transformer. " \
                          "It should be valid regex expression. Regex error: 'bad escape \\9'"
        assert expected_output in str(result.exception)
