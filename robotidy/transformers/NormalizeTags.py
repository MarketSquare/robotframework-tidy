from robot.api.parsing import ModelTransformer
from robot.api.parsing import Tags
from robot.api.parsing import Token


class NormalizeTags(ModelTransformer):
    """
    This transformer orders tags.
    example usage:
    robotidy --transform NormalizeTags:case=lowercase test.robot

    Other supported cases: uppercase, titlecase. The default is lowercase.
    See https://robotidy.readthedocs.io/en/latest/transformers/NormalizeTags.html for more examples.
    """
    CASE_FUNCTIONS = {'lowercase': str.lower, 'uppercase': str.upper, 'titlecase': str.title}

    def __init__(self, case: str = 'lowercase'):
        self.case = case
        self.convert_case = self.CASE_FUNCTIONS[self.case]

    def visit_Tags(self, node):
        return self.normalize_tags(node)

    def visit_DefaultTags(self, node):
        return self.normalize_tags(node)

    def visit_ForceTags(self, node):
        return self.normalize_tags(node)

    def normalize_tags(self, node):
        tags = [tag.value for tag in node.data_tokens[1:]]
        print(tags)
        if self.convert_case != None:
            tags = [self.convert_case(item) for item in tags]
        tags = list(dict.fromkeys(tags))
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

