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
            "skip_settings",
            "skip_arguments",
            "skip_setup",
            "skip_teardown",
            "skip_timeout",
            "skip_template",
            "skip_return_statement",
            "skip_tags",
        }
    )

    def __init__(
        self,
        documentation: bool = False,
        return_values: bool = False,
        keyword_call: Optional[List] = None,
        keyword_call_pattern: Optional[List] = None,
        settings: bool = False,
        arguments: bool = False,
        setup: bool = False,
        teardown: bool = False,
        timeout: bool = False,
        template: bool = False,
        return_statement: bool = False,
        tags: bool = False,
    ):
        self.documentation = documentation
        self.return_values = return_values
        self.keyword_call: List = keyword_call if keyword_call else []
        self.keyword_call_pattern: List = keyword_call_pattern if keyword_call_pattern else []
        self.settings = settings
        self.arguments = arguments
        self.setup = setup
        self.teardown = teardown
        self.timeout = timeout
        self.template = template
        self.return_statement = return_statement
        self.tags = tags

    @classmethod
    def from_str_config(
        cls,
        global_skip,
        documentation: Optional[str] = None,
        return_values: Optional[str] = None,
        keyword_call: Optional[str] = None,
        keyword_call_pattern: Optional[str] = None,
        settings: Optional[str] = None,
        arguments: Optional[str] = None,
        setup: Optional[str] = None,
        teardown: Optional[str] = None,
        timeout: Optional[str] = None,
        template: Optional[str] = None,
        return_statement: Optional[str] = None,
        tags: Optional[str] = None,
    ):
        """Integrate local and global configurations into one (local takes precedence if specified)."""
        # FIXME DRY
        documentation = join_optional_flag_with_global(documentation, global_skip.documentation)
        return_values = join_optional_flag_with_global(return_values, global_skip.return_values)
        settings = join_optional_flag_with_global(settings, global_skip.settings)
        arguments = join_optional_flag_with_global(arguments, global_skip.arguments)
        setup = join_optional_flag_with_global(setup, global_skip.setup)
        teardown = join_optional_flag_with_global(teardown, global_skip.teardown)
        timeout = join_optional_flag_with_global(timeout, global_skip.timeout)
        template = join_optional_flag_with_global(template, global_skip.template)
        return_statement = join_optional_flag_with_global(return_statement, global_skip.return_statement)
        tags = join_optional_flag_with_global(tags, global_skip.tags)
        keyword_call = join_optional_list_with_global(keyword_call, global_skip.keyword_call)
        keyword_call_pattern = join_optional_list_with_global(keyword_call_pattern, global_skip.keyword_call_pattern)
        return cls(
            documentation=documentation,
            return_values=return_values,
            keyword_call=keyword_call,
            keyword_call_pattern=keyword_call_pattern,
            settings=settings,
            arguments=arguments,
            setup=setup,
            teardown=teardown,
            timeout=timeout,
            template=template,
            return_statement=return_statement,
            tags=tags,
        )

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Skip:
    """Defines global skip conditions for each transformer."""

    def __init__(self, skip_config: SkipConfig):
        self.return_values = skip_config.return_values
        self.documentation = skip_config.documentation
        self.keyword_call_names = {normalize_name(name) for name in skip_config.keyword_call}
        self.keyword_call_pattern = {validate_regex(pattern) for pattern in skip_config.keyword_call_pattern}
        self.any_keword_call = self.check_any_keyword_call()
        self.skip_settings = self.parse_skip_settings(skip_config)

    @staticmethod
    def parse_skip_settings(skip_config):
        settings = {"settings", "arguments", "setup", "teardown", "timeout", "template", "return_statement", "tags"}
        skip_settings = set()
        for setting in settings:
            if getattr(skip_config, setting):
                skip_settings.add(setting)
        return skip_settings

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

    def setting(self, name):
        if not self.skip_settings:
            return False
        if "settings" in self.skip_settings:
            return True
        return name.lower() in self.skip_settings


documentation_option = click.option(
    "--skip-documentation",
    is_flag=True,
    help="Skip formatting of documentation",
)
return_values_option = click.option(
    "--skip-return-values",
    is_flag=True,
    help="Skip formatting of return values",
)
keyword_call_option = click.option(
    "--skip-keyword-call",
    type=str,
    multiple=True,
    help="Keyword call name that should not be formatted",
)
keyword_call_pattern_option = click.option(
    "--skip-keyword-call-pattern",
    type=str,
    multiple=True,
    help="Keyword call name pattern that should not be formatted",
)
settings_option = click.option("--skip-settings", is_flag=True, help="Skip formatting of settings")
arguments_option = click.option(
    "--skip-arguments",
    is_flag=True,
    help="Skip formatting of arguments",
)
setup_option = click.option(
    "--skip-setup",
    is_flag=True,
    help="Skip formatting of setup",
)
teardown_option = click.option(
    "--skip-teardown",
    is_flag=True,
    help="Skip formatting of teardown",
)
timeout_option = click.option(
    "--skip-timeout",
    is_flag=True,
    help="Skip formatting of timeout",
)
template_option = click.option(
    "--skip-template",
    is_flag=True,
    help="Skip formatting of template",
)
return_option = click.option(
    "--skip-return",
    is_flag=True,
    help="Skip formatting of return statement",
)
tags_option = click.option(
    "--skip-tags",
    is_flag=True,
    help="Skip formatting of tags",
)
option_group = {
    "name": "Skip formatting",
    "options": [
        "--skip-documentation",
        "--skip-return-values",
        "--skip-keyword-call",
        "--skip-keyword-call-pattern",
        "--skip-settings",
        "--skip-arguments",
        "--skip-setup",
        "--skip-teardown",
        "--skip-timeout",
        "--skip-template",
        "--skip-return",
        "--skip-tags",
    ],
}
