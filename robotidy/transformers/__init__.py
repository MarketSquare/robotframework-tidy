"""
Transformers are classes used to transform passed Robot Framework code model.

To create your own transformer you need to create file with the same name as your transformer class. Your class
need to inherit from ``ModelTransformer`` or ``ast.NodeTransformer`` class. Finally put name of your transformer in
``TRANSFORMERS`` variable in this file.

If you don't want to run your transformer by default and only when calling robotidy with --transform YourTransformer
then add ``ENABLED = False`` class attribute inside.
"""
import copy
import pathlib
import textwrap
from itertools import chain
from typing import Dict, List, Optional

try:
    import rich_click as click
except ImportError:
    import click

from robot.api.parsing import ModelTransformer
from robot.errors import DataError
from robot.utils.importer import Importer

from robotidy.exceptions import ImportTransformerError, InvalidParameterError, InvalidParameterFormatError
from robotidy.skip import Skip, SkipConfig
from robotidy.utils import ROBOT_VERSION, RecommendationFinder, split_args_from_name_or_path

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
    "Translate",
    "BrowserDeprecateClick",
]


IMPORTER = Importer()


class TransformConfig:
    def __init__(self, config, force_include, custom_transformer, is_config):
        name, args = split_args_from_name_or_path(config.replace(" ", ""))
        self.name = name
        self.args = self.convert_args(args)
        self.force_include = force_include
        self.custom_transformer = custom_transformer
        self.is_config_only = is_config
        self.duplicate_reported = False

    def convert_args(self, args):
        """
        Convert list of param=value arguments to dictionary.
        """
        converted = dict()
        for arg in args:
            try:
                param, value = arg.split("=", maxsplit=1)
            except ValueError:
                raise InvalidParameterFormatError(self.name) from None
            if param == "enabled":
                converted[param] = value.lower() == "true"
            else:
                converted[param] = value
        return converted

    def join_transformer_configs(self, transformer_config: "TransformConfig"):
        """
        Join 2 configurations i.e. from --transform, --load-transformers or --config.
        """
        if self.force_include and transformer_config.force_include:
            if not self.duplicate_reported:
                click.echo(
                    f"Duplicated transformer '{self.name}' in the transform option. "
                    f"It will be run only once with the configuration from the last transform."
                )
                self.duplicate_reported = True
        self.is_config_only = self.is_config_only and transformer_config.is_config_only
        self.force_include = self.force_include or transformer_config.force_include
        self.custom_transformer = self.custom_transformer or transformer_config.custom_transformer
        self.join_args(transformer_config)

    def join_args(self, transformer_config: "TransformConfig"):
        self.args.update(transformer_config.args)


class TransformConfigMap:
    """
    Collection of all transformers and their configs.
    """

    def __init__(
        self,
        transform: List[TransformConfig],
        custom_transformers: List[TransformConfig],
        config: List[TransformConfig],
    ):
        self.force_included_only = False
        self.transformers: Dict[str, TransformConfig] = dict()
        for tr in chain(transform, custom_transformers, config):
            self.add_transformer(tr)

    def add_transformer(self, tr):
        if tr.force_include:
            self.force_included_only = True
        if tr.name in self.transformers:
            self.transformers[tr.name].join_transformer_configs(tr)
        else:
            self.transformers[tr.name] = tr

    def transformer_should_be_included(self, name: str) -> bool:
        """
        Check whether --transform option was used. If it was, check if transformer name was used with --transform.
        """
        if not self.force_included_only:
            return True
        return self.transformer_is_force_included(name)

    def transformer_is_force_included(self, name: str) -> bool:
        return name in self.transformers and self.transformers[name].force_include

    def transformer_was_forcefully_enabled(self, name: str) -> bool:
        if name not in self.transformers:
            return False
        return self.transformers[name].force_include or self.transformers[name].args.get("enabled", False)

    def update_with_defaults(self, defaults: List[str]):
        for default in defaults:
            if default in self.transformers:
                self.transformers[default].is_config_only = False
            else:
                self.transformers[default] = TransformConfig(default, False, False, False)

    def order_using_list(self, order: List[str]):
        temp_transformers: Dict[str, TransformConfig] = dict()
        for name in order:
            if name in self.transformers:
                temp_transformers[name] = self.transformers[name]
        for name, transformer in self.transformers.items():
            if name not in temp_transformers:
                temp_transformers[name] = transformer
        self.transformers = temp_transformers

    def validate_config_names(self):
        """
        Assert that all --configure NAME are either defaults or from --transform/--load-transformer.
        Otherwise raise an error with similar names.
        """
        for transf_name, transformer in self.transformers.items():
            if not transformer.is_config_only:
                continue
            similar_finder = RecommendationFinder()
            transformer_names = [name for name, transf in self.transformers.items() if not transf.is_config_only]
            similar = similar_finder.find_similar(transf_name, transformer_names)
            raise ImportTransformerError(
                f"Configuring transformer '{transf_name}' failed. " f"Verify if correct name was provided.{similar}"
            ) from None


class TransformConfigParameter(click.ParamType):
    """
    Click parameter that holds the name of the transformer and optional configuration.
    """

    name = "transform"

    def convert(self, value, param, ctx):
        force_included = param.name == "transform"
        custom_transformer = param.name == "custom_transformers"
        is_config = param.name == "configure"
        return TransformConfig(
            value, force_include=force_included, custom_transformer=custom_transformer, is_config=is_config
        )


class TransformerParameter:
    def __init__(self, name, default_value):
        self.name = name
        self.value = default_value

    def __str__(self):
        if self.value is not None and str(self.value) != "":
            return f"{self.name} : {self.value}"
        return self.name


class TransformerContainer:
    """
    Stub for transformer container class that holds the transformer instance and its metadata.
    """

    def __init__(self, instance, argument_names, spec):
        self.instance = instance
        self.name = instance.__class__.__name__
        self.enabled_by_default = getattr(instance, "ENABLED", True)
        self.parameters = self.get_parameters(argument_names, spec)

    def get_parameters(self, argument_names, spec):
        params = []
        for arg in argument_names:
            if arg == "enabled":
                default = self.enabled_by_default
            else:
                default = spec.defaults.get(arg, None)
            params.append(TransformerParameter(arg, default))
        return params

    def __str__(self):
        s = f"## Transformer {self.name}\n" + textwrap.dedent(self.instance.__doc__)
        if self.parameters:
            s += "\nSupported parameters:\n  - " + "\n - ".join(str(param) for param in self.parameters) + "\n"
        s += f"\nSee <https://robotidy.readthedocs.io/en/latest/transformers/{self.name}.html> for more examples."
        return s


class Transformer(ModelTransformer):
    def __init__(self, skip: Optional[Skip] = None):
        self.formatting_config = None  # to make lint happy (we're injecting the configs)
        self.languages = None
        self.transformers: Dict = dict()
        self.disablers = None
        self.skip = skip


def get_transformer_short_name(name):
    """Removes module path or file extension for better printing the errors."""
    if name.endswith(".py"):
        return name.split(".")[-2]
    return name.split(".")[-1]


def get_absolute_path_to_transformer(name, short_name):
    """
    If the transformer is not default one, try to get absolute path to transformer to make it easier to import it.
    """
    if short_name in TRANSFORMERS:
        return name
    if pathlib.Path(name).exists():
        return pathlib.Path(name).resolve()
    return name


def import_transformer(name, args, skip):
    short_name = get_transformer_short_name(name)
    name = get_absolute_path_to_transformer(name, short_name)
    try:
        imported_class = IMPORTER.import_class_or_module(name)
        spec = IMPORTER._get_arg_spec(imported_class)
        handles_skip = getattr(imported_class, "HANDLES_SKIP", {})
        positional, named, argument_names = resolve_args(short_name, spec, args, skip, handles_skip=handles_skip)
    except DataError:
        similar_finder = RecommendationFinder()
        similar = similar_finder.find_similar(short_name, TRANSFORMERS)
        raise ImportTransformerError(
            f"Importing transformer '{short_name}' failed. "
            f"Verify if correct name or configuration was provided.{similar}"
        ) from None
    instance = imported_class(*positional, **named)
    return TransformerContainer(instance, argument_names, spec)


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


def resolve_argument_names(argument_names, handles_skip):
    """Get transformer argument names with resolved skip parameters."""
    new_args = ["enabled"]
    if "skip" not in argument_names:
        return new_args + argument_names
    new_args.extend([arg for arg in argument_names if arg != "skip"])
    new_args.extend(arg for arg in sorted(handles_skip) if arg not in new_args)
    return new_args


def assert_handled_arguments(transformer, args, argument_names):
    """Check if provided arguments are handled by given transformer.
    Raises InvalidParameterError if arguments does not match."""
    arg_names = [arg.split("=")[0] for arg in args]
    for arg in arg_names:
        # it's fine to only check for first non-matching parameter
        if arg not in argument_names:
            similar_finder = RecommendationFinder()
            similar = similar_finder.find_similar(arg, argument_names)
            if not similar and argument_names:
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
    argument_names = resolve_argument_names(spec.argument_names, handles_skip)
    assert_handled_arguments(transformer, args, argument_names)
    try:
        positional, named = spec.resolve(args)
        named = dict(named)
        if "skip" in spec.argument_names:
            named["skip"] = get_skip_class(spec, skip_args, global_skip)
        return positional, named, argument_names
    except ValueError as err:
        raise InvalidParameterError(transformer, f" {err}") from None


def resolve_core_import_path(name):
    """Append import path if transformer is core Robotidy transformer."""
    return f"robotidy.transformers.{name}" if name in TRANSFORMERS else name


def load_transformer(name, args, skip) -> Optional[TransformerContainer]:
    import_name = resolve_core_import_path(name)
    return import_transformer(import_name, args, skip)


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
    transformers_config: TransformConfigMap,
    target_version,
    skip=None,
    allow_disabled=False,
    force_order=False,
    allow_version_mismatch=True,
):
    """Dynamically load all classes from this file with attribute `name` defined in selected_transformers"""
    loaded_transformers = []
    transformers_config.update_with_defaults(TRANSFORMERS)
    transformers_config.validate_config_names()
    if not force_order:
        transformers_config.order_using_list(TRANSFORMERS)
    for name, transformer_config in transformers_config.transformers.items():
        if not allow_disabled and not transformers_config.transformer_should_be_included(name):
            continue
        container = load_transformer(name, transformer_config.args, skip)
        if transformers_config.force_included_only:
            enabled = transformer_config.args.get("enabled", True)
        else:
            if "enabled" in transformer_config.args:
                enabled = transformer_config.args["enabled"]
            else:
                enabled = getattr(container.instance, "ENABLED", True)
        if not (enabled or allow_disabled):
            continue
        if can_run_in_robot_version(
            container.instance,
            overwritten=transformers_config.transformer_was_forcefully_enabled(name),
            target_version=target_version,
        ):
            container.enabled_by_default = enabled
            loaded_transformers.append(container)
        elif allow_version_mismatch and allow_disabled:
            setattr(container.instance, "ENABLED", False)
            container.enabled_by_default = False
            loaded_transformers.append(container)
    return loaded_transformers
