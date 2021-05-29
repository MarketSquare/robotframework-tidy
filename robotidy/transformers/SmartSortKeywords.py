from robot.api.parsing import ModelTransformer, EmptyLine
from robot.parsing.model.blocks import Keyword


class SmartSortKeywords(ModelTransformer):
    """
    Sort keywords in *** Keywords *** section.

    By default sortin is case insensitve, but keywords with leading underscore go to the bottom. Other underscores are
    treated as spaces.
    Empty lines (or lack of them) between keywords is preserved.

    Following code::
    *** Keywords ***
    _my secrete keyword
        Kw2

    My Keyword
        Kw1


    my_another_cool_keyword
    my another keyword
        Kw3

    Will be transformed to::
    *** Keywords ***
    my_another_cool_keyword

    my another keyword
        Kw3


    My Keyword
        Kw1
    _my secrete keyword
        Kw2

    Default behaviour could be changed using following parameters: ``case_insensitive``, ``ignore_leading_underscore``
    and ``ignore_other_underscore``.
    """
    ENABLED = False

    def __init__(self, case_insensitive=True, ignore_leading_underscore=False, ignore_other_underscore=True):
        self.ci = case_insensitive
        self.ilu = ignore_leading_underscore
        self.iou = ignore_other_underscore

    def visit_KeywordSection(self, node):  # noqa
        if not node.body:
            return node
        before, after = self.leave_only_keywords(node)
        empty_lines = self.pop_empty_lines(node)
        node.body.sort(key=self.sort_function)
        self.append_empty_lines(node, empty_lines)
        node.body = before + node.body + after
        return node

    @staticmethod
    def pop_empty_lines(node):
        all_empty = []
        for kw in node.body:
            kw_empty = []
            while kw.body and isinstance(kw.body[-1], EmptyLine):
                kw_empty.insert(0, kw.body.pop())
            all_empty.append(kw_empty)
        return all_empty

    @staticmethod
    def leave_only_keywords(node):
        before = []
        after = []
        while node.body and not isinstance(node.body[0], Keyword):
            before.append(node.body.pop(0))
        while node.body and not isinstance(node.body[-1], Keyword):
            after.append(node.body.pop(-1))
        return before, after

    def sort_function(self, kw):
        name = kw.name
        if self.ci:
            name = name.casefold().upper()  # to make sure that letters go before underscore
        if self.ilu:
            name = name.lstrip('_')
        if self.iou:
            index = len(name) - len(name.lstrip('_'))
            name = name[:index] + name[index:].replace("_", " ")
        return name

    @staticmethod
    def append_empty_lines(node, empty_lines):
        for kw, lines in zip(node.body, empty_lines):
            for line in lines:
                kw.body.append(line)
