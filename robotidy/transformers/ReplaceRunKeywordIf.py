from robot.api.parsing import (
    Token,
    ModelTransformer,
    End,
    If,
    IfHeader,
    ElseHeader,
    ElseIfHeader,
    KeywordCall
)
from robotidy.utils import normalize_name
from robotidy.decorators import check_start_end_line


def insert_separators(indent, tokens, space_count):
    yield Token(Token.SEPARATOR, indent + space_count * ' ')
    for token in tokens[:-1]:
        yield token
        yield Token(Token.SEPARATOR, space_count * ' ')
    yield tokens[-1]
    yield Token(Token.EOL)


class ReplaceRunKeywordIf(ModelTransformer):
    """
    Replace ``Run Keyword If`` keyword calls with IF END blocks.
    Supports global formatting params: ``--spacecount``, ``--startline`` and ``--endline``.

    Following code::

        Run Keyword If  ${condition}
        ...  Keyword  ${arg}
        ...  ELSE IF  ${condition2}  Keyword2
        ...  ELSE  Keyword3

    Will be transformed to::

        IF    ${condition}
            Keyword    ${arg}
        ELSE IF    ${condition2}
            Keyword2
        ELSE
            Keyword3
        END

    Any return value will be applied to every ELSE/ELSE IF branch::

        ${var}  Run Keyword If  ${condition}  Keyword  ELSE  Keyword2

    Output::

        IF    ${condition}
            ${var}    Keyword
        ELSE
            ${var}    Keyword2
        END

    Run Keywords inside Run Keyword If will be splitted into separate keywords::

       Run Keyword If  ${condition}  Run Keywords  Keyword  ${arg}  AND  Keyword2

    Output::

        IF    ${condition}
            Keyword    ${arg}
            Keyword2
        END

    """
    @check_start_end_line
    def visit_KeywordCall(self, node):  # noqa
        if not node.keyword:
            return node
        if normalize_name(node.keyword) == 'runkeywordif':
            return self.create_branched(node)
        return node

    def create_branched(self, node):
        separator = node.tokens[0]
        assign = node.get_tokens(Token.ASSIGN)
        raw_args = node.get_tokens(Token.ARGUMENT)
        if len(raw_args) < 2:
            return node
        end = End([
            separator,
            Token(Token.END),
            Token(Token.EOL)
        ])
        prev_if = None
        for branch in reversed(list(self.split_args_on_delimeters(raw_args, ('ELSE', 'ELSE IF')))):
            if branch[0].value == 'ELSE':
                header = ElseHeader([
                    separator,
                    Token(Token.ELSE),
                    Token(Token.EOL)
                ])
                if len(branch) < 2:
                    return node
                args = branch[1:]
            elif branch[0].value == 'ELSE IF':
                if len(branch) < 3:
                    return node
                header = ElseIfHeader([
                    separator,
                    Token(Token.ELSE_IF),
                    Token(Token.SEPARATOR, self.formatting_config.space_count * ' '),
                    branch[1],
                    Token(Token.EOL)
                ])
                args = branch[2:]
            else:
                if len(branch) < 2:
                    return node
                header = IfHeader([
                    separator,
                    Token(Token.IF),
                    Token(Token.SEPARATOR, self.formatting_config.space_count * ' '),
                    branch[0],
                    Token(Token.EOL)
                ])
                args = branch[1:]
            keywords = self.create_keywords(args, assign, separator.value)
            if_block = If(header=header, body=keywords, orelse=prev_if)
            prev_if = if_block
        prev_if.end = end
        return prev_if

    def create_keywords(self, arg_tokens, assign, indent):
        if normalize_name(arg_tokens[0].value) == 'runkeywords':
            return [self.args_to_keyword(keyword[1:], assign, indent)
                    for keyword in self.split_args_on_delimeters(arg_tokens, ('AND',))]
        return self.args_to_keyword(arg_tokens, assign, indent)

    def args_to_keyword(self, arg_tokens, assign, indent):
        separated_tokens = list(insert_separators(
            indent,
            [*assign, Token(Token.KEYWORD, arg_tokens[0].value), *arg_tokens[1:]],
            self.formatting_config.space_count
        ))
        return KeywordCall.from_tokens(separated_tokens)

    @staticmethod
    def split_args_on_delimeters(args, delimeters):
        split_points = [index for index, arg in enumerate(args) if arg.value in delimeters]
        prev_index = 0
        for split_point in split_points:
            yield args[prev_index:split_point]
            prev_index = split_point
        yield args[prev_index:len(args)]
