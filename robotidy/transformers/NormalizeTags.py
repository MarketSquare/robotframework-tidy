from robot.api.parsing import ModelTransformer, Tags, Token
import click

class NormalizeTags(ModelTransformer):
    """
    Normalize tag names by normalizing case and removing duplicates.
    example usage:

        robotidy --transform NormalizeTags:case=lowercase test.robot

    Other supported cases: uppercase, titlecase. The default is lowercase.

    You can also run it to remove duplicates but preserve current case by setting ``normalize_case`` parameter to False:

        robotidy --transform NormalizeTags:normalize_case=False test.robot

    See https://robotidy.readthedocs.io/en/latest/transformers/NormalizeTags.html for more examples.
    """
    CASE_FUNCTIONS = {'lowercase': str.lower, 'uppercase': str.upper, 'titlecase': str.title}

    def __init__(self, case: str = 'lowercase', normalize_case: bool = True):
        self.case = case.lower()
        self.normalize_case = normalize_case
        try:
            self.case_function = self.CASE_FUNCTIONS[self.case]
        except KeyError:
            raise click.BadOptionUsage(
                option_name='transform',
                message=f"Invalid configurable value: '{case}' for case for NormalizeTags transformer. "
                        f"Supported cases: lowercase, uppercase, titlecase.\n")

    def visit_Tags(self, node):
        return self.normalize_tags(node)

    def visit_DefaultTags(self, node):
        return self.normalize_tags(node, settings_section=True)

    def visit_ForceTags(self, node):
        return self.normalize_tags(node, settings_section=True)

    def normalize_tags(self, node, settings_section: bool = False):
        tags = [tag.value for tag in node.data_tokens[1:]]
        if self.normalize_case:
            tags = self.convert_case(tags)
        tags = self.remove_duplicates(tags)
        tokens = self.get_tokens(tags)
        if settings_section:
            node.tokens = Tags(
                (
                    node.tokens[0],
                    *tokens,
                    Token(Token.EOL, '\n'),
                ),
            )
        else:
            node.tokens = Tags(
                (
                    *node.tokens[:2],
                    *tokens,
                    Token(Token.EOL, '\n'),
                ),
            )
        return node

    def convert_case(self, tags):
        return [self.case_function(item) for item in tags]

    def remove_duplicates(self, tags):
        return list(dict.fromkeys(tags))

    def get_tokens(self, tags):
        result = []
        separator = Token(Token.SEPARATOR, self.formatting_config.separator)
        for tag in tags:
            result.extend([separator, Token(Token.TAGS, tag)])
        return result

