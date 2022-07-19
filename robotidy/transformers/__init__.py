"""
Transformers are classes used to transform passed Robot Framework code model.

To create your own transformer you need to create file with the same name as your transformer class. Your class
need to inherit from ``ModelTransformer`` or ``ast.NodeTransformer`` class. Finally put name of your transformer in
``TRANSFORMERS`` variable in this file.

If you don't want to run your transformer by default and only when calling robotidy with --transform YourTransformer
then add ``ENABLED = False`` class attribute inside.
"""
import copy
from itertools import chain
from typing import Dict, Optional

try:
    import rich_click as click
except ImportError:
    import click

from robot.api.parsing import ModelTransformer
from robot.errors import DataError
from robot.utils.importer import Importer

from robotidy.disablers import Skip, SkipConfig
from robotidy.exceptions import ImportTransformerError, InvalidParameterError, InvalidParameterFormatError
from robotidy.utils import ROBOT_VERSION, RecommendationFinder

TRANSFORMERS = [
    "AddMissingEnd",
    "NormalizeSeparators",
    "DiscardEmptySections",
    "MergeAndOrderSections",
    "RemoveEmptySettings",
    "NormalizeAssignments",
    "OrderSettings",
    "OrderSettingsSection",
    "NormalizeTags",
    "OrderTags",
    "IndentNestedKeywords",
    "AlignSettingsSection",
    "AlignVariablesSection",
    "AlignTemplatedTestCases",
    "AlignTestCasesSection",
    "AlignKeywordsSection",
    "NormalizeNewLines",
    "NormalizeSectionHeaderName",
    "NormalizeSettingName",
    "ReplaceRunKeywordIf",
    "SplitTooLongLine",
    "SmartSortKeywords",
    "RenameTestCases",
    "RenameKeywords",
    "ReplaceReturns",
    "ReplaceBreakContinue",
    "InlineIf",
]


IMPORTER = Importer()


class Transformer(ModelTransformer):
    def __init__(self, skip: Optional[Skip] = None):
        self.formatting_config = None  # to make lint happy (we're injecting the configs)
        self.transformers: Dict = dict()
        self.disablers = None
        self.skip = skip


def import_transformer(name, args, skip):
    short_name = name.split(".")[-1]
    try:
        imported_class = IMPORTER.import_class_or_module(name)
        spec = IMPORTER._get_arg_spec(imported_class)
        handles_skip = getattr(imported_class, "HANDLES_SKIP", {})
        positional, named = resolve_args(short_name, spec, args, skip, handles_skip=handles_skip)
    except DataError:
        similar_finder = RecommendationFinder()
        similar = similar_finder.find_similar(short_name, TRANSFORMERS)
        raise ImportTransformerError(
            f"Importing transformer '{short_name}' failed. "
            f"Verify if correct name or configuration was provided.{similar}"
        ) from None
    return imported_class(*positional, **named)


def split_args_to_class_and_skip(args):
    filtered_args = []
    skip_args = {}
    for arg, value in args.items():
        if arg == "enabled":
            continue
        if arg in SkipConfig.HANDLES:
            skip_args[arg.replace("skip_", "")] = value
        else:
            filtered_args.append(f"{arg}={value}")
    return filtered_args, skip_args


def assert_class_accepts_arguments(transformer, args, spec):
    if args and not spec.argument_names:
        raise InvalidParameterError(transformer, " This transformer does not accept arguments but they were provided.")


def resolve_argument_names(argument_names, handles_skip):
    """Get transformer argument names with resolved skip parameters."""
    new_args = ["enable"]
    if "skip" not in argument_names:
        return new_args + argument_names
    new_args.extend([arg for arg in argument_names if arg != "skip"])
    new_args.extend(arg for arg in sorted(handles_skip) if arg not in new_args)
    return new_args


def assert_handled_arguments(transformer, args, spec, handles_skip):
    """Check if provided arguments are handled by given transformer.
    Raises InvalidParameterError if arguments does not match."""
    arg_names = [arg.split("=")[0] for arg in args]
    for arg in arg_names:
        # it's fine to only check for first non-matching parameter
        argument_names = resolve_argument_names(spec.argument_names, handles_skip)
        if arg not in argument_names:
            similar_finder = RecommendationFinder()
            similar = similar_finder.find_similar(arg, argument_names)
            if not similar:
                arg_names = "\n    " + "\n    ".join(argument_names)
                similar = f" This transformer accepts following arguments:{arg_names}"
            raise InvalidParameterError(transformer, similar) from None


def get_skip_args_from_spec(spec):
    """
    It is possible to override default skip value (such as skip_documentation
    from False to True in AlignKeywordsSection).
    This method iterate over spec and finds such overrides.
    """
    defaults = dict()
    for arg, value in spec.defaults.items():
        if arg in SkipConfig.HANDLES:
            defaults[arg.replace("skip_", "")] = value
    return defaults


def get_skip_class(spec, skip_args, global_skip):
    defaults = get_skip_args_from_spec(spec)
    defaults.update(skip_args)
    if global_skip is None:
        skip_config = SkipConfig()
    else:
        skip_config = copy.deepcopy(global_skip)
    skip_config.update_with_str_config(**defaults)
    return Skip(skip_config)


def resolve_args(transformer, spec, args, global_skip, handles_skip):
    """
    Use class definition to identify which arguments from configuration
    should be used to invoke it.

    First we're splitting arguments into class arguments and skip arguments
    (those that are handled by Skip class).
    Class arguments are resolved with their definition and if class accepts
    "skip" parameter the Skip class will be also added to class arguments.
    """
    args, skip_args = split_args_to_class_and_skip(args)
    assert_class_accepts_arguments(transformer, args, spec)
    assert_handled_arguments(transformer, args, spec, handles_skip)
    try:
        positional, named = spec.resolve(args)
        named = dict(named)
        if "skip" in spec.argument_names:
            named["skip"] = get_skip_class(spec, skip_args, global_skip)
        return positional, named
    except ValueError as err:
        raise InvalidParameterError(transformer, f" {err}") from None


def resolve_core_import_path(name):
    """Append import path if transformer is core Robotidy transformer."""
    return f"robotidy.transformers.{name}" if name in TRANSFORMERS else name


def load_transformer(name, args, skip):
    if not args.get("enabled", True):
        return None
    import_name = resolve_core_import_path(name)
    return import_transformer(import_name, args, skip)


def join_configs(args, config):
    # args are from --transform Name:param=value and config is from --configure
    temp_args = {}
    for arg in chain(args, config):
        param, value = arg.split("=", maxsplit=1)
        if param == "enabled":
            temp_args[param] = value.lower() == "true"
        else:
            temp_args[param] = value
    return temp_args


def get_args(transformer, allowed_mapped, config):
    try:
        return join_configs(allowed_mapped.get(transformer, ()), config.get(transformer, ()))
    except ValueError:
        raise InvalidParameterFormatError(transformer) from None


def validate_config(config, allowed_mapped):
    for transformer in config:
        if transformer in allowed_mapped or transformer in TRANSFORMERS:
            continue
        similar_finder = RecommendationFinder()
        similar = similar_finder.find_similar(transformer, TRANSFORMERS + list(allowed_mapped.keys()))
        raise ImportTransformerError(
            f"Configuring transformer '{transformer}' failed. " f"Verify if correct name was provided.{similar}"
        ) from None


def can_run_in_robot_version(transformer, overwritten, target_version):
    if not hasattr(transformer, "MIN_VERSION"):
        return True
    if target_version >= transformer.MIN_VERSION:
        return True
    if overwritten:
        # --transform TransformerDisabledInVersion or --configure TransformerDisabledInVersion:enabled=True
        if target_version == ROBOT_VERSION.major:
            click.echo(
                f"{transformer.__class__.__name__} transformer requires Robot Framework {transformer.MIN_VERSION}.* "
                f"version but you have {ROBOT_VERSION} installed. "
                f"Upgrade installed Robot Framework if you want to use this transformer."
            )
        else:
            click.echo(
                f"{transformer.__class__.__name__} transformer requires Robot Framework {transformer.MIN_VERSION}.* "
                f"version but you set --target-version rf{target_version}. "
                f"Set --target-version to rf{transformer.MIN_VERSION} or do not forcefully enable this transformer "
                f"with --transform / enable parameter."
            )
    return False


def load_transformers(
    allowed_transformers,
    config,
    target_version,
    skip=None,
    allow_disabled=False,
    force_order=False,
    allow_version_mismatch=True,
):
    """Dynamically load all classes from this file with attribute `name` defined in allowed_transformers"""
    loaded_transformers = []
    allowed_mapped = {name: args for name, args in allowed_transformers} if allowed_transformers else {}
    validate_config(config, allowed_mapped)
    if not force_order:
        for name in TRANSFORMERS:
            if not allowed_mapped or name in allowed_mapped:
                args = get_args(name, allowed_mapped, config)
                imported_class = load_transformer(name, args, skip)
                if imported_class is None:
                    continue
                enabled = getattr(imported_class, "ENABLED", True) or args.get("enabled", False)
                if allowed_mapped or allow_disabled or enabled:
                    overwritten = name in allowed_mapped or args.get("enabled", False)
                    if can_run_in_robot_version(imported_class, overwritten=overwritten, target_version=target_version):
                        loaded_transformers.append(imported_class)
                    elif allow_version_mismatch and allow_disabled:
                        setattr(imported_class, "ENABLED", False)
                        loaded_transformers.append(imported_class)
    for name in allowed_mapped:
        if force_order or name not in TRANSFORMERS:
            args = get_args(name, allowed_mapped, config)
            imported_class = load_transformer(name, args, skip)
            if imported_class is not None:
                if can_run_in_robot_version(imported_class, overwritten=True, target_version=target_version):
                    loaded_transformers.append(imported_class)
    return loaded_transformers
