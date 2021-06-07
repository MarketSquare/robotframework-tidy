import click
from robot.api.parsing import (
    ModelTransformer,
    Variable,
    Token
)


class OrderSettingsSection(ModelTransformer):
    """
    Order settings inside *** Settings *** section.

    """
    def __init__(self):
        self.group_order = (
            'documentation',
            'imports',
            'settings',
            'tags'
        )
        self.documentation_order = (
            Token.DOCUMENTATION,
            Token.METADATA
        )
        self.imports_order = (
            Token.LIBRARY,
            Token.RESOURCE,
            Token.VARIABLES
        )
        self.settings_order = (
            Token.SUITE_SETUP,
            Token.SUITE_TEARDOWN,
            Token.TEST_SETUP,
            Token.TEST_TEARDOWN,
            Token.TEST_TIMEOUT,
            Token.TEST_TEMPLATE
        )
        self.tags_order = (
            Token.FORCE_TAGS,
            Token.DEFAULT_TAGS
        )

    def visit_Sett