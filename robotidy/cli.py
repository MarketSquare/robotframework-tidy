import copy
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Pattern, Set, Tuple, Union

try:
    import rich_click as click

    RICH_PRESENT = True
except ImportError:  # Fails on vendored-in LSP plugin
    import click

    RICH_PRESENT = False
from click.core import ParameterSource

from robotidy import app, decorators, files, skip, utils, version
from robotidy.config import Config, FormattingConfig
from robotidy.rich_console import console
from robotidy.transformers import TransformConfig, TransformConfigMap, TransformConfigParameter, load_transformers

CLI_OPTIONS_LIST = [
    {
        "name": "Run only selected transformers",
        "options": ["--transform"],
    },
    {
        "name": "Load custom transformers",
        "options": ["--load-transformers"],
    },
    {
        "name": "Work modes",
        "options": ["--overwrite", "--diff", "--check", "--force-order"],
    },
    {
        "name": "Documentation",
        "options": ["--list", "--desc"],
    },
    {
        "name": "Configuration",
        "options": ["--configure", "--config"],
    },
    {
        "name": "Global formatting settings",
        "options": [
            "--spacecount",
            "--indent",
            "--continuation-indent",
            "--line-length",
            "--lineseparator",
            "--separator",
            "--startline",
            "--endline",
        ],
    },
    {"name": "File exclusion", "options": ["--exclude", "--extend-exclude", "--skip-gitignore"]},
    skip.option_group,
    {
        "name": "Other",
        "options": ["--target-version", "--language", "--verbose", "--color", "--output", "--version", "--help"],
    },
]

if RICH_PRESENT:
    click.rich_click.USE_RICH_MARKUP = True
    click.rich_click.USE_MARKDOWN = True
    click.rich_click.STYLE_OPTION = "bold sky_blue3"
    click.rich_click.STYLE_SWITCH = "bold sky_blue3"
    click.rich_click.STYLE_METAVAR = "bold white"
    click.rich_click.STYLE_OPTION_DEFAULT = "grey37"
    click.rich_click.STYLE_OPTIONS_PANEL_BORDER = "grey66"
    click.rich_click.STYLE_USAGE = "magenta"
    click.rich_click.OPTION_GROUPS = {
        "robotidy": CLI_OPTIONS_LIST,
        "python -m robotidy": CLI_OPTIONS_LIST,
    }


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


def parse_opt(opt):
    while opt and opt[0] == "-":
        opt = opt[1:]
    return opt.replace("-", "_")


def validate_config_options(params, config):
    if params is None:
        return
    allowed = {parse_opt(opt) for param in params for opt in param.opts}
    for conf in config:
        if conf not in allowed:
            rec_finder = utils.RecommendationFinder()
            similar = rec_finder.find(conf, list(allowed))
            raise click.NoSuchOption(conf, possibilities=similar)


def read_config_file(ctx: click.Context, config_path, srcs: Tuple[str, ...], ignore_git_dir: bool) -> Optional[Dict]:
    if config_path:
        config = files.read_pyproject_config(config_path)
    elif srcs:
        return None
    else:
        src = (str(Path(".").resolve()),)  # FIXME  find and read should work with only one path
        config = files.find_and_read_config(src, ignore_git_dir)
    # Sanitize the values to be Click friendly. For more information please see:
    # https://github.com/psf/black/issues/1458
    # https://github.com/pallets/click/issues/1567
    config = {k: str(v) if not isinstance(v, (list, dict)) else v for k, v in config.items()}
    if "src" in config:
        config["src"] = tuple(config["src"])
    validate_config_options(ctx.command.params, config)
    return config


def read_config(ctx: click.Context, param: click.Parameter, value: Optional[str]) -> Optional[str]:
    # if --config was not used, try to find pyproject.toml or robotidy.toml file
    if value:
        config = files.read_pyproject_config(value)
    else:
        src = ctx.params["src"] or (str(Path(".").resolve()),)
        ignore_git_dir = ctx.params["ignore_git_dir"]
        config = files.find_and_read_config(src, ignore_git_dir)
    if not config:
        return
    # Sanitize the values to be Click friendly. For more information please see:
    # https://github.com/psf/black/issues/1458
    # https://github.com/pallets/click/issues/1567
    config = {k: str(v) if not isinstance(v, (list, dict)) else v for k, v in config.items()}
    if "src" in config:
        config["src"] = tuple(config["src"])
    validate_config_options(ctx.command.params, config)
    default_map: Dict[str, Any] = {}
    if ctx.default_map:
        default_map.update(ctx.default_map)
    default_map.update(config)
    ctx.default_map = default_map


def validate_regex_callback(
    ctx: click.Context,
    param: click.Parameter,
    value: Optional[str],
) -> Optional[Pattern]:
    return utils.validate_regex(value)


def validate_target_version(
    ctx: click.Context,
    param: Union[click.Option, click.Parameter],
    value: Optional[str],
) -> Optional[int]:
    if value is None:
        return utils.ROBOT_VERSION.major
    version = utils.TargetVersion[value.upper()].value
    if version > utils.ROBOT_VERSION.major:
        raise click.BadParameter(
            f"Target Robot Framework version ({version}) should not be higher than "
            f"installed version ({utils.ROBOT_VERSION})."
        )
    return version


def validate_list_optional_value(
    ctx: click.Context,
    param: Union[click.Option, click.Parameter],
    value: Optional[str],
):
    if not value:
        return value
    allowed = ["all", "enabled", "disabled"]
    if value not in allowed:
        raise click.BadParameter(f"Not allowed value. Allowed values are: {', '.join(allowed)}")
    return value


def csv_list_type(ctx: click.Context, param: Union[click.Option, click.Parameter], value: Optional[str]) -> List[str]:
    if not value:
        return []
    return value.split(",")


def print_transformer_docs(transformer):
    from rich.markdown import Markdown

    md = Markdown(str(transformer), code_theme="native", inline_code_lexer="robotframework")
    console.print(md)


@decorators.optional_rich
def print_description(name: str, target_version: int):
    # TODO: --desc works only for default transformers, it should also print custom transformer desc
    transformers = load_transformers(TransformConfigMap([], [], []), allow_disabled=True, target_version=target_version)
    transformer_by_names = {transformer.name: transformer for transformer in transformers}
    if name == "all":
        for transformer in transformers:
            print_transformer_docs(transformer)
    elif name in transformer_by_names:
        print_transformer_docs(transformer_by_names[name])
    else:
        rec_finder = utils.RecommendationFinder()
        similar = rec_finder.find_similar(name, transformer_by_names.keys())
        click.echo(f"Transformer with the name '{name}' does not exist.{similar}")
        return 1
    return 0


def _load_external_transformers(transformers: List, transformers_config: TransformConfigMap, target_version: int):
    external = []
    transformers_names = {transformer.name for transformer in transformers}
    transformers_from_conf = load_transformers(transformers_config, target_version=target_version)
    for transformer in transformers_from_conf:
        if transformer.name not in transformers_names:
            external.append(transformer)
    return external


@decorators.optional_rich
def print_transformers_list(
    transformers_config: TransformConfigMap, config: Config, target_version: int, list_transformers: str
):
    from rich.table import Table

    table = Table(title="Transformers", header_style="bold red")
    table.add_column("Name", justify="left", no_wrap=True)
    table.add_column("Enabled")
    transformers = load_transformers(TransformConfigMap([], [], []), allow_disabled=True, target_version=target_version)
    transformers.extend(_load_external_transformers(transformers, transformers_config, target_version))

    for transformer in transformers:
        enabled = transformer.name in config.transformers_lookup
        if list_transformers != "all":
            filter_by = list_transformers == "enabled"
            if enabled != filter_by:
                continue
        decorated_enable = "Yes" if enabled else "No"
        if enabled != transformer.enabled_by_default:
            decorated_enable = f"[bold magenta]{decorated_enable}*"
        table.add_row(transformer.name, decorated_enable)
    console.print(table)
    console.print(
        "Transformers are listed in the order they are run by default. If the transformer was enabled/disabled by the "
        "configuration the status will be displayed with extra asterisk (*) and in the [magenta]different[/] color."
    )
    console.print(
        "To see detailed docs run:\n"
        "    [bold]robotidy --desc [blue]transformer_name[/][/]\n"
        "or\n"
        "    [bold]robotidy --desc [blue]all[/][/]\n\n"
        "Non-default transformers needs to be selected explicitly with [bold cyan]--transform[/] or "
        "configured with param `enabled=True`.\n"
    )


# create config from cli, remember which ones are defined in cli and which are just defaults
# cli are most important
#
@dataclass
class RawConfig:
    """Configuration read directly from cli or configuration file."""

    transform: List[TransformConfig]
    custom_transformers: List[TransformConfig]
    configure: List[TransformConfig]
    src: Tuple[str, ...]
    exclude: Optional[Pattern]
    extend_exclude: Optional[Pattern]
    skip_gitignore: bool
    overwrite: bool
    diff: bool
    color: bool
    check: bool
    spacecount: int
    indent: Optional[int]
    continuation_indent: Optional[int]
    lineseparator: str
    verbose: bool
    config: Optional[str]
    config_directory: Optional[str]
    separator: Optional[str]
    startline: Optional[int]
    endline: Optional[int]
    line_length: int
    list_transformers: str
    desc: Optional[str]
    output: Optional[Path]
    force_order: bool
    target_version: int
    language: Optional[List[str]]
    reruns: int
    ignore_git_dir: bool
    skip_comments: bool
    skip_documentation: bool
    skip_return_values: bool
    skip_keyword_call: List[str]
    skip_keyword_call_pattern: List[str]
    skip_settings: bool
    skip_arguments: bool
    skip_setup: bool
    skip_teardown: bool
    skip_timeout: bool
    skip_template: bool
    skip_return: bool
    skip_tags: bool
    skip_block_comments: bool
    skip_sections: str
    defined_in_cli: Set = field(default_factory=set)

    @classmethod
    def from_cli(cls, ctx: click.Context, **kwargs):
        """Creates RawConfig instances while saving which options were supplied from CLI."""
        defined_in_cli = set()
        for option in kwargs:
            if ctx.get_parameter_source(option) == ParameterSource.COMMANDLINE:
                defined_in_cli.add(option)
        return cls(**kwargs, defined_in_cli=defined_in_cli)

    def merge_with_config_file(self, config: Dict) -> "RawConfig":
        """Merge cli config with the configuration file config.

        Use configuration file parameter value only if it was not defined in the cli already.
        """
        merged = copy.deepcopy(self)
        if not config:
            return merged
        for param, param_value in config.items():
            if param == "src" or param not in self.defined_in_cli:
                setattr(merged, param, param_value)
        return merged


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--transform",
    "-t",
    type=TransformConfigParameter(),
    multiple=True,
    metavar="TRANSFORMER_NAME",
    help="Transform files from [PATH(S)] with given transformer",
)
@click.option(
    "--load-transformers",
    "custom_transformers",
    type=TransformConfigParameter(),
    multiple=True,
    metavar="TRANSFORMER_NAME",
    help="Load custom transformer from the path and run them after default ones.",
)
@click.option(
    "--configure",
    "-c",
    type=TransformConfigParameter(),
    multiple=True,
    metavar="TRANSFORMER_NAME:PARAM=VALUE",
    help="Configure transformers",
)
@click.argument(
    "src",
    nargs=-1,
    type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True, allow_dash=True),
    # is_eager=True,
    metavar="[PATH(S)]",
)
@click.option(
    "--exclude",
    type=str,
    callback=validate_regex_callback,
    help=(
        "A regular expression that matches files and directories that should be"
        " excluded on recursive searches. An empty value means no paths are excluded."
        " Use forward slashes for directories on all platforms."
    ),
    show_default=f"{files.DEFAULT_EXCLUDES}",
)
@click.option(
    "--extend-exclude",
    type=str,
    callback=validate_regex_callback,
    help=(
        "Like **--exclude**, but adds additional files and directories on top of the"
        " excluded ones. (Useful if you simply want to add to the default)"
    ),
)
@click.option(
    "--skip-gitignore",
    is_flag=True,
    show_default=True,
    help="Skip **.gitignore** files and do not ignore files listed inside.",
)
@click.option(
    "--ignore-git-dir",
    is_flag=True,
    # is_eager=True,
    help="Ignore .git directories when searching for the default configuration file. "
    "By default first parent directory with .git directory is returned and this flag disables this behaviour.",
    show_default=True,
)
@click.option(
    "--config",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        allow_dash=False,
        path_type=str,
    ),
    # is_eager=True,
    # callback=read_config,
    help="Read configuration from FILE path.",
)
# This option is workaround to make it possible to pass configuration directory when reading config.
# We first load the config file and then map every value from it as cli option defaults. The option must exist, so we
# cannot pass additional info, ie the directory where config file was found.
@click.option(
    "--config-directory",
    hidden=True,
)
@click.option(
    "--overwrite/--no-overwrite",
    default=None,
    help="Write changes back to file",
    show_default=True,
)
@click.option(
    "--diff",
    is_flag=True,
    help="Output diff of each processed file.",
    show_default=True,
)
@click.option(
    "--color/--no-color",
    default=True,
    help="Enable ANSI coloring the output",
    show_default=True,
)
@click.option(
    "--check",
    is_flag=True,
    help="Don't overwrite files and just return status. Return code 0 means nothing would change. "
    "Return code 1 means that at least 1 file would change. Any internal error will overwrite this status.",
    show_default=True,
)
@click.option(
    "-s",
    "--spacecount",
    type=click.types.INT,
    default=4,
    help="The number of spaces between cells",
    show_default=True,
)
@click.option(
    "--indent",
    type=click.types.INT,
    default=None,
    help="The number of spaces to be used as indentation",
    show_default="same as --spacecount value",
)
@click.option(
    "--continuation-indent",
    type=click.types.INT,
    default=None,
    help="The number of spaces to be used as separator after ... (line continuation) token",
    show_default="same as --spacecount value]",
)
@click.option(
    "-ls",
    "--lineseparator",
    type=click.types.Choice(["native", "windows", "unix", "auto"]),
    default="native",
    help="""
    Line separator to use in the outputs:
    - **native**:  use operating system's native line endings
    - windows: use Windows line endings (CRLF)
    - unix:    use Unix line endings (LF)
    - auto:    maintain existing line endings (uses what's used in the first line)
    """,
    show_default=True,
)
@click.option(
    "--separator",
    type=click.types.Choice(["space", "tab"]),
    default="space",
    help="""
    Token separator to use in the outputs:
    - **space**:   use --spacecount spaces to separate tokens
    - tab:     use a single tabulation to separate tokens
    """,
    show_default=True,
)
@click.option(
    "-sl",
    "--startline",
    default=None,
    type=int,
    help="Limit robotidy only to selected area. If **--endline** is not provided, format text only at **--startline**. "
    "Line numbers start from 1.",
)
@click.option(
    "-el",
    "--endline",
    default=None,
    type=int,
    help="Limit robotidy only to selected area. Line numbers start from 1.",
)
@click.option(
    "--line-length",
    default=120,
    type=int,
    help="Max allowed characters per line",
    show_default=True,
)
@click.option(
    "--list",
    "-l",
    "list_transformers",
    callback=validate_list_optional_value,
    # is_eager=True,
    is_flag=False,
    default="",
    flag_value="all",
    help="List available transformers and exit. "
    "Pass optional value **enabled** or **disabled** to filter out list by transformer status.",
)
@click.option(
    "--desc",
    "-d",
    default=None,
    metavar="TRANSFORMER_NAME",
    help="Show documentation for selected transformer.",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(file_okay=True, dir_okay=False, writable=True, allow_dash=False),
    default=None,
    metavar="PATH",
    help="Use this option to override file destination path.",
)
@click.option("-v", "--verbose", is_flag=True, help="More verbose output", show_default=True)
@click.option(
    "--force-order",
    is_flag=True,
    help="Transform files using transformers in order provided in cli",
)
@click.option(
    "--target-version",
    "-tv",
    type=click.Choice([v.name.lower() for v in utils.TargetVersion], case_sensitive=False),
    callback=validate_target_version,
    help="Only enable transformers supported in set target version",
    show_default="installed Robot Framework version",
)
@click.option(
    "--language",
    "--lang",
    callback=csv_list_type,
    help="Parse Robot Framework files using additional languages.",
    show_default="en",
)
@click.option(
    "--reruns",
    "-r",
    type=int,
    help="Robotidy will rerun the transformations up to reruns times until the code stop changing.",
    show_default="0",
)
@skip.comments_option
@skip.documentation_option
@skip.return_values_option
@skip.keyword_call_option
@skip.keyword_call_pattern_option
@skip.settings_option
@skip.arguments_option
@skip.setup_option
@skip.teardown_option
@skip.timeout_option
@skip.template_option
@skip.return_option
@skip.tags_option
@skip.sections_option
@skip.block_comments_option
@click.version_option(version=version.__version__, prog_name="robotidy")
@click.pass_context
@decorators.catch_exceptions
def cli(
    ctx: click.Context,
    transform: List[TransformConfig],
    custom_transformers: List[TransformConfig],
    configure: List[TransformConfig],
    src: Tuple[str, ...],
    exclude: Optional[Pattern],
    extend_exclude: Optional[Pattern],
    skip_gitignore: bool,
    overwrite: bool,
    diff: bool,
    color: bool,
    check: bool,
    spacecount: int,
    indent: Optional[int],
    continuation_indent: Optional[int],
    lineseparator: str,
    verbose: bool,
    config: Optional[str],
    config_directory: Optional[str],
    separator: Optional[str],
    startline: Optional[int],
    endline: Optional[int],
    line_length: int,
    list_transformers: str,
    desc: Optional[str],
    output: Optional[Path],
    force_order: bool,
    target_version: int,
    language: Optional[List[str]],
    reruns: int,
    ignore_git_dir: bool,
    skip_comments: bool,
    skip_documentation: bool,
    skip_return_values: bool,
    skip_keyword_call: List[str],
    skip_keyword_call_pattern: List[str],
    skip_settings: bool,
    skip_arguments: bool,
    skip_setup: bool,
    skip_teardown: bool,
    skip_timeout: bool,
    skip_template: bool,
    skip_return: bool,
    skip_tags: bool,
    skip_block_comments: bool,
    skip_sections: str,
):
    """
    Robotidy is a tool for formatting Robot Framework source code.
    Full documentation available at <https://robotidy.readthedocs.io> .
    """
    # TODO config_directory dont need to be option anymore
    cli_config = RawConfig.from_cli(**locals())
    # if the --config is defined, or there are no sources in cli so we need to search from config in cwd
    config_file = read_config_file(ctx, cli_config.config, cli_config.src, cli_config.ignore_git_dir)
    common_config = cli_config.merge_with_config_file(config_file)
    # read config file, merge with cli config
    # if not src, search from root, load config, check if src

    # TODO if --config, we do not need to search for configs
    if not common_config.src and not (common_config.list_transformers or common_config.desc):
        print("No source path provided. Run robotidy --help to see how to use robotidy")
        sys.exit(1)

    if common_config.exclude is None:
        common_config.exclude = re.compile(files.DEFAULT_EXCLUDES)

    if common_config.config_directory and common_config.verbose:  # TODO print where it is loaded, if at all
        click.echo(f"Loaded {common_config.config} configuration file")  # FIXME

    if common_config.overwrite is None:
        # None is default, with check not set -> overwrite, with check set -> overwrite only when overwrite flag is set
        common_config.overwrite = not common_config.check

    if common_config.color:
        common_config.color = "NO_COLOR" not in os.environ

    skip_config = skip.SkipConfig(
        documentation=common_config.skip_documentation,
        return_values=common_config.skip_return_values,
        keyword_call=common_config.skip_keyword_call,
        keyword_call_pattern=common_config.skip_keyword_call_pattern,
        settings=common_config.skip_settings,
        arguments=common_config.skip_arguments,
        setup=common_config.skip_setup,
        teardown=common_config.skip_teardown,
        template=common_config.skip_template,
        timeout=common_config.skip_timeout,
        return_statement=common_config.skip_return,
        tags=common_config.skip_tags,
        comments=common_config.skip_comments,
        block_comments=common_config.skip_block_comments,
        sections=common_config.skip_sections,
    )

    formatting = FormattingConfig(
        space_count=common_config.spacecount,
        indent=common_config.indent,
        continuation_indent=common_config.continuation_indent,
        line_sep=common_config.lineseparator,
        start_line=common_config.startline,
        separator=common_config.separator,
        end_line=common_config.endline,
        line_length=common_config.line_length,
    )

    transformers_config = TransformConfigMap(
        common_config.transform, common_config.custom_transformers, common_config.configure
    )
    config = Config(
        formatting=formatting,
        skip=skip_config,
        transformers_config=transformers_config,
        src=common_config.src,
        exclude=common_config.exclude,
        extend_exclude=common_config.extend_exclude,
        skip_gitignore=common_config.skip_gitignore,
        overwrite=common_config.overwrite,
        show_diff=common_config.diff,
        verbose=common_config.verbose,
        check=common_config.check,
        output=common_config.output,
        force_order=common_config.force_order,
        target_version=common_config.target_version,
        color=common_config.color,
        language=common_config.language,
        reruns=common_config.reruns,
        config_directory=common_config.config_directory,
    )

    if common_config.list_transformers:
        print_transformers_list(
            transformers_config, config, common_config.target_version, common_config.list_transformers
        )
        sys.exit(0)
    if common_config.desc is not None:
        return_code = print_description(common_config.desc, common_config.target_version)
        sys.exit(return_code)

    tidy = app.Robotidy(config=config)
    status = tidy.transform_files()
    sys.exit(status)
