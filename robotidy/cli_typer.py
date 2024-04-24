import re
import sys
from enum import Enum
from pathlib import Path
from typing import List, Optional, Pattern, Tuple, Union

try:
    import rich_click as click

    RICH_PRESENT = True
except ImportError:  # Fails on vendored-in LSP plugin
    import click

    RICH_PRESENT = False

from pathlib import Path

import typer
from typing_extensions import Annotated

from robotidy import app
from robotidy import config as config_module
from robotidy import decorators, exceptions, files, skip, version
from robotidy.config import RawConfig, csv_list_type, validate_target_version
from robotidy.rich_console import console
from robotidy.transformers import (
    TransformConfig,
    TransformConfigMap,
    TransformConfigParameter,
    complete_transformer_name,
    load_transformers,
)
from robotidy.utils import misc
from robotidy.version import __version__

context_settings = {"help_option_names": ["-h", "--help"]}
cli_app = typer.Typer(rich_markup_mode="rich", context_settings=context_settings)  # , no_args_is_help=True


class LineSeparatorStyle(str, Enum):
    native = "native"
    windows = "windows"
    unix = "unix"
    auto = "auto"


class LineSeparator(str, Enum):
    space = "space"
    tab = "tab"


def validate_regex_callback(ctx: click.Context, param: click.Parameter, value: Optional[str]) -> Optional[Pattern]:
    return misc.validate_regex(value)


def validate_list_optional_value(
    ctx: click.Context, param: Union[click.Option, click.Parameter], value: Optional[str]
) -> str:
    if not value:
        return value
    allowed = ["all", "enabled", "disabled"]
    if value not in allowed:
        raise click.BadParameter(f"Not allowed value. Allowed values are: {', '.join(allowed)}")
    return value


def validate_target_version_callback(
    ctx: click.Context, param: Union[click.Option, click.Parameter], value: Optional[str]
) -> int:
    return validate_target_version(value)


def csv_list_type_callback(
    ctx: click.Context, param: Union[click.Option, click.Parameter], value: Optional[str]
) -> List[str]:
    return csv_list_type(value)


def _load_external_transformers(transformers: List, transformers_config: TransformConfigMap, target_version: int):
    external = []
    transformers_names = {transformer.name for transformer in transformers}
    transformers_from_conf = load_transformers(transformers_config, target_version=target_version)
    for transformer in transformers_from_conf:
        if transformer.name not in transformers_names:
            external.append(transformer)
    return external


@decorators.optional_rich
def print_transformers_list(global_config: config_module.MainConfig):
    from rich.table import Table

    target_version = global_config.default.target_version
    list_transformers = global_config.default.list_transformers
    config = global_config.get_config_for_source(Path.cwd())
    table = Table(title="Transformers", header_style="bold red")
    table.add_column("Name", justify="left", no_wrap=True)
    table.add_column("Enabled")
    transformers = load_transformers(TransformConfigMap([], [], []), allow_disabled=True, target_version=target_version)
    transformers.extend(_load_external_transformers(transformers, config.transformers_config, target_version))

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
        rec_finder = misc.RecommendationFinder()
        similar = rec_finder.find_similar(name, transformer_by_names.keys())
        click.echo(f"Transformer with the name '{name}' does not exist.{similar}", err=True)
        return 1
    return 0


def generate_default_config(global_config: config_module.MainConfig):
    try:
        import tomli_w
    except ImportError:
        raise exceptions.MissingOptionalTomliWDependencyError()
    target_version = global_config.default.target_version
    config = global_config.default_loaded
    transformers = load_transformers(TransformConfigMap([], [], []), allow_disabled=True, target_version=target_version)
    transformers.extend(_load_external_transformers(transformers, config.transformers_config, target_version))

    toml_config = {
        "tool": {
            "robotidy": {
                "diff": global_config.default_loaded.show_diff,
                "overwrite": global_config.default_loaded.overwrite,
                "verbose": global_config.default_loaded.verbose,
                "separator": global_config.default.separator,
                "spacecount": global_config.default_loaded.formatting.space_count,
                "line_length": global_config.default.line_length,
                "lineseparator": global_config.default.lineseparator,
                "skip_gitignore": global_config.default.skip_gitignore,
                "ignore_git_dir": global_config.default.ignore_git_dir,
            }
        }
    }
    configure_transformers = [
        f"{transformer.name}:enabled={transformer.name in config.transformers_lookup}" for transformer in transformers
    ]
    toml_config["tool"]["robotidy"]["configure"] = configure_transformers

    with open(global_config.default.generate_config, "w") as fp:
        fp.write(tomli_w.dumps(toml_config))


def version_callback(value: bool):
    if value:
        print(f"robotidy, version {__version__}")
        raise typer.Exit()


@cli_app.command()
def desc(transformer_name: Annotated[str, typer.Argument(help="Transformer name")]):
    """Show documentation for selected transformer."""
    raise typer.Exit()


# FIXME OR --list always require value (all / enabled / disabled) OR list command


@cli_app.callback(invoke_without_command=True)
def robotidy_cli(
    ctx: typer.Context,
    src: Annotated[list[Path], typer.Argument(allow_dash=True, writable=True, lazy=True)] = None,
    transform: Annotated[
        list[TransformConfig],
        typer.Option(
            "--transform",
            "-t",
            click_type=TransformConfigParameter(),
            show_default=False,
            rich_help_panel="Run only selected transformers",
            help="Transform files from [PATH(S)] with given transformer",
        ),
    ] = None,
    custom_transformers: Annotated[
        list[TransformConfig],
        typer.Option(
            "--load-transformers",
            "--custom-transformers",
            click_type=TransformConfigParameter(),
            show_default=False,
            rich_help_panel="Load custom transformers",
            help="Load custom transformer from the path and run them after default ones.",
        ),
    ] = None,
    configure: Annotated[
        list[TransformConfig],
        typer.Option(
            "--configure",
            "-c",
            click_type=TransformConfigParameter(),
            metavar="TRANSFORMER_NAME:PARAM=VALUE",
            show_default=False,
            rich_help_panel="Configuration",
            help="Configure transformers",
        ),
    ] = None,
    exclude: Annotated[
        str,
        typer.Option(
            callback=validate_regex_callback,
            show_default=f"{files.DEFAULT_EXCLUDES}",
            help=(
                "A regular expression that matches files and directories that should be"
                " excluded on recursive searches. An empty value means no paths are excluded."
                " Use forward slashes for directories on all platforms."
            ),
        ),
    ] = re.compile(files.DEFAULT_EXCLUDES),
    extend_exclude: Annotated[
        str,
        typer.Option(
            callback=validate_regex_callback,
            help=(
                "Like [b]--exclude[/], but adds additional files and directories on top of the"
                " excluded ones. (Useful if you simply want to add to the default)"
            ),
        ),
    ] = None,
    skip_gitignore: Annotated[
        bool,
        typer.Option("--skip-gitignore", help="Skip [b].gitignore[/] files and do not ignore files listed inside."),
    ] = False,
    ignore_git_dir: Annotated[
        bool,
        typer.Option(
            "--ignore-git-dir",
            help="Ignore [b].git[/] directories when searching for the default configuration file. "
            "By default first parent directory with [b].git[/] directory is returned and this flag disables this behaviour.",
        ),
    ] = False,
    config: Annotated[
        Path,
        typer.Option(
            file_okay=True,
            dir_okay=False,
            exists=True,
            readable=True,
            allow_dash=False,
            path_type=str,
            rich_help_panel="Configuration",
            help="Read configuration from FILE path.",
        ),
    ] = None,
    overwrite: Annotated[bool, typer.Option(help="Write changes back to file")] = True,
    diff: Annotated[bool, typer.Option("--diff", help="Output diff of each processed file.")] = False,
    color: Annotated[bool, typer.Option(help="Enable ANSI coloring the output")] = True,  # FIXME check in typer
    check: Annotated[
        bool,
        typer.Option(
            "--check",
            help="Don't overwrite files and just return status. Return code 0 means nothing would change. "
            "Return code 1 means that at least 1 file would change. Any internal error will overwrite this status.",
        ),
    ] = False,
    spacecount: Annotated[int, typer.Option("--spacecount", "-s", help="The number of spaces between cells")] = 4,
    indent: Annotated[
        int,
        typer.Option(show_default="same as --spacecount value", help="The number of spaces to be used as indentation"),
    ] = None,
    continuation_indent: Annotated[
        int,
        typer.Option(
            show_default="same as --spacecount value",
            help="The number of spaces to be used as separator after ... (line continuation) token",
        ),
    ] = None,
    lineseparator: Annotated[
        LineSeparatorStyle,
        typer.Option(
            "--lineseparator",
            "-ls",
            help="""
        Line separator to use in the outputs:
        - **native**:  use operating system's native line endings
        - windows: use Windows line endings (CRLF)
        - unix:    use Unix line endings (LF)
        - auto:    maintain existing line endings (uses what's used in the first line)
        """,
        ),
    ] = LineSeparatorStyle.native,
    separator: Annotated[
        LineSeparator,
        typer.Option(
            help="""
        Token separator to use in the outputs:
        - **space**:   use --spacecount spaces to separate tokens
        - tab:     use a single tabulation to separate tokens
        """
        ),
    ] = LineSeparator.space,
    startline: Annotated[
        int,
        typer.Option(
            "--startline",
            "-sl",
            show_default=False,
            help="Limit robotidy only to selected area. If [b]--endline[/] is not provided, format text only at **--startline**. Line numbers start from 1.",
        ),
    ] = None,
    endline: Annotated[
        int,
        typer.Option(
            "--endline",
            "-el",
            show_default=False,
            help="Limit robotidy only to selected area. Line numbers start from 1.",
        ),
    ] = None,
    line_length: Annotated[int, typer.Option(help="Max allowed characters per line")] = 120,
    # list_transformers: Annotated[
    #     str,
    #     typer.Option(
    #         "--list",
    #         "-l",
    #         callback=validate_list_optional_value,
    #         flag_value="all",
    #         show_default=False,
    #         help="List available transformers and exit. "
    #         "Pass optional value [b]enabled[/] or [b]disabled[/] to filter out list by transformer status.",
    #     ),
    # ] = "",
    generate_config: Annotated[
        str,
        typer.Option(
            flag_value="pyproject.toml",
            show_default="pyproject.toml",
            help="Generate configuration file. Pass optional value to change default config filename.",
        ),
    ] = "",
    describe_transformer: Annotated[
        str,
        typer.Option("--desc", "-d", metavar="TRANSFORMER_NAME", help="Show documentation for selected transformer."),
    ] = None,
    output: Annotated[
        Path,
        typer.Option(
            "--output",
            "-o",
            metavar="PATH",
            file_okay=True,
            dir_okay=False,
            writable=True,
            allow_dash=False,
            help="Use this option to override file destination path.",
        ),
    ] = None,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="More verbose output")] = False,
    force_order: Annotated[
        bool, typer.Option("--force-order", help="Transform files using transformers in order provided in cli")
    ] = False,
    target_version: Annotated[  # FIXME
        str,
        typer.Option(
            "--target-version",
            "-tv",
            case_sensitive=False,
            callback=validate_target_version_callback,
            # show_choices=["rf4", "rf5", "rf6", "rf7"],
            show_default="installed Robot Framework version",
            help="Only enable transformers supported in set target version",
        ),
    ] = None,
    language: Annotated[  # TODO test if default en will be used for callback
        list[str],
        typer.Option(
            "--language",
            "--lang",
            callback=csv_list_type_callback,
            show_default="en",
            help="Parse Robot Framework files using additional languages.",
        ),
    ] = None,
    reruns: Annotated[
        int,
        typer.Option(
            "--reruns",
            "-r",
            help="Robotidy will rerun the transformations up to reruns times until the code stop changing.",
        ),
    ] = 0,
    skip_comments: Annotated[
        bool, typer.Option("--skip-comments", help="Skip formatting of comments", rich_help_panel="Skip formatting")
    ] = False,
    skip_documentation: Annotated[
        bool,
        typer.Option(
            "--skip-documentation", help="Skip formatting of documentation", rich_help_panel="Skip formatting"
        ),
    ] = False,
    # @skip.return_values_option
    # @skip.keyword_call_option
    # @skip.keyword_call_pattern_option
    # @skip.settings_option
    # @skip.arguments_option
    # @skip.setup_option
    # @skip.teardown_option
    # @skip.timeout_option
    # @skip.template_option
    # @skip.return_option
    # @skip.tags_option
    # @skip.sections_option
    # @skip.block_comments_option
    version: Annotated[
        bool,
        typer.Option("--version", callback=version_callback, is_eager=True),
    ] = None,
):
    """
    Robotidy is a tool for formatting Robot Framework source code.
    Full documentation available at <https://robotidy.readthedocs.io> .
    """
    if ctx.invoked_subcommand is not None:
        return
    # TODO
    # Load all options, create configs and then decide to run Robotidy or delegate to commands
    # TODOlist should probably be separate command, but accept the same --transform/etc stuff? load default config?
    # but then this fn should be still default cmd
    cli_config = RawConfig.from_cli(**locals())
    global_config = config_module.MainConfig(cli_config)
    global_config.validate_src_is_required()
    if (
        not global_config.default.list_transformers
        and not global_config.default.describe_transformer
        and not global_config.default.generate_config
    ):
        tidy = app.Robotidy(global_config)
        status = tidy.transform_files()
        raise typer.Exit(status)

    # if global_config.default.list_transformers:
    #     print_transformers_list(global_config)
    #     raise typer.Exit()
    # if global_config.default.describe_transformer is not None:
    #     return_code = print_description(
    #         global_config.default.describe_transformer, global_config.default.target_version
    #     )
    #     raise typer.Exit(return_code)
    # if global_config.default.generate_config:
    #     generate_default_config(global_config)
    #     raise typer.Exit()
    raise ValueError("SHALL NOT PASS")


if __name__ == "__main__":
    cli_app()
