try:
    from robot.api.parsing import InlineIfHeader, TryHeader
except ImportError:
    InlineIfHeader, TryHeader = None, None

from robotidy.disablers import Skip, skip_if_disabled
from robotidy.transformers.aligners_core import AlignKeywordsTestsSection
from robotidy.utils import is_suite_templated


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
        skip_documentation: str = "True",  # noqa - override skip_documentation from Skip
        skip: Skip = None,
    ):
        super().__init__(widths, alignment_type, handle_too_long, skip)

    def visit_File(self, node):  # noqa
        if is_suite_templated(node):
            return node
        return self.generic_visit(node)

    @skip_if_disabled
    def visit_TestCase(self, node):  # noqa
        self.create_auto_widths_for_context(node)
        self.generic_visit(node)
        self.remove_auto_widths_for_context()
        return node

    def visit_Keyword(self, node):  # noqa
        return node
