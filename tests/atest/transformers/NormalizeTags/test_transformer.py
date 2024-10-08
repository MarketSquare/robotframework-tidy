import pytest

from tests.atest import TransformerAcceptanceTest


class TestNormalizeTags(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "NormalizeTags"

    def test_default(self):
        self.compare(source="tests.robot", expected="lowercase.robot")

    def test_lowercase(self):
        self.compare(
            source="tests.robot",
            expected="lowercase.robot",
            config=":case=lowercase:normalize_case=True",
        )

    def test_uppercase(self):
        self.compare(source="tests.robot", expected="uppercase.robot", config=":case=uppercase")

    def test_titlecase(self):
        self.compare(source="tests.robot", expected="titlecase.robot", config=":case=titlecase")

    def test_wrong_case(self):
        result = self.run_tidy(
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
        self.compare(source="duplicates.robot", config=":normalize_case=False")

    @pytest.mark.parametrize(
        "disablers",
        ["disablers.robot", "disablers2.robot", "disablers3.robot", "disablers4.robot"],
    )
    def test_disablers(self, disablers):
        self.compare(source=disablers, not_modified=True)

    @pytest.mark.parametrize("indent", [2, 4])
    @pytest.mark.parametrize("spaces", [2, 4])
    def test_spacing(self, spaces, indent):
        self.compare(
            source="spacing.robot",
            expected=f"spacing_{indent}indent_{spaces}spaces.robot",
            config=f" --spacecount {spaces} --indent {indent}",
        )

    def test_rf6(self):
        self.compare(source="rf6.robot", target_version=">=6", not_modified=True)

    def test_preserve_format(self):
        self.compare(
            source="preserve_format.robot",
            expected="preserve_format_enabled.robot",
            config=":preserve_format=True",
        )

    def test_preserve_format_do_not_normalize_case(self):
        self.compare(
            source="preserve_format.robot",
            config=":preserve_format=True:normalize_case=False",
            not_modified=True,
        )

    def test_ignore_format(self):
        self.compare(source="preserve_format.robot", expected="preserve_format_default.robot")

    @pytest.mark.parametrize("case_function", ["lowercase", "uppercase", "titlecase"])
    def test_variable_in_tag(self, case_function: str):
        self.compare(
            source="variables_in_tags.robot",
            expected=f"variables_in_tags_{case_function}.robot",
            config=f":case={case_function}",
            target_version=">=6",
        )
