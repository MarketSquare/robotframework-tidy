from itertools import tee

from robot.api.parsing import (
    ModelTransformer,
    Token
)


def eol():
    return Token(Token.EOL)


class SplitTooLongLine(ModelTransformer):
    def __init__(self, line_length: int = 120):
        self.line_length = line_length

    def visit_KeywordCall(self, node):  # noqa
        if all(token.end_col_offset <= self.line_length for token in node.tokens[::-1]):
            return node
        if not node.get_tokens(Token.ARGUMENT):  # return if there are no arguments - nothing to split
            return node
        return self.split_keyword_call(node)

    def split_keyword_call(self, node):
        is_single_line = node.lineno == node.end_lineno

        indent = node.tokens[0]
        assignment = list(self.insert_seperator(node.get_tokens(Token.ASSIGN)))
        keyword = node.get_token(Token.KEYWORD)

        if is_single_line:
            comment = node.get_tokens(Token.COMMENT)
            comment_line = [indent] + comment + [eol()] if comment else []

            head = comment_line + [indent] + assignment + [keyword]

            tail = node.tokens[node.tokens.index(keyword) + 1:]
            tail = list(filter(lambda t: t.type != Token.COMMENT, tail))

            lines = []
            for tokenized_line in self.pack_arguments(head, tail, indent):
                lines.extend(tokenized_line)

        else:
            return node  # Not implemented yet

        node.tokens = lines
        return node

    def pack_arguments(self, tokens_so_far, remaining_tokens, indent):
        if not remaining_tokens:
            return []

        # Ensure we are in the correct place to pack
        assert (not remaining_tokens or (
            remaining_tokens[0].type == Token.SEPARATOR
            and remaining_tokens[1].type == Token.ARGUMENT
        ))
        assert tokens_so_far[-1].type != Token.EOL

        line = tokens_so_far[:]

        for token, next_token in self.lookahead(remaining_tokens):
            if token.type in (Token.SEPARATOR, Token.CONTINUATION, Token.EOL):
                continue

            next_tokens = (
                [self.separator(), token, self.separator(), next_token]
                if next_token.type == Token.COMMENT else
                [self.separator(), token]
            )

            if self.cols_remaining(line + next_tokens) == 0:
                line.append(eol())
                yield line
                line = self.arg_continuation(indent)

            line.extend(next_tokens)

        line.append(eol())
        yield line  # last line

    def cols_remaining(self, tokens):
        return max(self.line_length - self.len_token_text(self.last_line_of(tokens)), 0)

    @staticmethod
    def lookahead(iterable):
        iterable, shifted_by_one = tee(iterable)
        next(shifted_by_one, None)
        return zip(iterable, shifted_by_one)

    def separator(self):
        return Token(Token.SEPARATOR, self.formatting_config.space_count * ' ')

    def insert_seperator(self, iterator):
        for elem in iterator:
            yield elem
            yield self.separator()

    def arg_continuation(self, indent):
        return [indent, Token(Token.CONTINUATION)]

    @staticmethod
    def len_token_text(tokens):
        return sum(len(token.value) for token in tokens)

    @staticmethod
    def last_line_of(tokens):
        """Return the tokens from after the last EOL in the given list"""
        if eol() not in tokens:
            return tokens
        return tokens[len(tokens) - tokens[::-1].index(eol()):]
