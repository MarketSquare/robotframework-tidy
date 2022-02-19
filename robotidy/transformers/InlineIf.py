from itertools import chain

from robot.api.parsing import ModelTransformer, If, IfHeader, ElseHeader, ElseIfHeader, Token, KeywordCall

try:
    from robot.api.parsing import ReturnStatement, Break, Continue, InlineIfHeader
except ImportError:
    ReturnStatement, Break, Continue, InlineIfHeader = None, None, None, None

from robotidy.utils import ROBOT_VERSION, normalize_name
from robotidy.decorators import check_start_end_line


class InlineIf(ModelTransformer):
    """
    Replaces IF blocks with inline IF.

    It will only replace IF block if it can fit in one line shorter than ``line_length`` parameter and return
    variables matches for all ELSE and ELSE IF branches.

    Following code::

        *** Test Cases ***
        Test
            IF    $condition1
                Keyword    argument
            END
            IF    $condition2
                ${var}  Keyword
            ELSE
                ${var}  Keyword 2
            END
            IF    $condition1
                Keyword    argument
                Keyword 2
            END

    will be transformed to:

        *** Test Cases ***
        Test
            IF    $condition1    Keyword    argument
            ${var}    IF    $condition2    Keyword    ELSE    Keyword 2
            IF    $condition1
                Keyword    argument
                Keyword 2
            END

    You can decide to not replace IF blocks containing ELSE or ELSE IF branches by setting ``skip_else`` to True.

    Supports global formatting params: ``--startline`` and ``--endline``.

    See https://robotidy.readthedocs.io/en/latest/transformers/InlineIf.html for more examples.
    """

    ENABLED = ROBOT_VERSION.major >= 5

    def __init__(self, line_length: int = None, skip_else: bool = False):
        self._line_length = line_length
        self.skip_else = skip_else

    @property
    def line_length(self):
        return self.formatting_config.line_length if self._line_length is None else self._line_length

    def visit_TestCase(self, node):  # noqa
        self.generic_visit(node)
        return node

    visit_Keyword = visit_TestCase

    @check_start_end_line
    def visit_If(self, node: If):  # noqa
        if node.errors or self.is_inline_end(node.end) or node.end.errors:  # already inline if (or error)
            return node
        self.generic_visit(node)
        if node.orelse:
            self.generic_visit(node.orelse)
        indent = node.header.tokens[0]
        if not (self.should_transform(node) and self.assignment_identical(node)):
            return node
        return self.to_inline(node, indent.value)

    def should_transform(self, node):
        if node.header.errors:
            return False
        if (
            len(node.body) > 1
            or not node.body
            or not isinstance(node.body[0], (KeywordCall, ReturnStatement, Break, Continue))
        ):
            return False
        if node.orelse:
            return self.should_transform(node.orelse)
        return True

    @staticmethod
    def if_to_branches(if_block):
        yield if_block
        or_else = if_block.orelse
        while or_else:
            yield or_else
            or_else = or_else.orelse

    def assignment_identical(self, node):
        else_found = False
        assigned = []
        for branch in self.if_to_branches(node):
            if isinstance(branch.header, ElseHeader):
                else_found = True
            if not isinstance(branch.body[0], KeywordCall) or not branch.body[0].assign:
                assigned.append([])
            else:
                assigned.append([normalize_name(assign).replace("=", "") for assign in branch.body[0].assign])
            if len(assigned) > 1 and assigned[-1] != assigned[-2]:
                return False
        if any(x for x in assigned):
            return else_found
        return True

    def is_shorter_than_limit(self, inline_if):
        line_len = self.if_len(inline_if)
        or_else = inline_if.orelse
        while or_else:
            line_len += self.if_len(or_else)
            or_else = or_else.orelse
        return line_len <= self.line_length

    @staticmethod
    def is_inline_end(end):
        if not end:
            return True
        if not len(end.tokens) == 1:
            return False
        return not end.tokens[0].value

    @staticmethod
    def if_len(if_st):
        return sum(
            len(tok.value)
            for tok in chain(if_st.body[0].tokens if if_st.body else [], if_st.header.tokens)
            if tok.value != "\n"
        )

    def to_inline(self, node, indent):
        tail = node
        if_block = if_block_tail = self.inline_if_from_branch(node, indent)
        while tail.orelse:
            if self.skip_else:
                return node
            if_block_tail.orelse = self.inline_if_from_branch(tail.orelse, self.formatting_config.separator)
            tail = tail.orelse
            if_block_tail = if_block_tail.orelse
        if self.is_shorter_than_limit(if_block):
            return if_block
        return node

    def inline_if_from_branch(self, node, indent):
        if not node:
            return None
        separator = self.formatting_config.separator
        last_token = Token(Token.EOL) if node.orelse is None else Token(Token.SEPARATOR, separator)
        assigned = None

        if isinstance(node.body[0], KeywordCall):
            assigned = node.body[0].assign
            keyword = self.to_inline_keyword(node.body[0], separator, last_token)
        elif isinstance(node.body[0], ReturnStatement):
            keyword = self.to_inline_return(node.body[0], separator, last_token)
        elif isinstance(node.body[0], Break):
            keyword = Break(self.to_inline_break_continue_tokens(Token.BREAK, separator, last_token))
        elif isinstance(node.body[0], Continue):
            keyword = Continue(self.to_inline_break_continue_tokens(Token.CONTINUE, separator, last_token))
        else:
            return node

        # check for ElseIfHeader first since it's child of IfHeader class
        if isinstance(node.header, ElseIfHeader):
            header = ElseIfHeader(
                [Token(Token.ELSE_IF), Token(Token.SEPARATOR, separator), Token(Token.ARGUMENT, node.header.condition)]
            )
        elif isinstance(node.header, IfHeader):
            tokens = [Token(Token.SEPARATOR, indent)]
            if assigned:
                for assign in assigned:
                    tokens.extend([Token(Token.ASSIGN, assign), Token(Token.SEPARATOR, separator)])
            tokens.extend(
                [
                    Token(Token.INLINE_IF),
                    Token(Token.SEPARATOR, separator),
                    Token(Token.ARGUMENT, node.header.condition),
                ]
            )
            header = InlineIfHeader(tokens)
        elif isinstance(node.header, ElseHeader):
            header = ElseHeader([Token(Token.ELSE)])
        else:
            return node
        return If(header=header, body=[keyword])

    @staticmethod
    def to_inline_keyword(keyword, separator, last_token):
        tokens = [Token(Token.SEPARATOR, separator), Token(Token.KEYWORD, keyword.keyword)]
        for arg in keyword.get_tokens(Token.ARGUMENT):
            tokens.extend([Token(Token.SEPARATOR, separator), arg])
        tokens.append(last_token)
        return KeywordCall(tokens)

    @staticmethod
    def to_inline_return(node, separator, last_token):
        tokens = [Token(Token.SEPARATOR, separator), Token(Token.RETURN_STATEMENT)]
        for value in node.values:
            tokens.extend([Token(Token.SEPARATOR, separator), Token(Token.ARGUMENT, value)])
        tokens.append(last_token)
        return ReturnStatement(tokens)

    @staticmethod
    def to_inline_break_continue_tokens(token, separator, last_token):
        return [Token(Token.SEPARATOR, separator), Token(token), last_token]
