import pytest

from tests.atest import TransformerAcceptanceTest


class TestRenameVariables(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "RenameVariables"

    def test_transformer(self):
        self.compare(source="test.robot")

    def test_template(self):
        self.compare(source="test_template.robot")

    def test_try_except(self):
        self.compare(source="try_except.robot", target_version=">=5.0")

    def test_inline_if(self):
        self.compare(source="inline_if.robot", target_version=">=5.0")

    def test_disablers(self):
        self.compare(source="disablers.robot")

    def test_lower_case(self):
        self.compare(
            source="test.robot",
            expected="test_lower.robot",
            config=":settings_section_case=lower:variables_section_case=lower:unknown_variables_case=lower",
        )

    def test_ignore_unknown_case(self):
        self.compare(source="test.robot", expected="test_ignore_unknown.robot", config=":unknown_variables_case=ignore")

    def test_ignore_settings_case(self):
        self.compare(
            source="test.robot", expected="test_ignore_settings_case.robot", config=":settings_section_case=ignore"
        )

    def test_ignore_camel_case(self):
        self.compare(source="test.robot", expected="test_ignore_camel_case.robot", config=":convert_camel_case=False")

    def test_separator_underscore(self):
        self.compare(
            source="test.robot", expected="test_separator_underscore.robot", config=":variable_separator=space"
        )

    def test_return_and_set_globals(self):
        self.compare(source="return_and_set_global.robot")

    @pytest.mark.parametrize(
        "param_name, allowed",
        [
            ("settings_section_case", "upper, lower, ignore"),
            ("variables_section_case", "upper, lower, ignore"),
            ("unknown_variables_case", "upper, lower, ignore"),
        ],
    )
    def test_invalid_param(self, param_name, allowed):
        result = self.run_tidy(
            args=f"--transform {self.TRANSFORMER_NAME}:{param_name}=invalid".split(),
            source="test.robot",
            exit_code=1,
        )
        expected_output = (
            f"Error: {self.TRANSFORMER_NAME}: Invalid '{param_name}' parameter value: 'invalid'. "
            f"Invalid case type. Allowed case types are: {allowed}\n"
        )
        assert expected_output == result.output

    def test_invalid_variable_separator(self):
        result = self.run_tidy(
            args=f"--transform {self.TRANSFORMER_NAME}:variable_separator=invalid".split(),
            source="test.robot",
            exit_code=1,
        )
        expected_output = (
            f"Error: {self.TRANSFORMER_NAME}: Invalid 'variable_separator' parameter value: 'invalid'. "
            f"Allowed values are: underscore, space\n"
        )
        assert expected_output == result.output
