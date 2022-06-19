import functools
import re
from typing import List, Optional

from robot.api.parsing import Comment, ModelVisitor, Token

from robotidy.utils import normalize_name


def skip_if_disabled(func):
    """
    Do not transform node if it's not within passed ``start_line`` and ``end_line`` or
    it does match any ``# robotidy: off`` disabler
    """

    @functools.wraps(func)
    def wrapper(self, node, *args):
        if self.disablers.is_node_disabled(node):
            return node
        return func(self, node, *args)

    return wrapper


def skip_section_if_disabled(func):
    """
    Does the same checks as ``skip_if_disabled`` and additionally checks if the section header does not contain disabler
    """

    @functools.wraps(func)
    def wrapper(self, node, *args):
        if self.disablers.is_node_disabled(node):
            return node
        if self.disablers.is_header_disabled(node.lineno):
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
    def __init__(self, start_line, end_line, file_end):
        self.start_line = start_line
        self.end_line = end_line
        self.file_end = file_end
        self.lines = []
        self.disabled_headers = set()

    def add_disabler(self, start_line, end_line):
        self.lines.append((start_line, end_line))

    def add_disabled_header(self, lineno):
        self.disabled_headers.add(lineno)

    def parse_global_disablers(self):
        if not self.start_line:
            return
        end_line = self.end_line if self.end_line else self.start_line
        if self.start_line > 1:
            self.add_disabler(1, self.start_line - 1)
        if end_line < self.file_end:
            self.add_disabler(end_line + 1, self.file_end)

    def sort_disablers(self):
        self.lines = sorted(self.lines, key=lambda x: x[0])

    def is_header_disabled(self, line):
        return line in self.disabled_headers

    def is_node_disabled(self, node, full_match=True):
        if full_match:
            for start_line, end_line in self.lines:
                # lines are sorted on start_line, so we can return on first match
                if end_line >= node.end_lineno:
                    return start_line <= node.lineno
        else:
            for start_line, end_line in self.lines:
                if node.lineno <= end_line and node.end_lineno >= start_line:
                    return True
        return False


class RegisterDisablers(ModelVisitor):
    def __init__(self, start_line, end_line):
        self.start_line = start_line
        self.end_line = end_line
        self.disablers = DisabledLines(self.start_line, self.end_line, None)
        self.disabler_pattern = re.compile(r"\s*#\s?robotidy:\s?(?P<disabler>on|off)")
        self.stack = []
        self.file_disabled = False

    def any_disabler_open(self):
        return any(disabler for disabler in self.stack)

    def get_disabler(self, comment):
        if not comment.value:
            return None
        return self.disabler_pattern.match(comment.value)

    def close_disabler(self, end_line):
        disabler = self.stack.pop()
        if disabler:
            self.disablers.add_disabler(disabler, end_line)

    def visit_File(self, node):  # noqa
        self.disablers = DisabledLines(self.start_line, self.end_line, node.end_lineno)
        self.disablers.parse_global_disablers()
        self.stack = []
        self.file_disabled = False
        self.generic_visit(node)
        self.disablers.sort_disablers()

    def visit_SectionHeader(self, node):  # noqa
        for comment in node.get_tokens(Token.COMMENT):
            disabler = self.get_disabler(comment)
            if disabler and disabler.group("disabler") == "off":
                self.disablers.add_disabled_header(node.lineno)
                break
        return self.generic_visit(node)

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


def parse_and_normalize_csv(value):
    if not value:
        return []
    return [normalize_name(val) for val in value.split(",")]


def make_set(container):
    if container is None:
        return set()
    return set(container)


def str_to_bool(value):
    return value.lower() == "true"


class Skip:
    """Defines global skip conditions for each transformer."""

    # Following names will be taken from transformer config and provided to Skip class instead
    HANDLES = frozenset(
        {
            "skip_documentation",
            "skip_return_values",
            "skip_keyword_call",
            "skip_keyword_call_contains",
            "skip_keyword_call_starts_with",
        }
    )

    def __init__(
        self,
        documentation: bool = False,
        return_values: bool = False,
        keyword_call: Optional[List] = None,
        keyword_call_contains: Optional[List] = None,
        keyword_call_starts_with: Optional[List] = None,
    ):
        self.return_values = return_values
        self.documentation = documentation
        self.keyword_call_names = make_set(keyword_call)
        self.keyword_call_startswith = make_set(keyword_call_starts_with)
        self.keyword_call_contains = make_set(keyword_call_contains)
        self.any_keword_call = self.check_any_keyword_call()

    @classmethod
    def from_str_config(
        cls,
        documentation: str = "False",
        return_values: str = "False",
        keyword_call: str = "",
        keyword_call_contains: str = "",
        keyword_call_starts_with: str = "",
    ):
        documentation = str_to_bool(documentation)
        return_values = str_to_bool(return_values)
        keyword_calls = parse_and_normalize_csv(keyword_call)
        keyword_calls_startswiths = parse_and_normalize_csv(keyword_call_starts_with)
        keyword_calls_contains = parse_and_normalize_csv(keyword_call_contains)
        return cls(
            documentation=documentation,
            return_values=return_values,
            keyword_call=keyword_calls,
            keyword_call_contains=keyword_calls_contains,
            keyword_call_starts_with=keyword_calls_startswiths,
        )

    def check_any_keyword_call(self):
        if self.keyword_call_names:
            return True
        if self.keyword_call_startswith:
            return True
        if self.keyword_call_contains:
            return True
        return False

    def keyword_call(self, node):
        if not getattr(node, "keyword", None) or not self.any_keword_call:
            return False
        normalized = normalize_name(node.keyword)
        if normalized in self.keyword_call_names:
            return True
        for name in self.keyword_call_startswith:
            if normalized.startswith(name):
                return True
        for name in self.keyword_call_contains:
            if name in normalized:
                return True
        return False

    def __eq__(self, other):
        return (
            self.documentation == other.documentation
            and self.return_values == other.return_values
            and self.keyword_call_names == other.keyword_call_names
            and self.keyword_call_startswith == other.keyword_call_startswith
            and self.keyword_call_contains == other.keyword_call_contains
            and self.any_keword_call == other.any_keword_call
        )
