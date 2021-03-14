import os
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

    def __eq__(self, other):
        return other.text == self.text


class GlobalFormattingConfig:
    def __init__(self, use_pipes: bool, space_count: int, line_sep: str, start_line: int, end_line: int):
        self.use_pipes = use_pipes
        self.space_count = space_count
        self.start_line = start_line
        self.end_line = end_line
        if line_sep == 'windows':
            self.line_sep = '\r\n'
        elif line_sep == 'unix':
            self.line_sep = '\n'
        else:
            self.line_sep = os.linesep


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


def node_within_lines(node_start, node_end, start_line, end_line):
    if start_line:
        if node_start < start_line:
            return False
        if end_line:
            if node_end > end_line:
                return False
        else:
            if start_line != node_start:
                return False
    return True


def split_args_from_name_or_path(name):
    """Split arguments embedded to name or path like ``Example:arg1:arg2``.

    The separator can be either colon ``:`` or semicolon ``;``. If both are used,
    the first one is considered to be the separator.
    """
    if os.path.exists(name):
        return name, []
    index = _get_arg_separator_index_from_name_or_path(name)
    if index == -1:
        return name, []
    args = name[index+1:].split(name[index])
    name = name[:index]
    return name, args


def _get_arg_separator_index_from_name_or_path(name):
    colon_index = name.find(':')
    # Handle absolute Windows paths
    if colon_index == 1 and name[2:3] in ('/', '\\'):
        colon_index = name.find(':', colon_index+1)
    semicolon_index = name.find(';')
    if colon_index == -1:
        return semicolon_index
    if semicolon_index == -1:
        return colon_index
    return min(colon_index, semicolon_index)
