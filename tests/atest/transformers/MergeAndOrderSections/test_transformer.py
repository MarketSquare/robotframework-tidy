import pytest

from .. import run_tidy_and_compare, run_tidy


class TestMergeAndOrderSections:
    TRANSFORMER_NAME = "MergeAndOrderSections"

    def test_merging_and_ordering(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source="tests.robot")

    def test_both_test_and_task(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source="both_test_and_task.robot")

    def test_multiple_header_comments(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source="multiple_header_comments.robot")

    def test_nested_blocks(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source="nested_blocks.robot")

    def test_nested_block_for(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source="nested_block_for.robot")

    def test_empty_section(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source="empty_section.robot")

    def test_parsing_error(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source="parsing_error.robot")

    def test_too_few_calls_in_keyword(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source="too_few_calls_in_keyword.robot")

    def test_default_order(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source="order.robot")

    def test_custom_order(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source="order.robot",
            expected="order_settings_comments_keywords_variables_testcases.robot",
            config=":order=settings,comments,keyword,variables,testcases",
        )

    def test_do_not_create_comment_section(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source="tests.robot",
            expected="tests_without_comment_section.robot",
            config=":create_comment_section=False",
        )

    @pytest.mark.parametrize(
        "parameter",
        [
            "settings,variables,testcases,keyword",
            "comments,settings,variables,testcases,variables,variables",
            "comments,settings,variables,testcases,variables,INVALID",
        ],
    )
    def test_invalid_order_parameter(self, parameter):
        result = run_tidy(
            self.TRANSFORMER_NAME,
            args=f"--transform {self.TRANSFORMER_NAME}:order={parameter}".split(),
            source="order.robot",
            exit_code=1,
        )
        expected_output = f"Error: {self.TRANSFORMER_NAME}: Invalid 'order' parameter value: '{parameter}'. " \
                          "Custom order should be provided in comma separated list with all section names:\n" \
                          "order=comments,settings,variables,testcases,variables\n"
        assert expected_output == result.output
