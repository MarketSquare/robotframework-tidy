import pytest

from .. import TransformerAcceptanceTest


class TestAlignTestCases(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "AlignTestCases"

    @pytest.mark.parametrize(
        "source",
        [
            "test.robot",
            "no_header_col.robot",
            "for_loops.robot",
            "with_settings.robot",
            "templated_for_loops.robot",
            "templated_for_loops_and_without.robot",
            "templated_for_loops_header_cols.robot",
            "empty_line.robot",
        ],
    )
    def test_transformer(self, source):
        self.compare(source=source, expected=source)

    def test_only_with_headers(self):
        self.compare(
            source="no_header_col.robot",
            expected="no_header_col_only_headers.robot",
            config=":only_with_headers=True",
        )

    def test_fixed(self):
        self.compare(source="test.robot", expected="test_fixed.robot", config=":min_width=30")

    def test_for_fixed(self):
        self.compare(
            source="templated_for_loops_and_without.robot",
            expected="templated_for_loops_and_without_fixed.robot",
            config=":min_width=25",
        )
