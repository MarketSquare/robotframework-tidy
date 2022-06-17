from collections import defaultdict

from robot.api.parsing import ElseHeader, ElseIfHeader, ModelVisitor, Token
from robot.parsing.model import Statement

try:
    from robot.api.parsing import InlineIfHeader, TryHeader
except ImportError:
    InlineIfHeader, TryHeader = None, None

from robotidy.disablers import skip_if_disabled
from robotidy.transformers import Transformer
from robotidy.transformers.aligners_core import AlignKeywordsTestsSection
from robotidy.utils import is_blank_multiline, round_to_four, tokens_by_lines


class AlignTestCasesSection(AlignKeywordsTestsSection):
    """
    Short description in one line.

    Long description with short example before/after.
    """

    def __init__(
        self,
        widths: str = "",
        alignment_type: str = "fixed",
        handle_too_long: str = "overflow",
        skip_documentation: bool = True,
        skip_return_values: bool = False,
        skip_keyword_call: str = "",
        skip_keyword_call_contains: str = "",
        skip_keyword_call_starts_with: str = "",
    ):
        super().__init__(
            widths,
            alignment_type,
            handle_too_long,
            skip_documentation,
            skip_return_values,
            skip_keyword_call,
            skip_keyword_call_contains,
            skip_keyword_call_starts_with,
        )

    @skip_if_disabled
    def visit_TestCase(self, node):
        self.create_auto_widths_for_context(node)
        self.generic_visit(node)
        self.remove_auto_widths_for_context()
        return node
