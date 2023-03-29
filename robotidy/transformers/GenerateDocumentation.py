import re
from pathlib import Path

from jinja2 import Template
from robot.api.parsing import Documentation, ModelVisitor, Token

from robotidy.transformers import Transformer

GOOGLE_TEMPLATE = """
{% if keyword.arguments|length > 0 %}
{{ formatting.cont_indent }}Arguments:
{%- for arg in keyword.arguments %}
{{ formatting.cont_indent }}{{ formatting.cont_indent }}{{ arg.name }}: {% endfor %}
{% endif -%}
{% if keyword.returns|length > 0 %}
{{ formatting.cont_indent }}Returns:
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
            self.default = None
        self.full_name = arg

    def __str__(self):
        return self.full_name


class KeywordData:
    def __init__(self, name, arguments, returns):
        self.name = name
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
        # embedded variables
        for variable in node.header.data_tokens[0].tokenize_variables():
            if variable.type == Token.VARIABLE:
                self.arguments.append(Argument(variable.value))
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


class GenerateDocumentation(Transformer):
    """
    Generate keyword documentation with the documentation template.

    By default, GenerateDocumentation uses Google documentation template.
    Following keyword:

    ```robotframework
    *** Keywords ***
    Keyword
        [Arguments]    ${arg}
        ${var}   ${var2}    Step
        RETURN    ${var}    ${var2}
    ```

    will produce following documentation:

    ```robotframework
    *** Keywords ***
    Keyword
        [Documentation]
        ...
        ...    Arguments:
        ...        ${arg}:
        ...
        ...    Returns:
        ...        ${var}
        ...        ${var2}
        [Arguments]    ${arg}
        ${var}   ${var2}    Step
        RETURN    ${var}    ${var2}
    ```

    It is possible to create own template and insert dynamic text like keyword name, argument default values
    or static text (like ``[Documentation]    Documentation stub``). See our docs for more details.

    Generated documentation will be affected by ``NormalizeSeparators`` transformer that's why it's best to
    skip formatting documentation by this transformer:

    ```
    > robotidy --configure GenerateDocumentation:enabled=True --configure NormalizeSeparators:skip_documentation=True src
    ```
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
