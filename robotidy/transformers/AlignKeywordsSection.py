from collections import defaultdict

from robot.api.parsing import ModelTransformer, ModelVisitor, Token, EmptyLine, Comment
from robot.parsing.model import Statement

from robotidy.disablers import skip_if_disabled
from robotidy.utils import tokens_by_lines, round_to_four, is_blank_multiline


class AlignKeywordsSection(ModelTransformer):
    """
    Short description in one line.

    Long description with short example before/after.

    See https://robotidy.readthedocs.io/en/latest/transformers/AlignKeywordsSection.html for more examples.
    """
    ENABLED = False
    DEFAULT_WIDTH = 24

    def __init__(self, widths: str = "", overflow_allowed: bool = True):
        self.indent = 1
        self.overflow_allowed = overflow_allowed
        # column widths map - 0: 40, 1: 30
        if widths:
            self.widths = {index: int(width) for index, width in enumerate(widths.split(","))}  # TODO type check
        else:
            self.widths = None

    def visit_If(self, node):  # noqa
        self.indent += 1
        self.generic_visit(node)
        self.indent -= 1
        return node

    visit_Else = visit_ElseIf = visit_For = visit_If

    def get_width(self, col):
        if not self.widths:
            return self.DEFAULT_WIDTH
        if col in self.widths:
            return self.widths[col]
        return self.widths[len(self.widths) - 1]  # last element

    @skip_if_disabled
    def visit_Keyword(self, node):  # noqa
        # counter = ColumnWidthCounter(self.disablers)
        # # counter.visit(node)
        # # self.widths = counter.widths
        # # statements = []
        # # for child in node.body:
        # #     if self.disablers.is_node_disabled(child) or isinstance(child, (EmptyLine, Comment)):
        # #         statements.append(child)
        # #     else:
        # #         statements.append(list(tokens_by_lines(child)))
        # widths = counter.collect_widths(node)
        return self.generic_visit(node)

    def visit_ForHeader(self, node):  # noqa
        # Fix indent for FOR, IF, WHILE, TRY block headers & ends
        indent = Token(Token.SEPARATOR, (self.indent - 1) * self.formatting_config.indent)
        node.tokens = [indent] + list(node.tokens[1:])
        return node

    visit_End = visit_ForHeader  # TOOD add other headers

    @skip_if_disabled
    def visit_KeywordCall(self, node):  # noqa
        lines = list(tokens_by_lines(node))
        indent = Token(Token.SEPARATOR, self.indent * self.formatting_config.indent)
        aligned_statement = []
        for line in lines:
            if is_blank_multiline(line):
                line[-1].value = line[-1].value.lstrip(" \t")  # normalize eol from '  \n' to '\n'
                aligned_statement.extend(line)
                continue
            aligned_statement.append(indent)
            column = 0
            # FIXME if line has only one element, just fix indent and go on
            if len(line) < 2:
                return node
            for token in line[:-2]:
                aligned_statement.append(token)
                width = self.get_width(column)
                # TODO rework overflow - we are not interested in aligning to next column, just any next witch matching alignment
                separator_len = width - len(token.value)  # TODO round to 4 for auto
                if separator_len < self.formatting_config.space_count:
                    if not self.overflow_allowed:
                        return node  # TODO overflow logic
                    # (len(token) + separator) - width
                    while (len(token.value) + self.formatting_config.space_count) > width:
                        column += 1
                        width += self.get_width(column)
                    separator_len = width - len(token.value)
                aligned_statement.append(Token(Token.SEPARATOR, separator_len * " "))
                column += 1
            last_token = line[-2]
            # remove leading whitespace before token
            last_token.value = last_token.value.strip() if last_token.value else last_token.value
            aligned_statement.append(last_token)
            aligned_statement.append(line[-1])  # eol

        return Statement.from_tokens(aligned_statement)


class ColumnWidthCounter(ModelVisitor):
    def __init__(self, disablers):
        # column width should be min from (longest_token shorter than 30, 30)
        # longest_token should be chosen first (
        self.max_width = 40
        self.disablers = disablers

    def collect_widths(self, node):
        lines = []
        for child in node.body:
            if self.disablers.is_node_disabled(child) or isinstance(child, (EmptyLine, Comment)):
                continue
            else:
                lines.append(list(tokens_by_lines(child)))
                # statements.append(list(tokens_by_lines(child)))
        widths = self.create_look_up(lines)
        return widths

    def create_look_up(self, statements):
        look_up = defaultdict(int)
        for st in statements:
            for line in st:
                for index, token in enumerate(line):
                    if len(token.value) > self.max_width:
                        continue
                    look_up[index] = max(look_up[index], len(token.value))
                    # look_up[index] = min(look_up[index], self.max_width)
        return {index: round_to_four(length) for index, length in look_up.items()}

    # @skip_if_disabled
    # def visit_Statement(self, statement):  # noqa
    #     if statement.type == Token.COMMENT:
    #         return

# maybe IFs, WHILEs, TRYs, FORs should be aligned separately?
