from robot.parsing.model.visitor import ModelVisitor


class StatementLinesCollector(ModelVisitor):
    def __init__(self, model):
        self.text = ''
        self.visit(model)

    def visit_Statement(self, node):  # noqa
        for token in node.tokens:
            self.text += token.value
