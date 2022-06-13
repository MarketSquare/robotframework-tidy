from collections import defaultdict

from robot.api.parsing import ElseHeader, ElseIfHeader, ModelTransformer, ModelVisitor, Token
from robot.parsing.model import Statement

try:
    from robot.api.parsing import InlineIfHeader, TryHeader
except ImportError:
    InlineIfHeader, TryHeader = None, None

from robotidy.disablers import skip_if_disabled
from robotidy.exceptions import InvalidParameterValueError
from robotidy.utils import is_blank_multiline, round_to_four, tokens_by_lines


class AlignKeywordsSection(ModelTransformer):
    """
    Short description in one line.

    Long description with short example before/after.
    """

    ENABLED = False
    DEFAULT_WIDTH = 24

    def __init__(
        self,
        widths: str = "",
        alignment_type: str = "fixed",
        handle_too_long: str = "overflow",
        documentation: str = "skip",
        skip: str = "",
    ):
        self.is_inline = False
        self.indent = 1
        self.handle_too_long = self.parse_handle_too_long(handle_too_long)
        self.fixed_alignment = self.parse_alignment_type(alignment_type)
        self.skip_documentation = self.parse_documentation_mode(documentation)
        # column widths map - 0: 40, 1: 30
        if widths:
            self.widths = self.parse_widths(widths)
        else:
            self.widths = None
        self.auto_widths = []

    def parse_widths(self, widths):
        parsed_widths = dict()
        for index, width in enumerate(widths.split(",")):
            try:
                number = int(width)
                if number < 0:
                    raise ValueError("Should not be a negative number.")
            except ValueError:
                raise InvalidParameterValueError(
                    self.__class__.__name__,
                    "widths",
                    widths,
                    "Widths should be comma separated list of numbers equal or greater than 0.",
                ) from None
            parsed_widths[index] = number
        return parsed_widths

    def parse_handle_too_long(self, value):
        if value not in ("overflow", "compact_overflow", "ignore_line", "ignore_rest"):
            raise InvalidParameterValueError(
                self.__class__.__name__,
                "handle_too_long",
                value,
                "Chose between modes: 'overflow' (align to the next column), 'compact_overflow' (), "
                "'ignore_line' (ignore this line in alignment) or 'ignore_rest' (align to long token and ignore rest)",
            )
        return value

    def parse_alignment_type(self, value):
        if value not in ("fixed", "auto"):
            raise InvalidParameterValueError(
                self.__class__.__name__,
                "alignment_type",
                value,
                "Chose between two modes: 'fixed' (align to fixed width) or "
                "'auto' (align to longest token in column).",
            )
        return value == "fixed"

    def parse_documentation_mode(self, doc_mode):
        if doc_mode not in ("skip", "align_first_col"):
            raise InvalidParameterValueError(
                self.__class__.__name__,
                "doc_mode",
                doc_mode,
                "Chose between two modes: 'skip' (default - do not align documentation) or "
                "'align_first_col' (align first documentation indentation).",
            )
        return doc_mode == "skip"

    def visit_If(self, node):  # noqa
        # ignore inline ifs and their else/else if branches
        if self.is_inline:
            return node
        self.create_auto_widths_for_context(node)
        self.is_inline = InlineIfHeader and isinstance(node.header, InlineIfHeader)
        if self.is_inline:
            self.is_inline = False
            return node
        if not isinstance(node.header, (ElseHeader, ElseIfHeader)):
            self.indent += 1
        self.generic_visit(node)
        if not isinstance(node.header, (ElseHeader, ElseIfHeader)):
            self.indent -= 1
        self.remove_auto_widths_for_context()
        return node

    def visit_Try(self, node):  # noqa
        self.create_auto_widths_for_context(node)
        # do not increase header for Except, Else, Finally - it was done in Try already
        if isinstance(node.header, TryHeader):
            self.indent += 1
        self.generic_visit(node)
        if isinstance(node.header, TryHeader):
            self.indent -= 1
        self.remove_auto_widths_for_context()
        return node

    def visit_For(self, node):  # noqa
        self.create_auto_widths_for_context(node)
        self.indent += 1
        self.generic_visit(node)
        self.indent -= 1
        self.remove_auto_widths_for_context()
        return node

    visit_While = visit_For

    def get_width(self, col):
        # If auto mode is enabled, use auto widths for current context (last defined widths)
        if self.auto_widths:
            widths = self.auto_widths[-1]
        else:
            widths = self.widths
        if not widths:
            return self.DEFAULT_WIDTH
        if col in widths:
            return widths[col]
        return widths[len(widths) - 1]  # if there is no such column, use last column width

    def visit_SettingSection(self, node):  # do the same for test case section in keywords alignment etc
        return node

    @skip_if_disabled
    def visit_Documentation(self, node):  # noqa
        if self.skip_documentation:
            return node
        # For every line:
        # {indent}...{align}{leave alone}
        for line in node.lines:
            sep_count = 0
            prev_token = None
            for token in line:
                if token.type == Token.SEPARATOR:
                    sep_count += 1
                    if sep_count == 1:
                        token.value = self.formatting_config.indent
                    else:
                        width = self.get_width(0)
                        if width == 0:
                            separator_len = round_to_four(
                                len(prev_token.value) + self.formatting_config.space_count
                            ) - len(prev_token.value)
                        else:
                            separator_len = max(width - len(prev_token.value), self.formatting_config.space_count)
                        token.value = " " * separator_len
                        break
                elif token.type != Token.ARGUMENT:  # ...   # comment edge case
                    prev_token = token
        return node

    @skip_if_disabled
    def visit_TestCase(self, node):  # noqa  FIXME Move to AlignTestCases
        self.create_auto_widths_for_context(node)
        self.generic_visit(node)
        self.remove_auto_widths_for_context()
        return node

    @skip_if_disabled
    def visit_Keyword(self, node):  # noqa
        self.create_auto_widths_for_context(node)
        self.generic_visit(node)
        self.remove_auto_widths_for_context()
        return node

    def create_auto_widths_for_context(self, node):
        if self.fixed_alignment:
            return
        counter = ColumnWidthCounter(
            self.disablers,
            self.skip_documentation,
            self.handle_too_long,
            self.widths,
            self.DEFAULT_WIDTH,
            self.formatting_config.space_count,
        )
        counter.visit(node)
        counter.calculate_column_widths()
        self.auto_widths.append(counter.widths)

    def remove_auto_widths_for_context(self):
        if not self.fixed_alignment:
            self.auto_widths.pop()

    def visit_ForHeader(self, node):  # noqa
        # Fix indent for FOR, IF, WHILE, TRY block headers & ends
        indent = Token(Token.SEPARATOR, (self.indent - 1) * self.formatting_config.indent)
        node.tokens = [indent] + list(node.tokens[1:])
        return node

    visit_End = visit_ForHeader  # TODO add other headers

    @skip_if_disabled
    def visit_KeywordCall(self, node):  # noqa
        if node.errors:
            return node
        lines = list(tokens_by_lines(node))
        indent = Token(Token.SEPARATOR, self.indent * self.formatting_config.indent)
        separator = self.formatting_config.space_count
        aligned_statement = []
        for line in lines:
            prev_overflow_len = 0
            fixed_separator = False
            aligned_statement.append(indent)
            if is_blank_multiline(line):  # ...\n edge case
                line[-1].value = line[-1].value.lstrip(" \t")  # normalize eol from '  \n' to '\n'
                aligned_statement.extend(line)
                continue
            tokens, comments = separate_comments(line)
            if len(tokens) < 2:  # only happens with weird encoding, better to skip
                return node
            column = 0
            for token in tokens[:-2]:
                aligned_statement.append(token)
                width = self.get_width(column)
                if width == 0:
                    separator_len = round_to_four(len(token.value) + separator) - len(token.value)
                else:
                    token_len = len(token.value)
                    if fixed_separator:  # ignore_rest is on
                        aligned_statement.append(Token(Token.SEPARATOR, separator * " "))
                        continue
                    separator_len = width - token_len - prev_overflow_len
                    if separator_len < separator:
                        if self.handle_too_long == "ignore_line":
                            return node
                        elif self.handle_too_long == "ignore_rest":
                            fixed_separator = True
                            separator_len = separator
                        elif self.handle_too_long == "compact_overflow":
                            required_width = round_to_four(token_len + separator)
                            separator_len = required_width - token_len
                            prev_overflow_len = required_width - width
                        else:
                            while round_to_four(token_len + separator) > width:
                                column += 1
                                width += self.get_width(column)
                            separator_len = width - token_len
                aligned_statement.append(Token(Token.SEPARATOR, separator_len * " "))
                column += 1
            last_token = strip_extra_whitespace(tokens[-2])
            aligned_statement.extend([last_token, *join_comments(comments), tokens[-1]])

        return Statement.from_tokens(aligned_statement)

    visit_Arguments = (
        visit_Setup
    ) = visit_Teardown = visit_Timeout = visit_Template = visit_Return = visit_Tags = visit_KeywordCall  # TODO skip


def strip_extra_whitespace(token):
    if not token.value:
        return token
    token.value = token.value.strip()
    return token


def separate_comments(tokens):
    non_comments, comments = [], []
    for token in tokens:
        if token.type == Token.COMMENT:
            comments.append(token)
        else:
            non_comments.append(token)
    return non_comments, comments


def join_comments(comments):
    tokens = []
    separator = Token(Token.SEPARATOR, "  ")
    for token in comments:
        tokens.append(separator)
        tokens.append(token)
    return tokens


class ColumnWidthCounter(ModelVisitor):
    NON_DATA_TOKENS = frozenset((Token.SEPARATOR, Token.COMMENT, Token.EOL, Token.EOS))

    def __init__(self, disablers, skip_documentation, handle_too_long, max_widths, default_width, min_separator):
        self.skip_documentation = skip_documentation
        self.handle_too_long = handle_too_long
        self.max_widths = max_widths
        self.default_width = default_width
        self.min_separator = min_separator
        self.raw_widths = defaultdict(list)
        self.widths = dict()
        self.disablers = disablers

    def get_width(self, col):
        if not self.max_widths:
            return self.default_width
        if col in self.max_widths:
            return self.max_widths[col]
        return self.max_widths[len(self.max_widths) - 1]  # if there is no such column, use last column width

    def calculate_column_widths(self):
        if self.max_widths:
            self.widths.update(self.max_widths)
        for column, widths in self.raw_widths.items():
            max_width = self.get_width(column)
            if max_width == 0:
                self.widths[column] = max(widths)
            else:
                filter_widths = [width for width in widths if width <= max_width]
                self.widths[column] = max(filter_widths, default=max_width)

    @skip_if_disabled
    def visit_KeywordCall(self, node):  # noqa
        if node.errors:
            return node
        for line in node.lines:
            # if assign disabled and assign in line: continue
            data_tokens = [token for token in line if token.type not in self.NON_DATA_TOKENS]
            raw_lens = {}
            for column, token in enumerate(data_tokens):
                max_width = self.get_width(column)
                token_len = round_to_four(len(token.value) + self.min_separator)
                if max_width == 0 or token_len <= max_width:
                    raw_lens[column] = token_len
                elif self.handle_too_long == "ignore_line":
                    raw_lens = {}
                    break
                else:  # ignore_rest, overflow and compact_overflow
                    break
            for col, token in raw_lens.items():
                self.raw_widths[col].append(token)

    visit_Arguments = (
        visit_Setup
    ) = visit_Teardown = visit_Timeout = visit_Template = visit_Return = visit_Tags = visit_KeywordCall  # TODO skip

    @skip_if_disabled
    def visit_Documentation(self, node):  # noqa
        if self.skip_documentation:
            return
        doc_header_len = round_to_four(len(node.data_tokens[0].value) + self.min_separator)
        self.raw_widths[0].append(doc_header_len)
