from typing import List
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


def decorate_diff_with_color(contents: List[str]) -> str:
    """Inject the ANSI color codes to the diff."""
    for i, line in enumerate(contents):
        if line.startswith("+++") or line.startswith("---"):
            line = f"\033[1;37m{line}\033[0m"  # bold white, reset
        elif line.startswith("@@"):
            line = f"\033[36m{line}\033[0m"  # cyan, reset
        elif line.startswith("+"):
            line = f"\033[32m{line}\033[0m"  # green, reset
        elif line.startswith("-"):
            line = f"\033[31m{line}\033[0m"  # red, reset
        contents[i] = line
    return '\n'.join(contents)


def normalize_name(name):
    return name.lower().replace('_', '').replace(' ', '')