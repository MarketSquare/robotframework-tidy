import inspect
import sys

from robot.parsing import ModelTransformer


def load_transformers(modes):
    """ Dynamically load all classess from this file with attribute `name` defined in modes """
    transfomers = []
    classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    for transfomer_class in classes:
        transfomer = transfomer_class[1]()
        if getattr(transfomer, 'name', None) in modes:
            transfomers.append(transfomer)
    return transfomers


def load_transfomers_names():
    transfomers = []
    classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    for transfomer_class in classes:
        if hasattr(transfomer_class[1], 'name'):
            transfomers.append(transfomer_class[1].name)
    return transfomers


class DummyTransformer(ModelTransformer):
    name = 'dummy_transformer'

    def __str__(self):
        return self.name


class AnotherTransfomer(ModelTransformer):
    name = 'another_transformer'

    def __str__(self):
        return self.name
