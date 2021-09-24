from robot.api.parsing import ModelTransformer, Tags, Token


class OrderTags(ModelTransformer):
    """
    Order tags inside Keywords and Test Cases.

    Tags are ordered like this:

        *** Test Cases ***
        Tags Upper Lower
            [Tags]    ba    Ab    Bb    Ca    Cb    aa
            My Keyword

        *** Keywords ***
        My Keyword
            [Tags]    ba    Ab    Bb    Ca    Cb    aa
            No Operation

    To:

        *** Test Cases ***
        Tags Upper Lower
            [Tags]    aa    Ab    ba    Bb    Ca    Cb
            My Keyword

        *** Keywords ***
        My Keyword
            [Tags]    aa    Ab    ba    Bb    Ca    Cb
            No Operation

    Default order can be changed using following parameters:
      - ``case_sensitive = False``
      - ``reverse = False``

    See https://robotidy.readthedocs.io/en/latest/transformers/OrderTags.html for more examples.
    """
    ENABLED = False

    def __init__(self,
                 case_sensitive: bool = False,
                 reverse: bool = False,
                 default_tags: bool = True,
                 force_tags: bool = True):
        self.key = self.get_key(case_sensitive)
        self.reverse = reverse
        self.default_tags = default_tags
        self.force_tags = force_tags

    def visit_Tags(self, node):
        return self.order_tags(node)

    def visit_DefaultTags(self, node):
        return self.order_tags(node) if self.default_tags else node

    def visit_ForceTags(self, node):
        return self.order_tags(node) if self.force_tags else node

    def order_tags(self, node):
        tags = [tag.value for tag in node.data_tokens[1:]]
        if len(tags) > 1:
            tags = sorted(tags, key=self.key, reverse=self.reverse)
            tokens = self.get_tokens(tags)
            node.tokens = Tags(
                (
                    *node.tokens[:2],
                    *tokens,
                    Token(Token.EOL, '\n'),
                ),
            )
        return node

    def get_tokens(self, tags):
        result = []
        separator = Token(Token.SEPARATOR, self.formatting_config.separator)
        for tag in tags:
            result.extend([separator, Token(Token.TAGS, tag)])
        return result

    def get_key(self, case_sensitive):
        default = str.casefold
        if case_sensitive == True:
            return str
        elif case_sensitive == False:
            return str.casefold
        else:
            return default
