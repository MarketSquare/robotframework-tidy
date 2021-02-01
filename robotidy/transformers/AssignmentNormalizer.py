import re
import ast
from collections import Counter

import click
from robot.api.parsing import (
    ModelTransformer,
    Variable,
    Token
)


class AssignmentNormalizer(ModelTransformer):
    """
    Normalize assignments. By default it detects most common assignment sign
    and apply it to every assignment in given file.

    In this code most common is no equal sign at all. We should remove ``=`` signs from the all lines::

        *** Variables ***
        ${var} =  ${1}
        @{list}  a
        ...  b
        ...  c

        ${variable}=  10


        *** Keywords ***
        Keyword
            ${var}  Keyword1
            ${var}   Keyword2
            ${var}=    Keyword

    To::

        *** Variables ***
        ${var}  ${1}
        @{list}  a
        ...  b
        ...  c

        ${variable}  10


        *** Keywords ***
        Keyword
            ${var}  Keyword1
            ${var}   Keyword2
            ${var}    Keyword

    You can configure that behaviour to automatically add desired equal sign with ``equal_sign_type`` parameter
    (possible types are: ``remove``, ``equal_sign`` ('='), ``space_and_equal_sign`` (' =').

    """
    def __init__(self, equal_sign_type: str = 'autodetect'):
        self.remove_equal_sign = re.compile(r'\s?=$')
        self.file_equal_sign_type = None
        self.equal_sign_type = self.parse_equal_sign_type(equal_sign_type)

    @staticmethod
    def parse_equal_sign_type(value):
        types = {
            'remove': '',
            'equal_sign': '=',
            'space_and_equal_sign': ' =',
            'autodetect': None
        }
        if value not in types:
            raise click.BadOptionUsage(
                option_name='transform',
                message=f"Invalid configurable value: {value} for equal_sign_type for AssignmentNormalizer transformer."
                        f" Possible values:\n    remove\n    equal_sign\n    space_and_equal_sign"
            )
        return types[value]

    def visit_File(self, node):  # noqa
        """
        If no assignment sign was set the file will be scanned to find most common assignment sign.
        This auto detection will happen for every file separately.
        """
        if self.equal_sign_type is None:
            equal_sign_type = self.auto_detect_equal_sign(node)
            if equal_sign_type is None:
                return node
            self.file_equal_sign_type = equal_sign_type
        self.generic_visit(node)
        self.file_equal_sign_type = None

    def visit_KeywordCall(self, node):  # noqa
        if node.assign:  # if keyword returns any value
            assign_tokens = node.get_tokens(Token.ASSIGN)
            self.normalize_equal_sign(assign_tokens[-1])
        return node

    def visit_VariableSection(self, node):  # noqa
        for child in node.body:
            if not isinstance(child, Variable):
                continue
            var_token = child.get_token(Token.VARIABLE)
            self.normalize_equal_sign(var_token)
        return node

    def normalize_equal_sign(self, token):
        token.value = re.sub(self.remove_equal_sign, '', token.value)
        if self.equal_sign_type:
            token.value += self.equal_sign_type
        elif self.file_equal_sign_type:
            token.value += self.file_equal_sign_type

    @staticmethod
    def auto_detect_equal_sign(node):
        auto_detector = AssignmentTypeDetector()
        auto_detector.visit(node)
        return auto_detector.most_common


class AssignmentTypeDetector(ast.NodeVisitor):
    def __init__(self):
        self.sign_counter = Counter()
        self.most_common = None

    def visit_File(self, node):  # noqa
        self.generic_visit(node)
        if len(self.sign_counter) >= 2:
            self.most_common = self.sign_counter.most_common(1)[0][0]

    def visit_KeywordCall(self, node):  # noqa
        if node.assign:  # if keyword returns any value
            sign = self.get_assignment_sign(node.assign[-1])
            self.sign_counter[sign] += 1

    def visit_VariableSection(self, node):  # noqa
        for child in node.body:
            if not isinstance(child, Variable):
                continue
            var_token = child.get_token(Token.VARIABLE)
            sign = self.get_assignment_sign(var_token.value)
            self.sign_counter[sign] += 1
        return node

    @staticmethod
    def get_assignment_sign(token_value):
        return token_value[token_value.find('}')+1:]
