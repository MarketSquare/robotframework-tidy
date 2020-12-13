from robot.parsing.model.visitor import ModelVisitor


class StatementLinesCollector(ModelVisitor):
    """
    Used to get writeable presentation of Robot Framework model.
    """
    def __init__(self, model):
        self.text = ''
        self.visit(model)

    def visit_Statement(self, node):  # noqa
        for token in node.tokens:
            self.text += token.value
