import pytest

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
            f"Error: {self.TRANSFORMER_NAME}: Invalid 'case' parameter value: 'invalid'. "
            f"Supported cases: lowercase, uppercase, titlecase.\n"
        )
        assert expected_output == result.output

    def test_only_remove_duplicates(self):
        self.compare(source="duplicates.robot", config=f":normalize_case=False")

    def test_disablers(self):
        self.compare(source="disablers.robot", not_modified=True)

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
