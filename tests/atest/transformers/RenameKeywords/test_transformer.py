from tests.atest import TransformerAcceptanceTest


class TestRenameKeywords(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "RenameKeywords"

    def test_transformer(self):
        self.compare(source="test.robot", expected="test.robot")

    def test_transform_library(self):
        self.compare(source="test.robot", expected="test_transform_library.robot", config=":ignore_library=False")

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
            rf"Error: {self.TRANSFORMER_NAME}: Invalid 'replace_pattern' parameter value: '[\911]'. "
            "It should be a valid regex expression. Regex error: 'bad escape \\9'\n"
        )
        assert expected_output == result.output

    def test_with_library_name_ignore(self):
        self.compare(source="with_library_name.robot")

    def test_with_library_name_transform(self):
        self.compare(
            source="with_library_name.robot",
            expected="with_library_name_transform.robot",
            config=":ignore_library=False",
        )

    def test_disablers(self):
        self.compare(source="disablers.robot", not_modified=True)

    def test_run_keywords(self):
        self.compare(source="run_keywords.robot")

    def test_embedded_variables(self):
        self.compare(source="embedded_variables.robot")

    def test_embedded_with_pattern(self):
        self.compare(
            config=":replace_pattern=(?i)rename\s?with\s.+variable$:replace_to=New_Name_${keyword}_And_${var}",
            source="library_embedded_var_pattern.robot",
        )

    def test_underscore_handling_bugs(self):
        self.compare(source="bug537_538.robot")

    def test_no_title_case(self):
        self.compare(
            source="no_title_case.robot",
            config=":convert_title_case=False",
        )
