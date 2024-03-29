from robot.api import Token

from robotidy.transformers import Transformer


class CustomClass1(Transformer):
    def visit_SettingSection(self, node):
        node.header.data_tokens[0].value = node.header.data_tokens[0].value.lower()
        return node


class CustomClass2(Transformer):
    def __init__(self, extra_param: bool = False):
        self.extra_param = extra_param
        super().__init__()

    def visit_TestCaseName(self, node):  # noqa
        """If extra_param is set to True, lower case the test case name."""
        if not self.extra_param:
            return node
        token = node.get_token(Token.TESTCASE_NAME)
        token.value = token.value.lower()
        return node
