import pytest

from .. import TransformerAcceptanceTest


class TestInlineIf(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "InlineIf"

    def test_transformer(self):
        self.compare(source="test.robot")

    def test_transformer_skip_else(self):
        self.compare(source="test.robot", expected="test_skip_else.robot", config=":skip_else=True:line_length=120")

    def test_invalid_if(self):
        self.compare(source="invalid_if.robot", not_modified=True)

    def test_invalid_inline_if(self):
        self.compare(source="invalid_inline_if.robot", not_modified=True, config=":line_length=120")

    def test_disablers(self):
        self.compare(source="test_disablers.robot")

    @pytest.mark.parametrize("indent", [2, 4])
    @pytest.mark.parametrize("spaces", [2, 4])
    def test_one_if_spacing(self, spaces, indent):
        self.compare(
            source="one_if.robot",
            expected=f"one_if_{spaces}spaces.robot",
            config=f" --spacecount {spaces} --indent {indent}",
        )
