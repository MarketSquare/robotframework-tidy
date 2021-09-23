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

    def __init__(self, case_sensitive=False, reverse=False):
        self.key = self.get_key(case_sensitive)
        self.reverse = reverse
        self.separator = '    '

    def visit_TestCase(self, node):
        return self.order_Tags(node)

    def visit_Keyword(self, node):
        return self.order_Tags(node)

    def order_Tags(self, node):
        for child in node.body:
            if getattr(child, 'type', 'invalid') in (Token.TAGS):
                tags = [tag.value for tag in child.data_tokens[1:]]
                if len(tags) > 1:
                    tags = sorted(tags, key=self.key, reverse=self.reverse)
                    tokens = self.get_tokens_to_add(tags)
                    child.tokens = Tags(
                        (
                            *child.tokens[:2],
                            *tokens,
                            Token(Token.EOL, '\n'),
                        ),
                    )
        return node

    def get_tokens_to_add(self, tags):
        result = ()
        for tag in tags:
            result += (
                Token(Token.SEPARATOR, self.separator),
                Token(Token.TAGS, tag),
            )
        return result

    def get_key(self, case_sensitive):
        default = str.casefold
        if case_sensitive == True:
            return str
        elif case_sensitive == False:
            return str.casefold
        else:
            return default
