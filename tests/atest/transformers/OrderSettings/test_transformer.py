import pytest

from .. import TransformerAcceptanceTest


class TestOrderSettings(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "OrderSettings"

    def test_order(self):
        self.compare(source="test.robot")

    @pytest.mark.parametrize(
        "keyword_before, keyword_after, test_before, test_after, expected",
        [
            (
                "documentation,tags,timeout,arguments",
                "teardown,return",
                "documentation,tags,template,timeout,setup",
                "teardown",
                "custom_order_default.robot",
            ),
            (
                "",
                "documentation,tags,timeout,arguments,teardown,return",
                "",
                "documentation,tags,template,timeout,setup,teardown",
                "custom_order_all_end.robot",
            ),
            (None, None, None, "", "custom_order_without_test_teardown.robot"),
        ],
    )
    def test_custom_order(self, keyword_before, keyword_after, test_before, test_after, expected):
        config = ""
        if keyword_before is not None:
            config += f":keyword_before={keyword_before}"
        if keyword_after is not None:
            config += f":keyword_after={keyword_after}"
        if test_before is not None:
            config += f":test_before={test_before}"
        if test_after is not None:
            config += f":test_after={test_after}"
        self.compare(source="test.robot", expected=expected, config=config)

    def test_custom_order_invalid_param(self):
        result = self.run_tidy(
            args=f"--transform {self.TRANSFORMER_NAME}:keyword_before=documentation:keyword_after=tags,invalid".split(),
            source="test.robot",
            exit_code=1,
        )
        expected_output = (
            f"Error: {self.TRANSFORMER_NAME}: Invalid 'order' parameter value: 'tags,invalid'."
            f" Custom order should be provided in comma separated list with valid setting names:\n"
            f"['arguments', 'documentation', 'return', 'tags', 'teardown', 'timeout']\n"
        )
        assert expected_output == result.output
