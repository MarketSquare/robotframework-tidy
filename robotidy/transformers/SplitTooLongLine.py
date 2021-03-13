from robot.api.parsing import (
    ModelTransformer,
    Token
)


EOL = Token(Token.EOL)
CONTINUATION = Token(Token.CONTINUATION)


class SplitTooLongLine(ModelTransformer):
    def __init__(self, line_length: int = 120, split_on_every_arg: bool = False):
        super().__init__()
        self.line_length = line_length
        self.split_on_every_arg = split_on_every_arg

    def visit_KeywordCall(self, node):  # noqa
        if all(line[-1].end_col_offset < self.line_length for line in node.lines):
            return node
        return self.split_keyword_call(node)

    def split_keyword_call(self, node):
        separator = Token(Token.SEPARATOR, self.formatting_config.space_count * ' ')
        indent = node.tokens[0]

        assignment = node.get_token(Token.ASSIGN)
        keyword = node.get_token(Token.KEYWORD)

        if assignment:
            head = [indent, assignment, separator, keyword]
        else:
            head = [indent, keyword]

        comments, tail, line = [], [], []

        # Comments with separators inside them are split into
        # [COMMENT, SEPARATOR, COMMENT] tokens in the AST, so in order to preserve the
        # original comment, we need a lookback on the separator tokens.
        last_separator = None

        rest = node.tokens[node.tokens.index(keyword) + 1:]
        for token in rest:
            if token.type == Token.SEPARATOR:
                last_separator = token
            elif token.type in {Token.EOL, Token.CONTINUATION}:
                continue
            elif token.type == Token.COMMENT:
                # AST splits comments with separators, e.g.
                #
                # "# Comment     rest" -> ["# Comment", "     ", "rest"].
                #
                # Notice the third value not starting with a hash - that's what this
                # condition is about:
                if not str(token).startswith('#'):
                    # -2 because -1 is the EOL
                    comments[-2].value += last_separator.value + token.value
                else:
                    comments += [indent, token, EOL]
            elif token.type == Token.ARGUMENT:
                if self.cols_remaining(line + [separator, token]) == 0:
                    line.append(EOL)
                    tail += line
                    line = [indent, CONTINUATION, separator, token]
                else:
                    line += [separator, token]
            else:
                raise RuntimeError(f"Token with an unrecognized type: {repr(token)}")

        # last line
        line.append(EOL)
        tail += line

        node.tokens = comments + head + tail
        return node

    def cols_remaining(self, tokens):
        if self.split_on_every_arg:
            return 0
        return max(self.line_length - self.len_token_text(self.last_line_of(tokens)), 0)

    @staticmethod
    def len_token_text(tokens):
        return sum(len(token.value) for token in tokens)

    @staticmethod
    def last_line_of(tokens):
        """Return the tokens from after the last EOL in the given list"""
        if EOL not in tokens:
            return tokens
        return tokens[len(tokens) - tokens[::-1].index(EOL):]
