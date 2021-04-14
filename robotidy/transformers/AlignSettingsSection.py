from collections import defaultdict

from robot.api.parsing import (
    ModelTransformer,
    Token
)
from robot.parsing.model import Statement

from robotidy.utils import node_outside_selection


class AlignSettingsSection(ModelTransformer):
    """
    Align lines in *** Settings *** section to columns.

    Following code::

        *** Settings ***
        Library      SeleniumLibrary
        Library   Mylibrary.py
        Variables  variables.py
        Test Timeout  1 min
            # this should be left aligned

    Will be transformed to::

        *** Settings ***
        Library         SeleniumLibrary
        Library         Mylibrary.py
        Variables       variables.py
        Test Timeout    1 min
        # this should be left aligned

    You can configure how many columns should be aligned to longest token in given column. The remaining columns
    will use fixed length separator length ``--space_count``. To only align first two columns::

       robotidy --transform AlignSettingsSection:up_to_column=2

    Supports global formatting params: ``--startline``, ``--endline`` and ``--space_count``
    (for columns with fixed length).
    """
    def __init__(self, up_to_column: int = 0):
        self.up_to_column = up_to_column - 1

    def visit_SettingSection(self, node):  # noqa
        if node_outside_selection(node, self.formatting_config):
            return node
        statements = []
        for child in node.body:
            if child.type == Token.EOL or node_outside_selection(child, self.formatting_config):
                statements.append(child)
            elif child.type == Token.COMMENT:
                statements.append(self.left_align(child))
            else:
                statements.append(list(self.tokens_by_lines(child)))
        nodes_to_be_aligned = [st for st in statements if isinstance(st, list)]
        if not nodes_to_be_aligned:
            return node
        look_up = self.create_look_up(nodes_to_be_aligned, self.up_to_column)  # for every col find longest value
        node.body = self.align_rows(statements, look_up, self.up_to_column)
        return node

    def align_rows(self, statements, look_up, up_to_column=-1):
        aligned_statements = []
        for st in statements:
            if not isinstance(st, list):
                aligned_statements.append(st)
                continue
            aligned_statement = []
            for line in st:
                up_to = up_to_column if up_to_column != -1 else len(line) - 2
                for index, token in enumerate(line[:-2]):
                    aligned_statement.append(token)
                    separator = (look_up[index] - len(token.value) + 4) * ' ' if index < up_to else \
                        self.formatting_config.space_count * ' '
                    aligned_statement.append(Token(Token.SEPARATOR, separator))
                last_token = line[-2]
                # remove leading whitespace before token
                last_token.value = last_token.value.strip() if last_token.value else last_token.value
                aligned_statement.append(last_token)
                aligned_statement.append(line[-1])  # eol
            aligned_statements.append(Statement.from_tokens(aligned_statement))
        return aligned_statements

    def tokens_by_lines(self, node):
        for index, line in enumerate(node.lines):
            if line:
                if line[0].type == Token.VARIABLE and not line[0].value:
                    # if variable is prefixed with spaces
                    line = line[1:]
                elif line[0].type == Token.ARGUMENT:
                    line[0].value = line[0].value.strip() if line[0].value else line[0].value
            yield [token for token in line if token.type not in ('SEPARATOR', 'EOS')]

    @staticmethod
    def left_align(node):
        """ remove leading separator token """
        tokens = list(node.tokens)
        while tokens and tokens[0].type == Token.SEPARATOR:
            tokens.pop(0)
        return Statement.from_tokens(tokens)

    @staticmethod
    def create_look_up(statements, up_to_column=-1):
        look_up = defaultdict(int)
        for st in statements:
            for line in st:
                up_to = up_to_column if up_to_column != -1 else len(line)
                for index, token in enumerate(line[:up_to]):
                    look_up[index] = max(look_up[index], len(token.value))
        return {index: AlignSettingsSection.round_to_four(length) for index, length in look_up.items()}

    @staticmethod
    def round_to_four(number):
        div = number % 4
        if div:
            return number + 4 - div
        return number
