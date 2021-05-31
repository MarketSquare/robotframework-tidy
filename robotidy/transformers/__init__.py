"""
Transformers are classes used to transform passed Robot Framework code model.

To create your own transformer you need to create file with the same name as your transformer class. Your class
need to inherit from ``ModelTransformer`` or ``ast.NodeTransformer`` class. Finally put name of your transformer in
``TRANSFORMERS`` variable in this file.

If you don't want to run your transformer by default and only when calling robotidy with --transform YourTransformer
then add ``ENABLED = False`` class attribute inside.
"""
from robot.utils.importer import Importer

TRANSFORMERS = frozenset((
    'AlignSettingsSection',
    'AlignVariablesSection',
    'AssignmentNormalizer',
    'DiscardEmptySections',
    'NormalizeNewLines',
    'NormalizeSectionHeaderName',
    'NormalizeSettingName',
    'ReplaceRunKeywordIf',
    'SplitTooLongLine',
    'SmartSortKeywords'
))


def load_transformers(allowed_transformers):
    """ Dynamically load all classes from this file with attribute `name` defined in allowed_transformers """
    loaded_transformers = dict()
    if allowed_transformers:

        for name, args in allowed_transformers:
            import_name = f'robotidy.transformers.{name}' if name in TRANSFORMERS else name
            loaded_transformers[name] = Importer().import_class_or_module(
                import_name,
                instantiate_with_args=args
            )
    else:
        for name in TRANSFORMERS:
            imported_class = Importer().import_class_or_module(f'robotidy.transformers.{name}', instantiate_with_args=())
            if getattr(imported_class, 'ENABLED', True):
                loaded_transformers[name] = imported_class
    return loaded_transformers