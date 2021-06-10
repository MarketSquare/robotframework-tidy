import pytest

from .. import run_tidy_and_compare, run_tidy


class TestOrderSettings:
    TRANSFORMER_NAME = 'OrderSettings'

    def test_order(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source='test.robot')

    @pytest.mark.parametrize('keyword_before, keyword_after, test_before, test_after, expected', [
        (
                'documentation,tags,timeout,arguments',
                'teardown,return',
                'documentation,tags,template,timeout,setup',
                'teardown',
                'custom_order_default.robot'
        ),
        (
                '',
                'documentation,tags,timeout,arguments,teardown,return',
                '',
                'documentation,tags,template,timeout,setup,teardown',
                'custom_order_all_end.robot'
        ),
        (
                None,
                None,
                None,
                '',
                'custom_order_without_test_teardown.robot'
        )
    ])
    def test_custom_order(self, keyword_before, keyword_after, test_before, test_after, expected):
        config = ''
        if keyword_before is not None:
            config += f':keyword_before={keyword_before}'
        if keyword_after is not None:
            config += f':keyword_after={keyword_after}'
        if test_before is not None:
            config += f':test_before={test_before}'
        if test_after is not None:
            config += f':test_after={test_after}'
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source='test.robot',
            expected=expected,
            config=config
        )

    def test_custom_order_invalid_param(self):
        result = run_tidy(
            self.TRANSFORMER_NAME,
            args=f'--transform {self.TRANSFORMER_NAME}:keyword_before=documentation:keyword_after=tags,invalid'.split(),
            source='test.robot',
            exit_code=1
        )
        expected_output = f"Importing 'robotidy.transformers.{self.TRANSFORMER_NAME}' failed: " \
                          "Creating instance failed: BadOptionUsage: " \
                          f"Invalid configurable value: 'tags,invalid' for order for OrderSettings transformer." \
                          f" Custom order should be provided in comma separated list with valid setting names:\n" \
                          f"['arguments', 'documentation', 'return', 'tags', 'teardown', 'timeout']"
        assert expected_output in str(result.exception)
