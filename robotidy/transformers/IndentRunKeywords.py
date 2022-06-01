from robot.api.parsing import ModelTransformer, Token

from robotidy.disablers import skip_if_disabled
from robotidy.utils import (
    collect_comments_from_tokens,
    is_token_value_in_tokens,
    join_tokens_with_token,
    normalize_name,
    merge_comments_into_one,
    split_on_token_type,
    split_on_token_value,
)


class RunKeywordVariant:
    def __init__(self, libname, name, resolve=1, branches=None, split_on_and=False):
        self.libname = normalize_name(libname)
        self.name = normalize_name(name)
        self.resolve = resolve
        self.branches = branches
        self.split_on_and = split_on_and


class IndentRunKeywords(ModelTransformer):
    """
    Format indentation inside run keywords variants such as ``Run Keywords`` or
    ``Run Keyword And Continue On Failure``.

    Keywords inside run keywords variants are detected and
    whitespace is formatted to outline them. This code:

    ```robotframework
        Run Keyword    Run Keyword If    ${True}    Run keywords   Log    foo    AND    Log    bar    ELSE    Log    baz
    ```

    will be transformed to:

    ```robotframework
        Run Keyword
        ...    Run Keyword If    ${True}
        ...        Run keywords
        ...            Log    foo
        ...            AND
        ...            Log    bar
        ...    ELSE
        ...        Log    baz
    ```

    It is possible to provide extra indentation for keywords using ``AND`` separators
    by configuring ``indent_and`` to ``True``:
    ```
    robotidy -c IndentRunKeywords:indent_and=True src
    ```

    It will result in:
    ```
    Run keywords
    ...        Log    foo
    ...    AND
    ...        Log    bar
    ```
    
    To skip formatting run keywords inside settings (such as ``Suite Setup``, ``[Setup]``, ``[Teardown]`` etc.) set
    ``skip_settings`` to ``True``.
    """

    ENABLED = False
    RUN_KW = [
        RunKeywordVariant("BuiltIn", "Run Keyword"),
        RunKeywordVariant("BuiltIn", "Run Keyword And Continue On Failure"),
        RunKeywordVariant("BuiltIn", "Run Keyword And Expect Error", resolve=2),
        RunKeywordVariant("BuiltIn", "Run Keyword And Ignore Error"),
        RunKeywordVariant("BuiltIn", "Run Keyword And Return"),
        RunKeywordVariant("BuiltIn", "Run Keyword And Return If", resolve=2),
        RunKeywordVariant("BuiltIn", "Run Keyword And Return Status"),
        RunKeywordVariant("BuiltIn", "Run Keyword And Warn On Failure"),
        RunKeywordVariant("BuiltIn", "Run Keyword If", resolve=2, branches=["ELSE IF", "ELSE"]),
        RunKeywordVariant("BuiltIn", "Run Keyword If All Tests Passed"),
        RunKeywordVariant("BuiltIn", "Run Keyword If Any Tests Failed"),
        RunKeywordVariant("BuiltIn", "Run Keyword If Test Failed"),
        RunKeywordVariant("BuiltIn", "Run Keyword If Test Passed"),
        RunKeywordVariant("BuiltIn", "Run Keyword If Timeout Occurred"),
        RunKeywordVariant("BuiltIn", "Run Keyword Unless", resolve=2),
        RunKeywordVariant("BuiltIn", "Run Keywords", split_on_and=True),
        RunKeywordVariant("BuiltIn", "Repeat Keyword", resolve=2),
        RunKeywordVariant("BuiltIn", "Wait Until Keyword Succeeds", resolve=3),
    ]

    def __init__(self, indent_and: bool = False, skip_settings: bool = False):
        self.indent_and = indent_and
        self.skip_settings = skip_settings
        self.run_keywords = dict()
        for run_kw in self.RUN_KW:
            self.run_keywords[run_kw.name] = run_kw
            self.run_keywords[f"{run_kw.libname}.{run_kw.name}"] = run_kw

    def get_run_keyword(self, kw_name):
        kw_norm = normalize_name(kw_name)
        return self.run_keywords.get(kw_norm, None)

    @skip_if_disabled
    def visit_SuiteSetup(self, node):  # noqa
        if self.skip_settings or node.errors or not len(node.data_tokens) > 1:
            return node
        run_keyword = self.get_run_keyword(node.data_tokens[1].value)
        if not run_keyword:
            return node
        lines = self.parse_sub_kw(node.data_tokens[1:])
        if not lines:
            return node
        comments = collect_comments_from_tokens(node.tokens, indent=None)
        separator = Token(Token.SEPARATOR, self.formatting_config.separator)
        new_line = [Token(Token.EOL), Token(Token.CONTINUATION)]
        tokens = [node.data_tokens[0], separator, *join_tokens_with_token(lines[0][1], separator)]
        for level, line in lines[1:]:
            tokens.extend(new_line)
            tokens.append(Token(Token.SEPARATOR, self.formatting_config.separator * level))
            tokens.extend(join_tokens_with_token(line, separator))
        tokens.append(node.tokens[-1])  # eol
        node.tokens = tokens
        return (*comments, node)

    visit_SuiteTeardown = visit_TestSetup = visit_TestTeardown = visit_SuiteSetup

    @skip_if_disabled
    def visit_Setup(self, node):  # noqa
        if self.skip_settings or node.errors or not len(node.data_tokens) > 1:
            return node
        run_keyword = self.get_run_keyword(node.data_tokens[1].value)
        if not run_keyword:
            return node
        lines = self.parse_sub_kw(node.data_tokens[1:])
        if not lines:
            return node
        indent = node.tokens[0]
        separator = Token(Token.SEPARATOR, self.formatting_config.separator)
        new_line = [Token(Token.EOL), indent, Token(Token.CONTINUATION)]
        tokens = [indent, node.data_tokens[0], separator, *join_tokens_with_token(lines[0][1], separator)]
        comment = merge_comments_into_one(node.tokens)
        if comment:
            # need to add comments on first line for [Setup] / [Teardown] settings
            comment_sep = Token(Token.SEPARATOR, "  ")
            tokens.extend([comment_sep, Token(Token.COMMENT, comment)])
        for level, line in lines[1:]:
            tokens.extend(new_line)
            tokens.append(Token(Token.SEPARATOR, self.formatting_config.separator * level))
            tokens.extend(join_tokens_with_token(line, separator))
        tokens.append(node.tokens[-1])  # eol
        node.tokens = tokens
        return node

    visit_Teardown = visit_Setup

    @skip_if_disabled
    def visit_KeywordCall(self, node):  # noqa
        if node.errors or not node.keyword:
            return node
        run_keyword = self.get_run_keyword(node.keyword)
        if not run_keyword:
            return node
        indent = node.tokens[0]
        comments = collect_comments_from_tokens(node.tokens, indent)

        assign, kw_tokens = split_on_token_type(node.data_tokens, Token.KEYWORD)
        lines = self.parse_sub_kw(kw_tokens)

        tokens = []
        separator = Token(Token.SEPARATOR, self.formatting_config.separator)
        new_line = [Token(Token.EOL), indent, Token(Token.CONTINUATION)]
        for index, (level, line) in enumerate(lines):
            if index == 0:
                tokens.append(indent)
                if assign:
                    tokens.extend(join_tokens_with_token(assign, separator))
                    tokens.append(separator)
            else:
                tokens.extend(new_line)
                tokens.append(Token(Token.SEPARATOR, self.formatting_config.separator * level))
            tokens.extend(join_tokens_with_token(line, separator))
        tokens.append(node.tokens[-1])  # eol
        node.tokens = tokens
        return (*comments, node)

    def parse_sub_kw(self, tokens, level=0):
        if not tokens:
            return []
        run_keyword = self.get_run_keyword(tokens[0].value)
        if not run_keyword:
            return [(level, list(tokens))]
        lines = [(level, tokens[: run_keyword.resolve])]
        tokens = tokens[run_keyword.resolve :]
        if run_keyword.branches:
            if "ELSE IF" in run_keyword.branches:
                while is_token_value_in_tokens("ELSE IF", tokens):
                    level = max(level, 1)
                    prefix, branch, tokens = split_on_token_value(tokens, "ELSE IF", 2)
                    lines += self.parse_sub_kw(prefix, level + 1)
                    lines.append((level, branch))
            if "ELSE" in run_keyword.branches and is_token_value_in_tokens("ELSE", tokens):
                return self.split_on_else(tokens, lines, level)
        elif run_keyword.split_on_and:
            return self.split_on_and(tokens, lines, level)
        return lines + self.parse_sub_kw(tokens, level + 1)

    def split_on_else(self, tokens, lines, level):
        level = max(level, 1)
        prefix, branch, tokens = split_on_token_value(tokens, "ELSE", 1)
        lines += self.parse_sub_kw(prefix, level + 1)
        lines.append((level, branch))
        lines += self.parse_sub_kw(tokens, level + 1)
        return lines

    def split_on_and(self, tokens, lines, level):
        if is_token_value_in_tokens("AND", tokens):
            while is_token_value_in_tokens("AND", tokens):
                prefix, branch, tokens = split_on_token_value(tokens, "AND", 1)
                lines += self.parse_sub_kw(prefix, level + 1 + int(self.indent_and))
                lines.append((level + 1, branch))
            lines += self.parse_sub_kw(tokens, level + 1 + int(self.indent_and))
        else:
            keywords = [(level + 1, [kw_token]) for kw_token in tokens]
            lines += keywords
        return lines
