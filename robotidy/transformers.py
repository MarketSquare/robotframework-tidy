import inspect
import sys

from robot.parsing import ModelTransformer


def load_transformers(modes):
    """ Dynamically load all classess from this file with attribute `name` defined in modes """
    transfomers = []
    classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    for transfomer_class in classes:
        if transfomer_class[1].__name__ in modes:
            transfomers.append(transfomer_class[1]())
    return transfomers


def load_transfomers_names():
    transfomers = []
    classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    for transfomer_class in classes:
        if issubclass(transfomer_class[1], ModelTransformer) and transfomer_class[1].__name__ != 'ModelTransformer':
            transfomers.append(transfomer_class[1].__name__)
    return transfomers


class DummyTransformer(ModelTransformer):
    pass


class AnotherTransformer(ModelTransformer):
    pass
