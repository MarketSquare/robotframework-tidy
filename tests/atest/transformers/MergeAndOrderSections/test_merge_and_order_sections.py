import pytest

from .. import TransformerAcceptanceTest


class TestMergeAndOrderSections(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "MergeAndOrderSections"

    def test_merging_and_ordering(self):
        self.compare(source="tests.robot")

    def test_both_test_and_task(self):
        self.compare(source="both_test_and_task.robot")

    def test_multiple_header_comments(self):
        self.compare(source="multiple_header_comments.robot")

    def test_nested_blocks(self):
        self.compare(source="nested_blocks.robot")

    def test_nested_block_for(self):
        self.compare(source="nested_block_for.robot")

    def test_empty_section(self):
        self.compare(source="empty_section.robot")

    def test_parsing_error(self):
        self.compare(source="parsing_error.robot", not_modified=True)

    def test_too_few_calls_in_keyword(self):
        self.compare(source="too_few_calls_in_keyword.robot")

    def test_default_order(self):
        self.compare(source="order.robot", not_modified=True)

    def test_custom_order(self):
        self.compare(
            source="order.robot",
            expected="order_settings_comments_keywords_variables_testcases.robot",
            config=":order=settings,comments,keyword,variables,testcases",
        )

    def test_do_not_create_comment_section(self):
        self.compare(
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
        result = self.run_tidy(
            args=f"--transform {self.TRANSFORMER_NAME}:order={parameter}".split(),
            source="order.robot",
            exit_code=1,
        )
        expected_output = (
            f"Error: {self.TRANSFORMER_NAME}: Invalid 'order' parameter value: '{parameter}'. "
            "Custom order should be provided in comma separated list with all section names:\n"
            "order=comments,settings,variables,testcases,variables\n"
        )
        assert expected_output == result.output

    def test_inline_if(self):
        self.compare(source="inline_if.robot", not_modified=True)

    def test_disablers(self):
        self.compare(source="disablers.robot")

    def test_translated(self):
        self.compare(source="translated.robot", target_version=6)
