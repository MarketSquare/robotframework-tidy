from robot.api.parsing import Documentation, Token, ModelVisitor
from jinja2 import Template
from robotidy.transformers import Transformer
import re
from pathlib import Path


GOOGLE_TEMPLATE = """

{% if keyword.arguments|length > 0 -%}{{ formatting.cont_indent }}Arguments:
{%- for arg in keyword.arguments %}
{{ formatting.cont_indent }}{{ formatting.cont_indent }}{{ arg.name }}: {% endfor %}
{% endif -%}
{% if keyword.returns|length > 0 -%}{{ formatting.cont_indent }}Returns:
{%- for value in keyword.returns %}
{{ formatting.cont_indent }}{{ formatting.cont_indent }}{{ value }}: {% endfor %}
{% endif -%}
"""


class Argument:
    def __init__(self, arg):
        if "=" in arg:
            self.name, self.default = arg.split("=", 1)
        else:
            self.name = arg
            self.default = ""
        self.full_name = arg

    def __str__(self):
        return self.full_name


class KeywordData:
    def __init__(self, name, arguments, returns):
        self.name = name.split(".")[-1]
        self.original_name = name
        self.arguments = arguments
        self.returns = returns


class FormattingData:
    def __init__(self, cont_indent, separator):
        self.cont_indent = cont_indent
        self.separator = separator


class ArgumentsAndsReturnsVisitor(ModelVisitor):
    def __init__(self):
        self.arguments = []
        self.returns = []
        self.doc_exists = False

    def visit_Keyword(self, node):  # noqa
        self.arguments = []
        self.returns = []
        self.doc_exists = False
        self.generic_visit(node)

    def visit_Documentation(self, node):  # noqa
        self.doc_exists = True

    def visit_Arguments(self, node):  # noqa
        if node.errors:
            return
        self.arguments = [Argument(arg) for arg in node.values]

    def visit_ReturnStatement(self, node):  # noqa
        if node.errors:
            return
        self.returns = list(node.values)

    visit_Return = visit_ReturnStatement

# TODO: --documentation-template option
# pros:
# autochecked for existence
# can be relative path
# accept : and spaces in value
# cons
# breaks the convenance
class GenerateDocumentation(Transformer):
    """
    Short description in one line.

    Long description with short example before/after.
    """
    ENABLED = False
    # templated test docs?

    WHITESPACE_PATTERN = re.compile(r"(\s{2,}|\t)", re.UNICODE)

    def __init__(self, overwrite: bool = False, doc_template: str = "google"):
        self.overwrite = overwrite
        self.doc_template = Template(self.get_template(doc_template))
        self.args_returns_finder = ArgumentsAndsReturnsVisitor()
        super().__init__()

    @staticmethod
    def get_template(template: str) -> str:
        if template == "google":
            return GOOGLE_TEMPLATE
        template_path = Path(template)
        with open(template_path) as fp:
            return fp.read()

    def visit_Keyword(self, node):  # noqa
        self.args_returns_finder.visit(node)
        if not self.overwrite and self.args_returns_finder.doc_exists:
            return node
        formatting = FormattingData(self.formatting_config.continuation_indent, self.formatting_config.separator)
        kw_data = KeywordData(node.name, self.args_returns_finder.arguments, self.args_returns_finder.returns)
        generated = self.doc_template.render(keyword=kw_data, formatting=formatting)
        doc_node = self.create_documentation_from_string(generated)
        if self.overwrite:
            self.generic_visit(node)  # remove existing [Documentation]
        node.body.insert(0, doc_node)
        return node

    def visit_Documentation(self, node):  # noqa
        return None

    def create_documentation_from_string(self, doc_string):
        new_line = [Token(Token.EOL), Token(Token.SEPARATOR, self.formatting_config.indent), Token(Token.CONTINUATION)]
        tokens = [
            Token(Token.SEPARATOR, self.formatting_config.indent),
            Token(Token.DOCUMENTATION, "[Documentation]"),
        ]
        for index, line in enumerate(doc_string.splitlines()):
            if index != 0:
                tokens.extend(new_line)
            for value in self.WHITESPACE_PATTERN.split(line):
                if not value:
                    continue
                if value.strip():
                    tokens.append(Token(Token.ARGUMENT, value))
                else:
                    tokens.append(Token(Token.SEPARATOR, value))
        tokens.append(Token(Token.EOL))
        return Documentation(tokens)
