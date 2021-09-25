from robot.api.parsing import ModelTransformer, Tags, Token, DefaultTags, ForceTags


class OrderTags(ModelTransformer):
    """
    Order tags.

    Tags are ordered in lexicographic order like this:

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

    def visit_Tags(self, node):  # noqa
        tags = self.order_tags(node)
        if len(tags) <= 1:
            return node
        comments = node.get_tokens(Token.COMMENT)
        node = Tags.from_params(tags, separator=self.formatting_config.separator)
        if comments:
            node.tokens += tuple(self.join_tokens(comments))
        return node

    def visit_DefaultTags(self, node):  # noqa
        if not self.default_tags:
            return node
        tags = self.order_tags(node)
        if len(tags) <= 1:
            return node
        comments = node.get_tokens(Token.COMMENT)
        node = DefaultTags.from_params(tags, separator=self.formatting_config.separator)
        if comments:
            node.tokens += tuple(self.join_tokens(comments))
        return node

    def visit_ForceTags(self, node):  # noqa
        if not self.force_tags:
            return node
        tags = self.order_tags(node)
        if len(tags) <= 1:
            return node
        comments = node.get_tokens(Token.COMMENT)
        node = ForceTags.from_params(tags, separator=self.formatting_config.separator)
        if comments:
            node.tokens += tuple(self.join_tokens(comments))
        return node

    def order_tags(self, node):
        return sorted((tag.value for tag in node.data_tokens[1:]), key=self.key, reverse=self.reverse)

    def join_tokens(self, tokens):
        joined_tokens = []
        for token in tokens:
            joined_tokens.append(Token(Token.SEPARATOR, self.formatting_config.separator))
            joined_tokens.append(token)
        return joined_tokens

    @staticmethod
    def get_key(case_sensitive):
        return str if case_sensitive else str.casefold
