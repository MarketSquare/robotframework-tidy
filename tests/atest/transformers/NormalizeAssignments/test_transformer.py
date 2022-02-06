import pytest

from .. import TransformerAcceptanceTest


class TestNormalizeAssignments(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "NormalizeAssignments"

    @pytest.mark.parametrize(
        "filename", ["common_remove.robot", "common_equal_sign.robot", "common_space_and_equal_sign.robot"]
    )
    def test_autodetect(self, filename):
        self.compare(source=filename)

    @pytest.mark.parametrize("filename", ["common_remove", "common_equal_sign", "common_space_and_equal_sign"])
    def test_autodetect_variables(self, filename):
        self.compare(
            source=filename + ".robot",
            expected=filename + "_variables.robot",
            config=":equal_sign_type_variables=autodetect",
        )

    def test_remove(self):
        self.compare(source="tests.robot", expected="remove.robot", config=":equal_sign_type=remove")

    def test_add_equal_sign(self):
        self.compare(
            source="tests.robot",
            expected="equal_sign.robot",
            config=":equal_sign_type=equal_sign",
        )

    def test_add_space_and_equal_sign(self):
        self.compare(
            source="tests.robot",
            expected="space_and_equal_sign.robot",
            config=":equal_sign_type=space_and_equal_sign",
        )

    @pytest.mark.parametrize("param_name", ["equal_sign_type", "equal_sign_type_variables"])
    def test_invalid_equal_sign_type(self, param_name):
        result = self.run_tidy(
            args=f"--transform {self.TRANSFORMER_NAME}:{param_name}==".split(),
            source="tests.robot",
            exit_code=1,
        )
        expected_output = (
            f"Importing 'robotidy.transformers.{self.TRANSFORMER_NAME}' failed: "
            "Creating instance failed: BadOptionUsage: Invalid configurable value: = "
            f"for {param_name} for AssignmentNormalizer transformer. "
            "Possible values:\n    remove\n    equal_sign\n    space_and_equal_sign"
        )
        assert expected_output in str(result.exception)
