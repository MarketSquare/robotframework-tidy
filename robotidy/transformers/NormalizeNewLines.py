from typing import Optional
import ast

from robot.api.parsing import (
    ModelTransformer,
    EmptyLine
)


class NormalizeNewLines(ModelTransformer):
    """
    Normalize new lines.

    Ensure that there is exactly:
    * ``section_lines = 1`` empty lines between sections,
    * ``test_case_lines = 1`` empty lines between test cases,
    * ``keyword_lines = test_case_lines`` empty lines between keywords.
    Removes empty lines after section (and before any data) and appends 1 empty line at the end of file.

    If the suite contains Test Template tests will not be separated by empty lines unless ``separate_templated_tests``
    is set to True.
    """
    def __init__(self, test_case_lines: int = 1, keyword_lines: Optional[int] = None, section_lines: int = 1,
                 separate_templated_tests: bool = False):
        self.test_case_lines = test_case_lines
        self.keyword_lines = keyword_lines if keyword_lines is not None else test_case_lines
        self.section_lines = section_lines
        self.separate_templated_tests = separate_templated_tests
        self.last_section = None
        self.last_test = None
        self.last_keyword = None
        self.templated = False

    def visit_File(self, node):  # noqa
        self.templated = not self.separate_templated_tests and self.is_templated(node)
        self.last_section = node.sections[-1] if node.sections else None
        return self.generic_visit(node)

    def visit_Section(self, node):  # noqa
        self.trim_leading_empty_lines(node)
        self.trim_trailing_empty_lines(node)
        empty_line = EmptyLine.from_params()
        if node is self.last_section:
            node.body.append(empty_line)
            return self.generic_visit(node)
        node.body.extend([empty_line] * self.section_lines)
        return self.generic_visit(node)

    def visit_TestCaseSection(self, node):  # noqa
        self.last_test = node.body[-1] if node.body else None
        return self.visit_Section(node)

    def visit_KeywordSection(self, node):  # noqa
        self.last_keyword = node.body[-1] if node.body else None
        return self.visit_Section(node)

    def visit_TestCase(self, node):  # noqa
        self.trim_leading_empty_lines(node)
        self.trim_trailing_empty_lines(node)
        if node is self.last_test:
            return node
        if not self.templated:
            node.body.extend([EmptyLine.from_params()] * self.test_case_lines)
        return node

    def visit_Keyword(self, node):  # noqa
        self.trim_leading_empty_lines(node)
        self.trim_trailing_empty_lines(node)
        if node is self.last_keyword:
            return node
        node.body.extend([EmptyLine.from_params()] * self.keyword_lines)
        return node

    @staticmethod
    def trim_trailing_empty_lines(node):
        while hasattr(node, 'body') and node.body and isinstance(node.body[-1], EmptyLine):
            node.body.pop()

    @staticmethod
    def trim_leading_empty_lines(node):
        while node.body and isinstance(node.body[0], EmptyLine):
            node.body.pop(0)

    @staticmethod
    def is_templated(node):
        template_finder = TestTemplateFinder()
        template_finder.visit(node)
        return template_finder.templated


class TestTemplateFinder(ast.NodeVisitor):
    def __init__(self):
        self.templated = False

    def visit_TestTemplate(self, node):  # noqa
        if node.value:
            self.templated = True
