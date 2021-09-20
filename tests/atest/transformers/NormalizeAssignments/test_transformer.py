import pytest

from .. import run_tidy_and_compare, run_tidy


class TestNormalizeAssignments:
    TRANSFORMER_NAME = 'NormalizeAssignments'

    @pytest.mark.parametrize('filename', [
        'common_remove.robot',
        'common_equal_sign.robot',
        'common_space_and_equal_sign.robot'
    ])
    def test_autodetect(self, filename):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source=filename)

    @pytest.mark.parametrize('filename', [
        'common_remove',
        'common_equal_sign',
        'common_space_and_equal_sign'
    ])
    def test_autodetect_variables(self, filename):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source=filename + '.robot',
            expected=filename + '_variables.robot',
            config=':equal_sign_type_variables=autodetect'
        )

    def test_remove(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source='tests.robot',
            expected='remove.robot',
            config=':equal_sign_type=remove'
        )

    def test_add_equal_sign(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source='tests.robot',
            expected='equal_sign.robot',
            config=':equal_sign_type=equal_sign'
        )

    def test_add_space_and_equal_sign(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source='tests.robot',
            expected='space_and_equal_sign.robot',
            config=':equal_sign_type=space_and_equal_sign'
        )

    @pytest.mark.parametrize('param_name', ['equal_sign_type', 'equal_sign_type_variables'])
    def test_invalid_equal_sign_type(self, param_name):
        result = run_tidy(
            self.TRANSFORMER_NAME,
            args=f'--transform {self.TRANSFORMER_NAME}:{param_name}=='.split(),
            source='tests.robot',
            exit_code=1
        )
        expected_output = f"Importing 'robotidy.transformers.{self.TRANSFORMER_NAME}' failed: " \
                          "Creating instance failed: BadOptionUsage: Invalid configurable value: = " \
                          f"for {param_name} for AssignmentNormalizer transformer. " \
                          "Possible values:\n    remove\n    equal_sign\n    space_and_equal_sign"
        assert expected_output in str(result.exception)
