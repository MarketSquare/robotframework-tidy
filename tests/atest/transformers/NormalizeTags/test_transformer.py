from .. import TransformerAcceptanceTest


class TestNormalizeTags(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "NormalizeTags"

    def test_default(self):
        self.compare(source="tests.robot", expected="lowercase.robot")

    def test_lowercase(self):
        self.compare(
            source="tests.robot",
            expected="lowercase.robot",
            config=f":case=lowercase:normalize_case=True",
        )

    def test_uppercase(self):
        self.compare(source="tests.robot", expected="uppercase.robot", config=f":case=uppercase")

    def test_titlecase(self):
        self.compare(source="tests.robot", expected="titlecase.robot", config=f":case=titlecase")

    def test_wrong_case(self):
        result = self.run_tidy(
            args=f"--transform {self.TRANSFORMER_NAME}:case=invalid".split(),
            source="tests.robot",
            exit_code=1,
        )
        expected_output = (
            f"Importing 'robotidy.transformers.{self.TRANSFORMER_NAME}' failed: "
            "Creating instance failed: BadOptionUsage: "
            f"Invalid configurable value: 'invalid' for case for {self.TRANSFORMER_NAME}"
            f" transformer. Supported cases: lowercase, uppercase, titlecase."
        )
        assert expected_output in str(result.exception)

    def test_only_remove_duplicates(self):
        self.compare(source="duplicates.robot", config=f":normalize_case=False")
