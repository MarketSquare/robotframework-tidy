from .. import TransformerAcceptanceTest


class TestAlignKeywordsSection(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "AlignKeywordsSection"

    def test_transformer(self):
        self.compare(source="test.robot", expected="test_20_26_42_space2_indent4.robot", config=":widths=20,26,30 --spacecount 2 --indent 4")

    def test_transformer_overflow_allowed(self):
        self.compare(source="test.robot", expected="test_20_26_42_space2_indent4.robot", config=":widths=20,26,30:overflow_allowed=True --spacecount 2 --indent 4")

    def test_blocks(self):
        self.compare(source="blocks.robot")

    def test_invalid(self):
        self.compare(source="non_ascii_spaces.robot")
