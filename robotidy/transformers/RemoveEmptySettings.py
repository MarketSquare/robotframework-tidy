from robot.api.parsing import (
    ModelTransformer,
    Token
)
from robotidy.decorators import check_start_end_line


class RemoveEmptySettings(ModelTransformer):
    @check_start_end_line
    def visit_Statement(self, node):  # noqa
        if (node.type in Token.SETTING_TOKENS) and len(node.data_tokens) == 1:
            return None
        return node
