"""
Transformers are classes used to transform passed Robot Framework code model.
You can create your own transformer class if you follow those rules:
    - inherit from `ModelTransformer` class
    - add `@transformer` class decorator

Classes that do not met all of those two conditions will not be loaded into `robotidy` as transformers.
Thanks for that you can use it to create common classes / helper methods:

    class NotATransformer(ModelTransformer):
        pass

Transformers can have parameters configurable from cli or config files. To create them provide
function for parsing its value from `str` and decorate it with `@configurable`:

    @configurable
    def some_value(self, value: str):
        ''' configurable property with name `some_value`. Parse and return expected value to save it '''
        return int(value) + 1

You can access this parameter by name of parsing function - `self.some_value`. You can initialize it in two ways:
    - in __init__ - but the value used will be passed through parsing function
    - as `default` argument to configurable decorator: `@configurable(default=10)

"""
import inspect
import sys

from robot.parsing import ModelTransformer
from robot.parsing.model.statements import EmptyLine, Comment
from robot.parsing.model.blocks import CommentSection

from robotidy.decorators import transformer, configurable


def load_transformers(allowed_transformers):
    """ Dynamically load all classess from this file with attribute `name` defined in allowed_transformers """
    transformer_classes = {}
    classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    for transfomer_class in classes:
        if not allowed_transformers:
            if getattr(transfomer_class[1], 'is_transformer', False):
                transformer_classes[transfomer_class[1].__name__] = transfomer_class[1]()
        elif transfomer_class[1].__name__ in allowed_transformers:
            transformer_classes[transfomer_class[1].__name__] = transfomer_class[1]()
    return transformer_classes


@transformer
class DiscardEmptySections(ModelTransformer):
    @configurable(default=False)
    def allow_only_comments(self, value):
        """ If True then sections only with comments are not considered as empty """
        return bool(value)

    def check_if_empty(self, node):
        anything_but = EmptyLine if self.allow_only_comments or isinstance(node, CommentSection) else (Comment, EmptyLine)
        if all(isinstance(child, anything_but) for child in node.body):
            return None
        return node

    def visit_SettingSection(self, node):  # noqa
        return self.check_if_empty(node)

    def visit_VariableSection(self, node):  # noqa
        return self.check_if_empty(node)

    def visit_TestCaseSection(self, node):  # noqa
        return self.check_if_empty(node)

    def visit_KeywordSection(self, node):  # noqa
        return self.check_if_empty(node)

    def visit_CommentSection(self, node):  # noqa
        return self.check_if_empty(node)
