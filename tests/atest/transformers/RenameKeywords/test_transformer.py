from .. import run_tidy_and_compare, run_tidy


class TestRenameKeywords:
    TRANSFORMER_NAME = 'RenameKeywords'

    def test_transformer(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source='test.robot', expected='test.robot')

    def test_renaming_pattern(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source='test.robot',
            expected='rename_pattern_partial.robot',
            config=r':replace_pattern=(?i)rename\s?me:replace_to=New_Shining_Name'
        )

    def test_renaming_whole_name_pattern(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source='test.robot',
            expected='rename_pattern_whole.robot',
            config=r':replace_pattern=(?i)^rename\s?me$:replace_to=New_Shining_Name'
        )

    def test_keep_underscores(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source='test.robot',
            expected='with_underscores.robot',
            config=r':remove_underscores=False'
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
                          "It should be a valid regex expression. Regex error: 'bad escape \\9'"
        assert expected_output in str(result.exception)
