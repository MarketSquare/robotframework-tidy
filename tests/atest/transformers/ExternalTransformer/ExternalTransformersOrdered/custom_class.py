from robotidy.transformers import Transformer


class CustomClass1(Transformer):
    def visit_SettingSection(self, node):
        node.header.data_tokens[0].value = node.header.data_tokens[0].value.lower()
        return node
