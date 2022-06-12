from typing import Tuple

import pytest

from .. import TransformerAcceptanceTest


class TestAlignKeywordsSection(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "AlignKeywordsSection"

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

    # def test_invalid(self):
    #     self.compare(source="non_ascii_spaces.robot")

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
    @pytest.mark.parametrize("handle_too_long", ["align_to_next_col", "ignore_line"])
    @pytest.mark.parametrize("alignment_type", ["auto", "fixed"])
    def test_simple(self, alignment_type, handle_too_long, widths: Tuple):
        if widths == (4, 4, 4) and handle_too_long == "ignore_line":
            not_modified = True  # it will never fit, so all lines are ignored
        else:
            not_modified = False
        width_name = "_".join(str(width) for width in widths)
        if width_name == "0_0_0":
            width_name = "0"  # it should be the same result so we can reuse expected file
        width_csv = ",".join(str(width) for width in widths)
        expected = f"simple_{alignment_type}_{handle_too_long}_{width_name}.robot"
        config = f":alignment_type={alignment_type}:handle_too_long={handle_too_long}"
        config += f":widths={width_csv}"
        self.compare(source="simple.robot", expected=expected, config=config, not_modified=not_modified)

    def test_settings(self):
        self.compare(source="settings.robot")

    def test_examples(self):
        self.compare(source="example_cases.robot", config=":compact_overflow=True")

    def test_compact_overflow_first_line(self):
        self.compare(source="overflow_first_line.robot", config=":widths=24,28,20,20:compact_overflow=True")

    @pytest.mark.parametrize("alignment_type", ["fixed", "auto"])
    @pytest.mark.parametrize("doc_mode", ["skip", "align_first_col"])
    def test_documentation(self, doc_mode, alignment_type):
        self.compare(
            source="documentation.robot",
            expected=f"documentation_{alignment_type}_{doc_mode}.robot",
            config=f":documentation={doc_mode}:alignment_type={alignment_type}",
        )
