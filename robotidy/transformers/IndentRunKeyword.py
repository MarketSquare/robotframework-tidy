from robot.api.parsing import ModelTransformer, Token

from robotidy.disablers import skip_if_disabled
from robotidy.utils import normalize_name


class RunKeywordVariant:
    def __init__(self, libname, name, resolve=1, branches=None, split_on_and=False):
        self.libname = normalize_name(libname)
        self.name = normalize_name(name)
        self.resolve = resolve
        self.branches = branches
        self.split_on_and = split_on_and


class IndentRunKeyword(ModelTransformer):
    """
    Short description in one line.

    Long description with short example before/after.

    See https://robotidy.readthedocs.io/en/latest/transformers/IndentRunKeyword.html for more examples.
    """

    ENABLED = False
    RUN_KW = [
        RunKeywordVariant("BuiltIn", "Run Keyword And Continue On Failure"),
        RunKeywordVariant("BuiltIn", "Run Keywords", split_on_and=True),
        RunKeywordVariant("BuiltIn", "Run Keyword If", resolve=2, branches=["ELSE IF", "ELSE"]),
        RunKeywordVariant("BuiltIn", "Repeat Keyword", resolve=2),
        RunKeywordVariant("BuiltIn", "Wait Until Keyword Succeeds", resolve=3),
    ]

    def __init__(self):
        self.run_keywords = dict()
        for run_kw in self.RUN_KW:
            self.run_keywords[run_kw.name] = run_kw
            self.run_keywords[f"{run_kw.libname}.{run_kw.name}"] = run_kw

    def get_run_keyword(self, kw_name):
        kw_norm = normalize_name(kw_name)
        return self.run_keywords.get(kw_norm, None)

    @staticmethod
    def join_on_separator(tokens, separator):
        joined = [separator] * (len(tokens) * 2 - 1)
        joined[0::2] = tokens
        return joined

    @skip_if_disabled
    def visit_KeywordCall(self, node):  # noqa
        # TODO what about comments?
        if not node.keyword:
            return node
        run_keyword = self.get_run_keyword(node.keyword)
        if not run_keyword:
            return node
        indent = node.tokens[0]
        new_line = [Token(Token.EOL), indent, Token(Token.CONTINUATION)]
        separator = Token(Token.SEPARATOR, self.formatting_config.separator)
        assign, kw_tokens = self.split_on_type(node.data_tokens, Token.KEYWORD)
        lines = self.parse_sub_kw(kw_tokens)
        tokens = []
        for index, (level, line) in enumerate(lines):
            if index == 0:
                tokens.append(indent)
                if assign:
                    tokens.extend(self.join_on_separator(assign, separator))
                    tokens.append(separator)
            else:
                tokens.extend(new_line)
                tokens.append(Token(Token.SEPARATOR, self.formatting_config.separator * level))
            tokens.extend(self.join_on_separator(line, separator))
        tokens.append(node.tokens[-1])  # eol
        node.tokens = tokens
        return node

    @staticmethod
    def split_on_type(tokens, token_type):
        for index, token in enumerate(tokens):
            if token.type == token_type:
                return tokens[:index], tokens[index:]

    @staticmethod
    def word_in_tokens(word, tokens):
        return any(word == token.value for token in tokens)

    @staticmethod
    def split_on_marker(tokens, marker, resolve):
        for index, token in enumerate(tokens):
            if marker == token.value:
                prefix = tokens[:index]
                branch = tokens[index:index + resolve]
                remainder = tokens[index + resolve:]
                return prefix, branch, remainder
        else:
            return [], [], tokens

    def parse_sub_kw(self, tokens, level=0):
        if not tokens:
            return []
        run_keyword = self.get_run_keyword(tokens[0].value)
        if not run_keyword:
            return [(level, list(tokens))]
        lines = [(level, tokens[:run_keyword.resolve])]
        tokens = tokens[run_keyword.resolve:]
        if run_keyword.branches:
            while "ELSE IF" in run_keyword.branches and self.word_in_tokens("ELSE IF", tokens):
                level = max(level, 1)
                prefix, branch, tokens = self.split_on_marker(tokens, "ELSE IF", 2)
                lines += self.parse_sub_kw(prefix, level+1)
                lines.append((level, branch))
            if "ELSE" in run_keyword.branches and self.word_in_tokens("ELSE", tokens):
                level = max(level, 1)
                prefix, branch, tokens = self.split_on_marker(tokens, "ELSE", 1)
                lines += self.parse_sub_kw(prefix, level+1)
                lines.append((level, branch))
                lines += self.parse_sub_kw(tokens, level+1)
                return lines
        elif run_keyword.split_on_and:
            if self.word_in_tokens("AND", tokens):
                while self.word_in_tokens("AND", tokens):
                    prefix, branch, tokens = self.split_on_marker(tokens, "AND", 1)
                    lines += self.parse_sub_kw(prefix, level + 1)
                    lines.append((level + 1, branch))
                lines += self.parse_sub_kw(tokens, level+1)
            else:
                keywords = [(level + 1, [kw_token]) for kw_token in tokens]
                lines += keywords
            return lines
        return lines + self.parse_sub_kw(tokens, level+1)
