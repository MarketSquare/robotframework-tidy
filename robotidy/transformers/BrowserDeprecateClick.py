from robot.api.parsing import Token

from robotidy.transformers import Transformer
from robotidy.utils import normalize_name, split_on_token_type


class ClickArgument:
    def __init__(self, name, value):
        self.name = name
        self.value = value


DEFAULT_PARAMS = [
    ClickArgument("button", "left"),
    ClickArgument("clickCount", "1"),
    ClickArgument("delay", "None"),
    ClickArgument("position_x", "None"),
    ClickArgument("position_y", "None"),
    ClickArgument("force", "False"),
    ClickArgument("noWaitAfter", "False"),
]


class BrowserDeprecateClick(Transformer):
    """
    Short description in one line.

    Long description with short example before/after.
    """

    ENABLED = False
    REPLACE_NAMES = {"browser.click", "click"}

    def visit_KeywordCall(self, node):  # noqa
        # TODO: It can be part of run keyword, setup/teardown etc as well (see RenameKeywords transformer)
        name_token = node.get_token(Token.KEYWORD)
        if not name_token or not name_token.value:
            return node
        keyword_name = normalize_name(name_token.value)
        if keyword_name not in self.REPLACE_NAMES:
            return node
        lib_prefix = keyword_name == "browser.click"
        name_token.value = "Browser.Click With Options" if lib_prefix else "Click With Options"
        return self.convert_args(node)

    def convert_args(self, node):
        # TODO: Current implementation doesn't expect Click  elem  button=right, only Click  elem  right
        # FIXME: Handle comments (at least put them before keyword call if any comments between arguments are found)
        arguments = node.get_tokens(Token.ARGUMENT)
        if not arguments or len(arguments) < 2:
            return node
        kwargs = []
        for arg, default_arg in zip(arguments[1:], DEFAULT_PARAMS):
            if arg.value == default_arg.value:
                continue
            kwargs.append(Token(Token.ARGUMENT, f"{default_arg.name}={arg.value}"))
        args = arguments[8:]
        new_args = [arguments[0], *args, *kwargs]
        # take tokens before keyword name like assign, indentation unchanged
        tokens, after_tokens = split_on_token_type(node.tokens, Token.KEYWORD)
        tokens = list(tokens)  # tokens are tuple by default, splitting tokens also result in tuple
        tokens.append(after_tokens[0])  # keyword name
        for arg in new_args:
            tokens.append(Token(Token.SEPARATOR, self.formatting_config.separator))
            tokens.append(arg)
        tokens.append(Token(Token.EOL))
        node.tokens = tokens
        return node
