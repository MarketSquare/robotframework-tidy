import click
from robot.api.parsing import (
    ModelTransformer,
    EmptyLine,
    Token
)

from robotidy.decorators import check_start_end_line


class OrderSettings(ModelTransformer):
    """
    Order settings like [Arguments], [Setup], [Return] inside Keywords and Test Cases.

    Keyword settings [Documentation], [Tags], [Timeout], [Arguments] are put before keyword body and
    settings like [Teardown], [Return] are moved to the end of keyword::

       *** Keywords ***
        Keyword
            [Teardown]  Keyword
            [Return]  ${value}
            [Arguments]  ${arg}
            [Documentation]  this is
            ...    doc
            [Tags]  sanity
            Pass

    To::

       *** Keywords ***
        Keyword
            [Documentation]  this is
            ...    doc
            [Tags]  sanity
            [Arguments]  ${arg}
            Pass
            [Teardown]  Keyword
            [Return]  ${value}

    Test case settings [Documentation], [Tags], [Template], [Timeout], [Setup] are put before test case body and
    [Teardown] is moved to the end of test case.

    Default order can be changed using following parameters:
      - ``keyword_before = documentation,tags,timeout,arguments``
      - ``keyword_after = teardown,return``
      - ``test_before = documentation,tags,template,timeout,setup
      - ``test_after = teardown

    Not all settings names need to be passed to given parameter. Missing setting names are not ordered. Example::

        robotidy --configure OrderSettings:keyword_before=:keyword_after=

    It will order only test cases because all setting names for keywords are missing.

    Supports global formatting params: ``--startline`` and ``--endline``.
    """
    def __init__(self, keyword_before: str = None, keyword_after: str = None, test_before: str = None,
                 test_after: str = None):
        self.keyword_before, self.keyword_after, self.test_before, self.test_after = self.parse_order(
            keyword_before,
            keyword_after,
            test_before,
            test_after
        )
        self.keyword_settings = {
            *self.keyword_before,
            *self.keyword_after
        }
        self.test_settings = {
            *self.test_before,
            *self.test_after
        }

    @staticmethod
    def get_order(order, default, name_map):
        if order is None:
            return default
        if not order:
            return []
        splitted = order.lower().split(',')
        try:
            return [name_map[split] for split in splitted]
        except KeyError:
            raise click.BadOptionUsage(
                option_name='transform',
                message=f"Invalid configurable value: '{order}' for order for OrderSettings transformer."
                        f" Custom order should be provided in comma separated list with valid setting names:\n"
                        f"{sorted(name_map.keys())}")

    def parse_order(self, keword_before, keyword_after, test_before, test_after):
        keyword_order_before = (
            Token.DOCUMENTATION,
            Token.TAGS,
            Token.TIMEOUT,
            Token.ARGUMENTS,
        )
        keyword_order_after = (
            Token.TEARDOWN,
            Token.RETURN,
        )
        testcase_order_before = (
            Token.DOCUMENTATION,
            Token.TAGS,
            Token.TEMPLATE,
            Token.TIMEOUT,
            Token.SETUP
        )
        testcase_order_after = (
            Token.TEARDOWN,
        )
        keyword_map = {
            'documentation': Token.DOCUMENTATION,
            'tags': Token.TAGS,
            'timeout': Token.TIMEOUT,
            'arguments': Token.ARGUMENTS,
            'return': Token.RETURN,
            'teardown': Token.TEARDOWN
        }
        test_map = {
            'documentation': Token.DOCUMENTATION,
            'tags': Token.TAGS,
            'timeout': Token.TIMEOUT,
            'template': Token.TEMPLATE,
            'setup': Token.SETUP,
            'teardown': Token.TEARDOWN
        }
        return (self.get_order(keword_before, keyword_order_before, keyword_map),
                self.get_order(keyword_after, keyword_order_after, keyword_map),
                self.get_order(test_before, testcase_order_before, test_map),
                self.get_order(test_after, testcase_order_after, test_map))

    @check_start_end_line
    def visit_Keyword(self, node):  # noqa
        return self.order_settings(node, self.keyword_settings, self.keyword_before, self.keyword_after)

    @check_start_end_line
    def visit_TestCase(self, node):  # noqa
        return self.order_settings(node, self.test_settings, self.test_before, self.test_after)

    @staticmethod
    def order_settings(node, setting_types, before, after):
        if not node.body:
            return node
        settings = dict()
        rest = []
        new_body = []
        for child in node.body:
            if getattr(child, 'type', 'invalid') in setting_types:
                settings[child.type] = child
            else:
                rest.append(child)
        trailing_empty = []
        while rest and isinstance(rest[-1], EmptyLine):
            trailing_empty.append(rest.pop())
        for token_type in before:
            if token_type in settings:
                new_body.append(settings[token_type])
        new_body.extend(rest)
        for token_type in after:
            if token_type in settings:
                new_body.append(settings[token_type])
        new_body.extend(trailing_empty)
        node.body = new_body
        return node
