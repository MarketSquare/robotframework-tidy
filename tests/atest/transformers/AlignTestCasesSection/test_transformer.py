from typing import Tuple

import pytest

from .. import TransformerAcceptanceTest


class TestAlignTestCasesSection(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "AlignTestCasesSection"

    def test_blocks(self):
        self.compare(source="blocks.robot")

    def test_blocks_auto(self):
        self.compare(source="blocks.robot", expected="blocks_auto.robot", config=":alignment_type=auto")

    def test_blocks_auto_with_0(self):
        self.compare(source="blocks.robot", expected="blocks_auto_0.robot", config=":alignment_type=auto:widths=0")

    def test_blocks_rf5(self):
        self.compare(source="blocks_rf5.robot", target_version=5)

    def test_one_column(self):
        self.compare(source="one_column.robot")

    def test_invalid(self):
        self.compare(source="non_ascii_spaces.robot", target_version=5)

    @pytest.mark.parametrize(
        "widths",
        [
            (0,),
            (0, 0, 0),
            (24, 24, 24),
            (24, 40, 24),
            (24, 0, 24),
            (4, 4, 4),
        ],
    )
    @pytest.mark.parametrize("handle_too_long", ["overflow", "ignore_line", "ignore_rest"])
    @pytest.mark.parametrize("alignment_type", ["auto", "fixed"])
    def test_simple(self, alignment_type, handle_too_long, widths: Tuple):
        width_name = "_".join(str(width) for width in widths)
        if width_name == "0_0_0":
            width_name = "0"  # it should be the same result so we can reuse expected file
        width_csv = ",".join(str(width) for width in widths)
        expected = f"simple_{alignment_type}_{handle_too_long}_{width_name}.robot"
        config = f":alignment_type={alignment_type}:handle_too_long={handle_too_long}"
        config += f":widths={width_csv}"
        self.compare(source="simple.robot", expected=expected, config=config)

    def test_settings(self):
        self.compare(source="settings.robot")

    def test_compact_overflow_first_line(self):
        self.compare(source="overflow_first_line.robot", config=":widths=24,28,20,20:handle_too_long=compact_overflow")

    @pytest.mark.parametrize("alignment_type", ["fixed", "auto"])
    @pytest.mark.parametrize("skip_doc", [True, False])
    def test_documentation(self, skip_doc, alignment_type):
        doc_formatting = "skip" if skip_doc else "align_first_col"
        self.compare(
            source="documentation.robot",
            expected=f"documentation_{alignment_type}_{doc_formatting}.robot",
            config=f":skip_documentation={skip_doc}:alignment_type={alignment_type}",
        )

    def test_skip_keyword_name(self):
        self.compare(
            "skip_keywords.robot",
            config=":skip_keyword_call=should_not_be_none"
            ":skip_keyword_call_pattern=Contain,^(?i)prefix"
            ":skip_return_values=True"
            ":widths=24,24,24,28",
        )

    @pytest.mark.parametrize("handle_too_long", ["overflow", "compact_overflow", "ignore_line", "ignore_rest"])
    def test_auto_overflow_token_should_not_be_counted(self, handle_too_long):
        expected = f"too_long_token_counter_{handle_too_long}.robot"
        self.compare(
            "too_long_token_counter.robot",
            expected=expected,
            config=f":alignment_type=auto:handle_too_long={handle_too_long}",
        )

    def test_compact_overflow_last_0(self):
        self.compare(source="compact_overflow_last_0.robot", config=":widths=4,0")

    def test_templated(self):
        self.compare(source="templated.robot", not_modified=True)
