from robot.api.parsing import (
    ModelTransformer,
    Token
)


class SplitTooLongLine(ModelTransformer):
    def __init__(self, line_length: int = 120):
        self.line_length = line_length

    def visit_KeywordCall(self, node):  # noqa
        if all(token.end_col_offset <= self.line_length for token in node.tokens[::-1]):
            return node
        if not node.get_tokens(Token.ARGUMENT):  # return if there are no arguments - nothing to split
            return node
        return self.split_every_line(node)

    def split_every_line(self, node):
        indent = node.tokens[0]
        separator = Token(Token.SEPARATOR, self.formatting_config.space_count * ' ')
        assign = node.get_tokens(Token.ASSIGN)
        assigned = list(self.insert_seperator(assign, separator))
        keyword = node.get_tokens(Token.KEYWORD)
        tokens = [token for token in node.tokens if token.type in (Token.ARGUMENT, Token.COMMENT)]
        splitted_tokens = [indent] + assigned + keyword
        curr_len = self.len_of_tokens(splitted_tokens)
        for token in tokens:
            if self.split_only_at_max_length:
                next_token_len = self.len_of_tokens([separator, token])
                if (curr_len + next_token_len) < self.line_length:
                    splitted_tokens.append(separator)
                    splitted_tokens.append(token)
                    curr_len += next_token_len
                else:
                    splitted_tokens.extend(self.new_line(indent, separator, token))
                    curr_len = next_token_len + len(indent.value) + 3
            else:
                splitted_tokens.extend(self.new_line(indent, separator, token))

        node.tokens = splitted_tokens + [Token(Token.EOL)]
        return node

    @staticmethod
    def insert_seperator(iterator, separator):
        for elem in iterator:
            yield elem
            yield separator

    @staticmethod
    def new_line(indent, separator, token):
        return [Token(Token.EOL), indent, Token(Token.CONTINUATION), separator, token]

    @staticmethod
    def len_of_tokens(tokens):
        return sum(len(token.value) for token in tokens)
