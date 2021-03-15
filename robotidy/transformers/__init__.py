"""
Transformers are classes used to transform passed Robot Framework code model.

To create your own transformer you need to create file with the same name as your transformer class. Your class
need to inherit from ``ModelTransformer`` or ``ast.NodeTransformer`` class. Finally put name of your transformer in
``TRANSFORMERS`` variable in this file.
"""
from robot.utils.importer import Importer

TRANSFORMERS = frozenset((
    'AssignmentNormalizer',
    'DiscardEmptySections',
    'NormalizeNewLines',
    'NormalizeSectionHeaderName',
    'NormalizeSettingName',
    'ReplaceRunKeywordIf',
    'SplitTooLongLine'
))


def load_transformers(allowed_transformers):
    """ Dynamically load all classes from this file with attribute `name` defined in allowed_transformers """
    if allowed_transformers:
        loaded_transformers = dict()
        for name, args in allowed_transformers:
            name = f'robotidy.transformers.{name}' if name in TRANSFORMERS else name
            loaded_transformers[name] = Importer().import_class_or_module(
                name,
                instantiate_with_args=args
            )
        return loaded_transformers
    else:
        return {name: Importer().import_class_or_module(f'robotidy.transformers.{name}', instantiate_with_args=())
                for name in TRANSFORMERS}
