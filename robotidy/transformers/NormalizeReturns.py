from robot.api.parsing import ModelTransformer, ReturnStatement, Token, EmptyLine, Comment


class NormalizeReturns(ModelTransformer):
    """
    Short description in one line.

    Long description with short example before/after.

    See https://robotidy.readthedocs.io/en/latest/transformers/NormalizeReturns.html for more examples.
    """

    def __init__(self):
        self.return_statement = None

    def visit_Keyword(self, node):  # noqa
        self.return_statement = None
        node = self.generic_visit(node)
        if self.return_statement:
            skip_lines = []
            while node.body and isinstance(node.body[-1], (EmptyLine, Comment)):
                skip_lines.append(node.body.pop())
            return_stmt = ReturnStatement(
                [
                    Token(Token.SEPARATOR, self.formatting_config.separator),
                    Token(Token.RETURN_STATEMENT),
                    *self.return_statement.tokens[2:],
                ]
            )
            node.body.append(return_stmt)
            node.body.extend(skip_lines)
        return node

    def visit_KeywordCall(self, node):  # noqa
        if node.keyword and 'Return From' in node.keyword:
            print('s')
        return node

    def visit_Return(self, node):  # noqa
        if self.return_statement is None:
            self.return_statement = node
        return None

    def visit_Error(self, node):  # noqa
        for error in node.errors:
            if "Setting 'Return' is allowed only once" in error:
                return None
        return node
