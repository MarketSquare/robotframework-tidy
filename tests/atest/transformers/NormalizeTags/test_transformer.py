from .. import run_tidy_and_compare, run_tidy


class TestNormalizeTags:
    TRANSFORMER_NAME = "NormalizeTags"

    def test_default(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source="tests.robot", expected="lowercase.robot")

    def test_lowercase(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source="tests.robot",
            expected="lowercase.robot",
            config=f":case=lowercase:normalize_case=True",
        )

    def test_uppercase(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME, source="tests.robot", expected="uppercase.robot", config=f":case=uppercase"
        )

    def test_titlecase(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME, source="tests.robot", expected="titlecase.robot", config=f":case=titlecase"
        )

    def test_wrong_case(self):
        result = run_tidy(
            self.TRANSFORMER_NAME,
            args=f"--transform {self.TRANSFORMER_NAME}:case=invalid".split(),
            source="tests.robot",
            exit_code=1,
        )
        expected_output = (
            f"Error: {self.TRANSFORMER_NAME}: Invalid 'case' parameter value: 'invalid'. "
            f"Supported cases: lowercase, uppercase, titlecase.\n"
        )
        assert expected_output == result.output

    def test_only_remove_duplicates(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source="duplicates.robot", config=f":normalize_case=False")
