import re
import functools

from robot.api.parsing import ModelVisitor, Comment, Token


def skip_if_disabled(func):
    """
    Do not transform node if it's not within passed start_line and end_line or
    it does match any # robotidy: off disabler
    """

    @functools.wraps(func)
    def wrapper(self, node, *args):
        if not node:
            return node
        if self.disablers.is_node_disabled(node):
            return node
        return func(self, node, *args)

    return wrapper


def is_line_start(node):
    for token in node.tokens:
        if token.type == Token.SEPARATOR:
            continue
        return token.col_offset == 0
    return False


class DisabledLines:
    def __init__(self, start_line, end_line):
        self.start_line = start_line
        self.end_line = end_line
        self.lines = []

    def add_disabler(self, start_line, end_line):
        self.lines.append((start_line, end_line))

    def sort_disablers(self):
        self.lines = sorted(self.lines, key=lambda x: x[0])

    def node_within_global_lines(self, node):
        if self.start_line:
            if node.lineno < self.start_line:
                return False
            if self.end_line:
                if node.end_lineno > self.end_line:
                    return False
            else:
                if self.start_line != node.lineno:
                    return False
        return True

    def is_line_disabled(self, line):
        if self.start_line and self.start_line > line or self.end_line and self.end_line < line:
            return True
        for start_line, end_line in self.lines:
            if start_line <= line <= end_line:
                return True
        return False

    def is_node_disabled(self, node, full_match=True):
        # with full_match node is skipped only if it's fully outside start/end lines
        # it's useful when we allow to transform only part of the node (ie align part of the section)
        if full_match:
            if self.start_line and self.start_line > node.end_lineno or self.end_line and self.end_line < node.lineno:
                return True
        elif not self.node_within_global_lines(node):
            return True
        if full_match:
            for start_line, end_line in self.lines:
                if end_line >= node.end_lineno:
                    return start_line <= node.lineno
        else:
            for start_line, end_line in self.lines:
                # end_line and start_lines theoretically only increase over loop
                if node.lineno <= end_line and node.end_lineno >= start_line:
                    return True
        return False


class RegisterDisablers(ModelVisitor):
    def __init__(self, start_line, end_line):
        self.start_line = start_line
        self.end_line = end_line
        self.disablers = DisabledLines(self.start_line, self.end_line)
        self.stack = []
        self.file_disabled = False

    def any_disabler_open(self):
        return any(disabler for disabler in self.stack)

    @staticmethod
    def get_disabler(comment):
        if not comment.value:
            return None
        return re.match(r"\s*#\s?robotidy:\s?(?P<disabler>on|off)", comment.value)

    def close_disabler(self, end_line):
        disabler = self.stack.pop()
        if disabler:
            self.disablers.add_disabler(disabler, end_line)

    def visit_File(self, node):  # noqa
        self.disablers = DisabledLines(self.start_line, self.end_line)
        self.stack = []
        self.file_disabled = False
        self.generic_visit(node)
        self.disablers.sort_disablers()

    def visit_TestCase(self, node):  # noqa
        self.stack.append(0)
        self.generic_visit(node)
        if self.file_disabled:  # stop visiting if whole file is disabled
            return
        self.close_disabler(node.end_lineno)

    def visit_Try(self, node):  # noqa
        self.generic_visit(node.header)
        self.stack.append(0)
        for statement in node.body:
            self.visit(statement)
        if self.file_disabled:  # stop visiting if whole file is disabled
            return
        self.close_disabler(node.end_lineno)
        tail = node
        while tail.next:
            self.generic_visit(tail.header)
            self.stack.append(0)
            for statement in tail.body:
                self.visit(statement)
            if self.file_disabled:  # stop visiting if whole file is disabled
                return
            end_line = tail.next.lineno - 1 if tail.next else tail.end_lineno
            self.close_disabler(end_line=end_line)
            tail = tail.next

    visit_Keyword = visit_Section = visit_For = visit_ForLoop = visit_If = visit_While = visit_TestCase

    def visit_Statement(self, node):  # noqa
        if isinstance(node, Comment):
            comment = node.get_token(Token.COMMENT)
            disabler = self.get_disabler(comment)
            if not disabler:
                return
            index = 0 if is_line_start(node) else -1
            if disabler.group("disabler") == "on":
                if not self.stack[index]:  # no disabler open
                    return
                self.disablers.add_disabler(self.stack[index], node.lineno)
                self.stack[index] = 0
            else:
                if node.lineno == 1 and index == 0:
                    self.file_disabled = True
                elif not self.stack[index]:
                    self.stack[index] = node.lineno
        else:
            # inline disabler
            if self.any_disabler_open():
                return
            for comment in node.get_tokens(Token.COMMENT):
                disabler = self.get_disabler(comment)
                if disabler and disabler.group("disabler") == "off":
                    self.disablers.add_disabler(node.lineno, node.end_lineno)
