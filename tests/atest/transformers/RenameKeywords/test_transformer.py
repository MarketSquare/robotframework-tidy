from .. import TransformerAcceptanceTest


class TestRenameKeywords(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "RenameKeywords"

    def test_transformer(self):
        self.compare(source="test.robot", expected="test.robot")

    def test_renaming_pattern(self):
        self.compare(
            source="test.robot",
            expected="rename_pattern_partial.robot",
            config=r":replace_pattern=(?i)rename\s?me:replace_to=New_Shining_Name",
        )

    def test_renaming_whole_name_pattern(self):
        self.compare(
            source="test.robot",
            expected="rename_pattern_whole.robot",
            config=r":replace_pattern=(?i)^rename\s?me$:replace_to=New_Shining_Name",
        )

    def test_keep_underscores(self):
        self.compare(
            source="test.robot",
            expected="with_underscores.robot",
            config=r":remove_underscores=False",
        )

    def test_invalid_pattern(self):
        result = self.run_tidy(
            args=rf"--transform {self.TRANSFORMER_NAME}:replace_pattern=[\911]".split(),
            source="test.robot",
            exit_code=1,
        )
        expected_output = (
            f"Importing 'robotidy.transformers.{self.TRANSFORMER_NAME}' failed: "
            "Creating instance failed: BadOptionUsage: Invalid configurable value: "
            rf"'[\911]' for replace_pattern in {self.TRANSFORMER_NAME} transformer. "
            "It should be a valid regex expression. Regex error: 'bad escape \\9'"
        )
        assert expected_output in str(result.exception)

    def test_with_library_name(self):
        self.compare(source="with_library_name.robot")
