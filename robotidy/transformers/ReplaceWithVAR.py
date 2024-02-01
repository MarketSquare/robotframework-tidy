from copy import deepcopy
from typing import TYPE_CHECKING, List, Optional, Tuple

from robot.api.parsing import Comment, ElseHeader, ElseIfHeader, End, If, IfHeader, KeywordCall, Token
from robot.variables.search import is_list_variable

try:
    from robot.api.parsing import InlineIfHeader, Var
except ImportError:
    InlineIfHeader, Var = None, None

from robotidy.disablers import skip_if_disabled
from robotidy.transformers import Transformer
from robotidy.utils import misc

if TYPE_CHECKING:
    from robot.parsing.model.blocks import If


class ReplaceWithVAR(Transformer):
    """
    Short description in one line.

    Long description with short example before/after.
    """

    ENABLED = False
    MIN_VERSION = 7
    SET_SCOPE = {
        "setlocalvariable": "local",
        "settaskvariable": "task",
        "settestvariable": "test",
        "setsuitevariable": "suite",
        "setglobalvariable": "global",
    }
    SUPPORTS_CHILDREN_ARG = "setsuitevariable"

    def __init__(
        self,
        explicit_local: bool = False,
        replace_catenate: bool = True,
        replace_create_list: bool = True,
        replace_create_dictionary: bool = True,
        replace_set_variable_if: bool = True,
    ):
        super().__init__()
        self.explicit_local = explicit_local
        self.replace_catenate = replace_catenate
        self.replace_create_list = replace_create_list
        self.replace_create_dictionary = replace_create_dictionary
        self.replace_set_variable_if = replace_set_variable_if
        self.SET_KW = {
            "setvariable": self.replace_set_variable,
            "setlocalvariable": self.replace_set_variable_scope,
            "settaskvariable": self.replace_set_variable_scope,
            "settestvariable": self.replace_set_variable_scope,
            "setsuitevariable": self.replace_set_variable_scope,
            "setglobalvariable": self.replace_set_variable_scope,
            "setvariableif": self.replace_set_variable_if_kw,
            "catenate": self.replace_catenate_kw,
            "createlist": self.replace_create_list_kw,
            "createdictionary": self.replace_create_dictionary_kw,
        }

    @skip_if_disabled
    def visit_KeywordCall(self, node):  # noqa
        if node.errors:
            return node
        kw_name = misc.after_last_dot(misc.normalize_name(node.keyword))
        if kw_name not in self.SET_KW:
            return node
        # we can retrieve comments here
        # single comments we could try to stick to line where VAR is
        # multiple comments need to be put in separate lines before VAR
        comments = node.get_tokens(Token.COMMENT)
        indent = node.get_token(Token.SEPARATOR)
        converted_node = self.SET_KW[kw_name](node, kw_name, indent.value)
        if converted_node is None:
            return node
        return self.restore_comments(converted_node, comments, indent.value)

    # def visit_TestCase(self, node):
    #     if "Inline IF set if and custom keyword value2" in node.name:
    #         print()
    #     return self.generic_visit(node)

    def visit_If(self, node: "If"):  # noqa
        if not self.is_inline_if(node):
            return self.generic_visit(node)
        # FIXME comments
        indent = node.header.get_token(Token.SEPARATOR).value
        block_indent = indent + self.formatting_config.indent
        block_indent_token = Token(Token.SEPARATOR, block_indent)
        sep_token = Token(Token.SEPARATOR, self.formatting_config.separator)
        assign = self.get_assign_names(node.assign)
        assign_tokens = misc.join_tokens_with_token(
            [Token(Token.ASSIGN, assign_val) for assign_val in assign], sep_token
        )
        modified = False
        head = tail = None
        source_node = node  # TODO replace with node
        while True:
            # TODO pop comments
            branch_statement = source_node.body[0]
            if isinstance(branch_statement, KeywordCall):
                if branch_statement.errors:
                    return node
                kw_name = misc.after_last_dot(misc.normalize_name(branch_statement.keyword))
                if kw_name in self.SET_KW:
                    branch_statement = self.SET_KW[kw_name](branch_statement, kw_name, block_indent, assign)
                    if branch_statement is None:
                        return node
                    modified = True
                else:
                    if assign:
                        kw_tokens = (
                            [block_indent_token] + assign_tokens + [sep_token] + list(branch_statement.tokens[1:])
                        )
                    else:
                        kw_tokens = [block_indent_token] + list(branch_statement.tokens[1:])
                    if kw_tokens[-1].type == Token.SEPARATOR:
                        kw_tokens[-1] = Token(Token.EOL)
                    branch_statement = KeywordCall.from_tokens(kw_tokens)
            else:
                kw_tokens = [block_indent_token] + list(branch_statement.tokens[1:])
                if kw_tokens[-1].type == Token.SEPARATOR:
                    kw_tokens[-1] = Token(Token.EOL)
                branch_statement = KeywordCall.from_tokens(kw_tokens)
            if tail:
                if isinstance(source_node.header, ElseIfHeader):
                    header = ElseIfHeader.from_params(condition=source_node.header.condition, indent=indent)
                else:
                    header = ElseHeader.from_params(indent=indent)
            else:
                header = IfHeader.from_params(condition=source_node.header.condition, indent=indent)
            if not isinstance(branch_statement, list):
                branch_statement = [branch_statement]
            if_node = If(header=header, body=branch_statement)
            if head:
                tail.orelse = if_node
            else:
                head = if_node
                head.end = End.from_params(indent=indent)
            source_node = source_node.orelse
            tail = if_node
            if not source_node:
                break
        if modified:
            return head
        return node

    def is_inline_if(self, node):
        return isinstance(node.header, InlineIfHeader)

    @staticmethod
    def update_statement_in_inline_if(statement, indent_token):
        updated_tokens = [indent_token] + list(statement.tokens[1:])
        if updated_tokens[-1].type == Token.SEPARATOR:
            updated_tokens[-1] = Token(Token.EOL)
        statement.tokens = tuple(updated_tokens)
        return statement

    def restore_comments(self, node, comments: List[Token], indent: str):
        if not comments:
            return node
        if len(comments) == 1:
            # insert comment between last data token and EOL
            node.tokens = tuple(list(node.tokens[:-1]) + [Token(Token.SEPARATOR, "  "), comments[0], node.tokens[-1]])
            return node
        comment_nodes = [Comment.from_params(comment=comment.value, indent=indent) for comment in comments]
        return *comment_nodes, node

    def resolve_variable_name(self, name: str) -> Optional[str]:
        if name.startswith("\\"):
            name = name[1:]
        if len(name) < 2 or name[0] not in "$@&":
            return None
        if name[1] != "{":
            name = f"{name[0]}{{{name[1:]}}}"
        return name

    def resolve_assign_name(self, name: str) -> str:
        return name.rstrip("=").rstrip()

    def get_assign_names(self, assign: Tuple[str]) -> List[str]:
        return [self.resolve_assign_name(assign) for assign in assign]

    def replace_set_variable(self, node, kw_name: str, indent: str, assign: Optional[List[str]] = None):
        assign = assign or self.get_assign_names(node.assign)
        args = node.get_tokens(Token.ARGUMENT)
        if len(assign) != len(args) and (len(assign) != 1 or args):
            return None
        if args:
            values = [arg.value if arg.value else "${EMPTY}" for arg in args]
        else:
            values = ["${EMPTY}"]
        if len(assign) == 1:
            var_name = assign[0]
            if len(values) > 1:
                var_name = "@" + var_name[1:]
            return Var.from_params(name=var_name, value=values, indent=indent)
        return [
            Var.from_params(name=var_assign, value=value, indent=indent) for var_assign, value in zip(assign, values)
        ]

    def replace_set_variable_scope(self, node, kw_name: str, indent: str, assign: Optional[List[str]] = None):
        assign = assign or node.assign
        args = node.get_tokens(Token.ARGUMENT)
        if not args or assign:
            return None
        scope = self.SET_SCOPE[kw_name]
        var_name = args[0].value
        var_name = self.resolve_variable_name(var_name)
        if not var_name:
            return None
        if len(args) > 1:
            values = [arg.value for arg in args[1:]]
            if kw_name == self.SUPPORTS_CHILDREN_ARG and any(value.startswith("children=") for value in values):
                return None
            if len(values) > 1:
                if all("=" in value for value in values):
                    var_name = "&" + var_name[1:]
                else:
                    var_name = "@" + var_name[1:]
        else:
            values = [var_name]
        scope = scope.upper() if self.explicit_local or scope != "local" else None
        return Var.from_params(name=var_name, value=values, indent=indent, scope=scope)

    def replace_set_variable_if_kw(self, node, kw_name: str, indent: str, assign: Optional[List[str]] = None):
        """
        # ${var}    Set Variable If    ${cond}    1
        # IF    ${cond}    VAR    1    ELSE    VAR    ${None}

        # ${var}    Set Variable If    ${cond}    1    2
        # IF    ${cond}    VAR    1    ELSE    VAR    2

        # ${var}    Set Variable If    ${cond}    1    ${cond2}    1
        # IF    ${cond}    VAR    1    ELSE IF    ${cond2}    VAR    1    ELSE    VAR    ${None}

        # Set Variable If    @{ITEMS} -> cannot be converted
        """
        # TODO set indent and separator
        assign = assign or self.get_assign_names(node.assign)
        if not self.replace_set_variable_if or len(assign) != 1:
            return None
        args = [arg.value for arg in node.get_tokens(Token.ARGUMENT)]
        if len(args) < 2 or any(is_list_variable(arg) for arg in args):
            return None
        scope = "LOCAL" if self.explicit_local else None
        in_block_indent = indent + self.formatting_config.indent
        var_name = assign[0]
        head = tail = None
        while True:
            if not args:
                condition, value = None, "${None}"
            elif len(args) == 1:
                condition, value = None, args[0]
            else:
                condition, value = args[:2]
            variable = Var.from_params(name=var_name, value=value, indent=in_block_indent, scope=scope)
            if tail:
                if condition:
                    header = ElseIfHeader.from_params(condition=condition, indent=indent)
                else:
                    header = ElseHeader.from_params(indent=indent)
            else:
                header = IfHeader.from_params(condition=condition, indent=indent)
            if_node = If(header=header, body=[variable])
            if head:
                tail.orelse = if_node
            else:
                head = if_node
                head.end = End.from_params(indent=indent)
            tail = if_node
            if len(args) < 2:
                return head
            args = args[2:]

    def replace_catenate_kw(self, node, kw_name: str, indent: str, assign: Optional[List[str]] = None):
        assign = assign or self.get_assign_names(node.assign)
        # not items - VAR with ${EMPTY}
        if not self.replace_catenate or len(assign) != 1:
            return None
        args = node.get_tokens(Token.ARGUMENT)
        if not args:
            return None
        var_name = assign[0]
        values = [arg.value if arg.value else "${EMPTY}" for arg in args]
        if values[0].startswith("SEPARATOR="):
            separator = values[0].replace("SEPARATOR=", "", 1) or "${SPACE}"
            values = values[1:]
            if not values:
                values = ["${EMPTY}"]
        else:
            separator = "${SPACE}"
        scope = "LOCAL" if self.explicit_local else None
        return Var.from_params(name=var_name, value=values, indent=indent, value_separator=separator, scope=scope)

    def replace_create_list_kw(self, node, kw_name: str, indent: str, assign: Optional[List[str]] = None):
        assign = assign or self.get_assign_names(node.assign)
        if not self.replace_create_list or len(assign) != 1:
            return None
        var_name = assign[0]
        var_name = "@" + var_name[1:]
        args = node.get_tokens(Token.ARGUMENT)
        if args:
            # TODO test for single empty values ie Create List \n ...
            values = [arg.value if arg.value else "${EMPTY}" for arg in args]
        else:
            values = ["@{EMPTY}"]
        scope = "LOCAL" if self.explicit_local else None
        return Var.from_params(name=var_name, value=values, indent=indent, scope=scope)

    def replace_create_dictionary_kw(self, node, kw_name: str, indent: str, assign: Optional[List[str]] = None):
        assign = assign or self.get_assign_names(node.assign)
        if not self.replace_create_dictionary or len(assign) != 1:
            return None
        var_name = assign[0]
        var_name = "&" + var_name[1:]
        args = node.get_tokens(Token.ARGUMENT)
        if args:
            # TODO empty values?
            values = [arg.value for arg in args]
            if any(not value for value in values):
                return None
        else:
            values = ["&{EMPTY}"]
        scope = "LOCAL" if self.explicit_local else None
        return Var.from_params(name=var_name, value=values, indent=indent, scope=scope)
