import re
from typing import Optional
import string

import click
from robot.api.parsing import ModelTransformer, Token

from robotidy.decorators import check_start_end_line


class RenameKeywords(ModelTransformer):
    """
    Enforce keyword naming.

    Title Case is applied to keyword name and underscores are replaced by spaces.

    You can keep underscores if you set remove_underscores to False:

        robotidy --transform RenameKeywords -c RenameKeywords:remove_underscores=False .

    It is also possible to configure `replace_pattern` parameter to find and replace regex pattern. Use `replace_to`
    to set replacement value. This configuration (underscores are used instead of spaces):

        robotidy --transform RenameKeywords -c RenameKeywords:replace_pattern=^(?i)rename\s?me$:replace_to=New_Shining_Name .

    will transform following code:

        *** Keywords ***
        rename Me
           Keyword Call

    To:

        *** Keywords ***
        New Shining Name
            Keyword Call

    Supports global formatting params: ``--startline`` and ``--endline``.

    See https://robotidy.readthedocs.io/en/latest/transformers/RenameKeywords.html for more examples.
    """
    ENABLED = False

    def __init__(self, replace_pattern: Optional[str] = None, replace_to: Optional[str] = None,
                 remove_underscores: bool = True):
        self.remove_underscores = remove_underscores
        try:
            self.replace_pattern = re.compile(replace_pattern) if replace_pattern is not None else None
        except re.error as err:
            raise click.BadOptionUsage(
                option_name='transform',
                message=f"Invalid configurable value: '{replace_pattern}' for replace_pattern in RenameKeywords"
                        f" transformer. It should be a valid regex expression. Regex error: '{err.msg}'")
        self.replace_to = '' if replace_to is None else replace_to

    @check_start_end_line
    def rename_node(self, node, type_of_name):
        token = node.get_token(type_of_name)
        if not token:
            return node
        if token.value:
            if self.replace_pattern is not None:
                token.value = self.replace_pattern.sub(repl=self.replace_to, string=token.value)
            if self.remove_underscores and token.value != '_':
                token.value = token.value.replace('_', ' ')
                token.value = re.sub(r'\s{2,}', ' ', token.value)  # replace two or more spaces by one
            token.value = string.capwords(token.value.strip())
        return node

    def visit_KeywordName(self, node):  # noqa
        return self.rename_node(node, Token.KEYWORD_NAME)

    def visit_KeywordCall(self, node):  # noqa
        return self.rename_node(node, Token.KEYWORD)
