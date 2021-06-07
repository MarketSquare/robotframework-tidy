from collections import defaultdict

import click
from robot.api.parsing import (
    ModelTransformer,
    Comment,
    Token,
    EmptyLine,
    LibraryImport
)
from robot.libraries import STDLIBS


class OrderSettingsSection(ModelTransformer):
    """
    Order settings inside *** Settings *** section.

    Settings are grouped in following groups:
      - documentation (Documentation, Metadata),
      - imports (Library, Resource, Variables),
      - settings (Suite Setup and Teardown, Test Setup and Teardown, Test Timeout, Test Template),
      - tags (Force Tags, Default Tags)

    Then ordered by groups (according to ``group_order = documentation,imports,settings,tags`` order). Every
    group is separated by ``new_lines_between_groups = 1`` new lines.
    Settings are grouped inside group. Default order can be modified through following parameters:
      - ``documentation_order = documentation,metadata``
      - ``imports_order = library,resource,variables``
      - ``settings_order = suite_setup,suite_teardown,test_setup,test_teardown,test_timeout,test_template``

    Setting names omitted from custom order will be removed from the file. In following example we are missing metadata
    therefore all metadata will be removed::

        robotidy --configure OrderSettingsSection:documentation_order=documentation

    Libraries are grouped into built in libraries and custom libraries.
    Parsing errors (such as Resources instead of Resource, duplicated settings) are moved to the end of section.
    """
    def __init__(self, new_lines_between_groups: int = 1, group_order: str = None, documentation_order: str = None,
                 imports_order: str = None, settings_order: str = None, tags_order: str = None):
        self.last_section = None
        self.new_lines_between_groups = new_lines_between_groups
        self.group_order = self.parse_group_order(group_order)
        self.documentation_order = self.parse_order_in_group(
            documentation_order,
            (
                Token.DOCUMENTATION,
                Token.METADATA
            ),
            {
                'documentation': Token.DOCUMENTATION,
                'metadata': Token.METADATA
            }
        )
        self.imports_order = self.parse_order_in_group(
            imports_order,
            (
                Token.LIBRARY,
                Token.RESOURCE,
                Token.VARIABLES
            ),
            {
                'library': Token.LIBRARY,
                'resource': Token.RESOURCE,
                'variables': Token.VARIABLES
            }
        )
        self.settings_order = self.parse_order_in_group(
            settings_order,
            (
                Token.SUITE_SETUP,
                Token.SUITE_TEARDOWN,
                Token.TEST_SETUP,
                Token.TEST_TEARDOWN,
                Token.TEST_TIMEOUT,
                Token.TEST_TEMPLATE
            ),
            {
                'suite_setup': Token.SUITE_SETUP,
                'suite_teardown': Token.SUITE_TEARDOWN,
                'test_setup': Token.TEST_SETUP,
                'test_teardown': Token.TEST_TEARDOWN,
                'test_timeout': Token.TEST_TIMEOUT,
                'test_template': Token.TEST_TEMPLATE
            }
        )
        self.tags_order = self.parse_order_in_group(
            tags_order,
            (
                Token.FORCE_TAGS,
                Token.DEFAULT_TAGS
            ),
            {
                'force_tags': Token.FORCE_TAGS,
                'default_tags': Token.DEFAULT_TAGS
            }
        )

    @staticmethod
    def parse_group_order(order):
        default = (
            'documentation',
            'imports',
            'settings',
            'tags'
        )
        if order is None:
            return default
        if not order:
            return []
        splitted = order.lower().split(',')
        if any(split not in default for split in splitted):
            raise click.BadOptionUsage(
                option_name='transform',
                message=f"Invalid configurable value: '{order}' for group_order for OrderSettingsSection transformer."
                        f" Custom order should be provided in comma separated list with valid group names:\n{default}"
            )
        return splitted

    @staticmethod
    def parse_order_in_group(order, default, mapping):
        if order is None:
            return default
        if not order:
            return []
        splitted = order.lower().split(',')
        try:
            return [mapping[split] for split in splitted]
        except KeyError:
            raise click.BadOptionUsage(
                option_name='transform',
                message=f"Invalid configurable value: '{order}' for order for OrderSettingsSection transformer."
                        f" Custom order should be provided in comma separated list with valid group names:\n"
                        f"{sorted(mapping.keys())}")

    def visit_File(self, node):  # noqa
        self.last_section = node.sections[-1] if node.sections else None
        return self.generic_visit(node)

    def visit_SettingSection(self, node):  # noqa
        if not node.body:
            return
        if node is self.last_section and not isinstance(node.body[-1], EmptyLine):
            node.body[-1] = self.fix_eol(node.body[-1])
        comments, errors = [], []
        groups = defaultdict(list)
        for child in node.body:
            child_type = getattr(child, 'type', None)
            if isinstance(child, Comment):
                comments.append(child)
            elif child_type in self.documentation_order:
                groups['documentation'].append((comments, child))
                comments = []
            elif child_type in self.imports_order:
                groups['imports'].append((comments, child))
                comments = []
            elif child_type in self.settings_order:
                groups['settings'].append((comments, child))
                comments = []
            elif child_type in self.tags_order:
                groups['tags'].append((comments, child))
                comments = []
            elif not isinstance(child, EmptyLine):
                errors.append(child)

        group_map = {
            'documentation': self.documentation_order,
            'imports': self.imports_order,
            'settings': self.settings_order,
            'tags': self.tags_order
        }

        new_body = []
        empty_line = EmptyLine.from_params(eol='\n')
        order_of_groups = [group for group in self.group_order if group in groups]
        last_index = len(order_of_groups) - 1
        for index, group in enumerate(order_of_groups):
            unordered = groups[group]
            if group == 'imports':
                unordered = self.sort_builtin_libs(unordered)
            order = group_map[group]
            for token_type in order:
                for comment_lines, child in unordered:
                    if child.type == token_type:
                        new_body.extend(comment_lines)
                        new_body.append(child)
            if index != last_index:
                new_body.extend([empty_line] * self.new_lines_between_groups)

        # not recognized headers, parsing errors like Resources instead of Resource
        if errors:
            new_body.extend([empty_line] * self.new_lines_between_groups)
            new_body.extend(errors)
        new_body.extend(comments)
        if node is not self.last_section:
            new_body.append(empty_line)
        node.body = new_body
        return node

    @staticmethod
    def fix_eol(node):
        if not getattr(node, 'tokens', None):
            return node
        if getattr(node.tokens[-1], 'type', None) != Token.EOL:
            return node
        node.tokens = list(node.tokens[:-1]) + [Token(Token.EOL, '\n')]
        return node

    @staticmethod
    def sort_builtin_libs(statements):
        before, after = [], []
        for comments, statement in statements:
            if isinstance(statement, LibraryImport) and statement.name and statement.name in STDLIBS:
                before.append((comments, statement))
            else:
                after.append((comments, statement))
        before = sorted(before, key=lambda x: x[1].name)
        return before + after
