import inspect
import sys

from robot.parsing import ModelTransformer

from robotidy.decorators import transformer, configurable


def load_transformers(allowed_transformers):
    """ Dynamically load all classess from this file with attribute `name` defined in allowed_transformers """
    transformer_classes = {}
    classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    for transfomer_class in classes:
        if transfomer_class[1].__name__ in allowed_transformers:
            transformer_classes[transfomer_class[1].__name__] = transfomer_class[1]()
    return transformer_classes


def load_transfomers_names():
    transformer_names = []
    classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    for transfomer_class in classes:
        if getattr(transfomer_class[1], 'is_transformer', False):
            transformer_names.append(transfomer_class[1].__name__)
    return transformer_names


@transformer
class DummyTransformer(ModelTransformer):
    def __init__(self):
        self.some_value = 10

    @configurable
    def some_value(self, value):
        return int(value) + 1


@transformer
class AnotherTransformer(ModelTransformer):
    def __init__(self):
        self.other_value = 5

    @configurable
    def other_value(self, value):
        value = value * 10
        return value


class NotATransformer(ModelTransformer):
    pass
