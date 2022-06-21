import re
from typing import List, Optional, Pattern

import click

from robotidy.utils import normalize_name


def parse_csv(value):
    if not value:
        return []
    return [val for val in value.split(",")]


def str_to_bool(value):
    return value.lower() == "true"


def validate_regex(value: str) -> Optional[Pattern]:
    try:
        return re.compile(value)
    except re.error:
        raise ValueError(f"'{value}' is not a valid regular expression.") from None


def join_optional_list_with_global(local: Optional[str], global_list: List):
    if local is None:
        return [elem for elem in global_list]
    return parse_csv(local) + global_list


def join_optional_flag_with_global(local: Optional[str], global_flag: bool):
    if local is None:
        return global_flag
    return str_to_bool(local)


class SkipConfig:
    """Skip configuration (global and for each transformer)."""

    # Following names will be taken from transformer config and provided to Skip class instead
    HANDLES = frozenset(
        {
            "skip_documentation",
            "skip_return_values",
            "skip_keyword_call",
            "skip_keyword_call_pattern",
        }
    )

    def __init__(
        self,
        documentation: bool = False,
        return_values: bool = False,
        keyword_call: Optional[List] = None,
        keyword_call_pattern: Optional[List] = None,
    ):
        self.documentation = documentation
        self.return_values = return_values
        self.keyword_call: List = keyword_call if keyword_call else []
        self.keyword_call_pattern: List = keyword_call_pattern if keyword_call_pattern else []

    @classmethod
    def from_str_config(
        cls,
        global_skip,
        documentation: Optional[str] = None,
        return_values: Optional[str] = None,
        keyword_call: Optional[str] = None,
        keyword_call_pattern: Optional[str] = None,
    ):
        """Integrate local and global configurations into one (local takes precedence if specified)."""
        documentation = join_optional_flag_with_global(documentation, global_skip.documentation)
        return_values = join_optional_flag_with_global(return_values, global_skip.return_values)
        keyword_call = join_optional_list_with_global(keyword_call, global_skip.keyword_call)
        keyword_call_pattern = join_optional_list_with_global(keyword_call_pattern, global_skip.keyword_call_pattern)
        return cls(
            documentation=documentation,
            return_values=return_values,
            keyword_call=keyword_call,
            keyword_call_pattern=keyword_call_pattern,
        )

    def __eq__(self, other):
        return (
            self.documentation == other.documentation
            and self.return_values == other.return_values
            and self.keyword_call == other.keyword_call
            and self.keyword_call_pattern == other.keyword_call_pattern
        )


class Skip:
    """Defines global skip conditions for each transformer."""

    def __init__(self, skip_config: SkipConfig):
        self.return_values = skip_config.return_values
        self.documentation = skip_config.documentation
        self.keyword_call_names = {normalize_name(name) for name in skip_config.keyword_call}
        self.keyword_call_pattern = {validate_regex(pattern) for pattern in skip_config.keyword_call_pattern}
        self.any_keword_call = self.check_any_keyword_call()

    def check_any_keyword_call(self):
        return self.keyword_call_names or self.keyword_call_pattern

    def keyword_call(self, node):
        if not getattr(node, "keyword", None) or not self.any_keword_call:
            return False
        normalized = normalize_name(node.keyword)
        if normalized in self.keyword_call_names:
            return True
        for pattern in self.keyword_call_pattern:
            if pattern.search(node.keyword):
                return True
        return False


documentation_option = click.option("--skip-documentation", is_flag=True, help="Skip formatting of documentation")
return_values_option = click.option("--skip-return-values", is_flag=True, help="Skip formatting of return values")
keyword_call_option = click.option(
    "--skip-keyword-call", type=str, multiple=True, help="Keyword call name that should not be formatted"
)
keyword_call_pattern_option = click.option(
    "--skip-keyword-call-pattern",
    type=str,
    multiple=True,
    help="Keyword call name pattern that should not be formatted",
)
