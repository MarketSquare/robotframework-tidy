from itertools import takewhile

from robot.api.parsing import (
    ModelTransformer,
    Token
)

from robotidy.decorators import check_start_end_line


class NormalizeSeparators(ModelTransformer):
    """
    Normalize separators and indents.

    All separators (pipes included) are converted to fixed length of 4 spaces (configurable via global argument
    ``--spacecount``).

    Supports global formatting params: ``--startline`` and ``--endline``.
    """
    def __init__(self):
        self.indent = 0

    def visit_File(self, node):  # noqa
        self.indent = 0
        return self.generic_visit(node)

    def visit_TestCase(self, node):  # noqa
        self.visit_Statement(node.header)
        self.indent += 1
        node.body = [self.visit(item) for item in node.body]
        self.indent -= 1
        return node

    def visit_Keyword(self, node):  # noqa
        self.visit_Statement(node.header)
        self.indent += 1
        node.body = [self.visit(item) for item in node.body]
        self.indent -= 1
        return node

    def visit_For(self, node):
        self.visit_Statement(node.header)
        self.indent += 1
        node.body = [self.visit(item) for item in node.body]
        self.indent -= 1
        self.visit_Statement(node.end)
        return node

    def visit_If(self, node):
        self.visit_Statement(node.header)
        self.indent += 1
        node.body = [self.visit(item) for item in node.body]
        self.indent -= 1
        if node.orelse:
            self.visit(node.orelse)
        if node.end:
            self.visit_Statement(node.end)
        return node

    @check_start_end_line
    def visit_Statement(self, statement):  # noqa
        has_pipes = statement.tokens[0].value.startswith('|')
        return self._handle_spaces(statement, has_pipes)

    def _handle_spaces(self, statement, has_pipes):
        new_tokens = []
        for line in statement.lines:
            if has_pipes and len(line) > 1:
                line = self._remove_consecutive_separators(line)
            new_tokens.extend([self._normalize_spaces(i, t, len(line))
                               for i, t in enumerate(line)])
        statement.tokens = new_tokens
        self.generic_visit(statement)
        return statement

    @staticmethod
    def _remove_consecutive_separators(line):
        sep_count = len(list(
            takewhile(lambda t: t.type == Token.SEPARATOR, line)
        ))
        return line[sep_count - 1:]

    def _normalize_spaces(self, index, token, line_length):
        if token.type == Token.SEPARATOR:
            spaces = self.formatting_config.space_count * self.indent \
                if index == 0 else self.formatting_config.space_count
            token.value = ' ' * spaces
        # remove trailing whitespace from last token
        if index == line_length - 2:
            token.value = token.value.rstrip()
        return token
