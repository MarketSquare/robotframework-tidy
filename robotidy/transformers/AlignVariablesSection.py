from collections import defaultdict

from robot.api.parsing import ModelTransformer, Token
from robot.parsing.model import Statement

from robotidy.utils import node_outside_selection, round_to_four, tokens_by_lines, left_align, is_blank_multiline


class AlignVariablesSection(ModelTransformer):
    """
    Align variables in *** Variables *** section to columns.

    Following code:

        *** Variables ***
        ${VAR}  1
        ${LONGER_NAME}  2
        &{MULTILINE}  a=b
        ...  b=c

    will be transformed to:

        *** Variables ***
        ${VAR}          1
        ${LONGER_NAME}  2
        &{MULTILINE}    a=b
        ...             b=c

    You can configure how many columns should be aligned to longest token in given column. The remaining columns
    will use fixed length separator length ``--space_count``. By default only first two columns are aligned.
    To align first three columns:

       robotidy --transform AlignVariablesSection:up_to_column=3

    To align all columns set ``up_to_column`` to 0.

    Supports global formatting params: ``--startline`` and ``--endline``.

    See https://robotidy.readthedocs.io/en/latest/transformers/AlignVariablesSection.html for more examples.
    """

    def __init__(self, up_to_column: int = 2):
        self.up_to_column = up_to_column - 1

    def visit_VariableSection(self, node):  # noqa
        if node_outside_selection(node, self.formatting_config):
            return node
        statements = []
        for child in node.body:
            if node_outside_selection(child, self.formatting_config):
                statements.append(child)
            elif child.type in (Token.EOL, Token.COMMENT):
                statements.append(left_align(child))
            else:
                statements.append(list(tokens_by_lines(child)))
        nodes_to_be_aligned = [st for st in statements if isinstance(st, list)]
        if not nodes_to_be_aligned:
            return node
        look_up = self.create_look_up(nodes_to_be_aligned)  # for every col find longest value
        node.body = self.align_rows(statements, look_up)
        return node

    def align_rows(self, statements, look_up):
        aligned_statements = []
        for st in statements:
            if not isinstance(st, list):
                aligned_statements.append(st)
                continue
            aligned_statement = []
            for line in st:
                if is_blank_multiline(line):
                    line[-1].value = line[-1].value.lstrip(" \t")  # normalize eol from '  \n' to '\n'
                    aligned_statement.extend(line)
                    continue
                up_to = self.up_to_column if self.up_to_column != -1 else len(line) - 2
                for index, token in enumerate(line[:-2]):
                    aligned_statement.append(token)
                    separator = (
                        (look_up[index] - len(token.value) + 4) * " "
                        if index < up_to
                        else self.formatting_config.space_count * " "
                    )
                    aligned_statement.append(Token(Token.SEPARATOR, separator))
                last_token = line[-2]
                # remove leading whitespace before token
                last_token.value = last_token.value.strip() if last_token.value else last_token.value
                aligned_statement.append(last_token)
                aligned_statement.append(line[-1])  # eol
            aligned_statements.append(Statement.from_tokens(aligned_statement))
        return aligned_statements

    def create_look_up(self, statements):
        look_up = defaultdict(int)
        for st in statements:
            for line in st:
                up_to = self.up_to_column if self.up_to_column != -1 else len(line)
                for index, token in enumerate(line[:up_to]):
                    look_up[index] = max(look_up[index], len(token.value))
        return {index: round_to_four(length) for index, length in look_up.items()}
