import os
import re
from pathlib import Path
import sys
import textwrap
from typing import Any, Dict, List, Optional, Pattern, Tuple, Union

import rich_click as click
from rich.markdown import Markdown

from robotidy.app import Robotidy
from robotidy.console import console
from robotidy.decorators import catch_exceptions
from robotidy.files import DEFAULT_EXCLUDES, find_and_read_config, read_pyproject_config
from robotidy.transformers import load_transformers
from robotidy.utils import (
    GlobalFormattingConfig,
    RecommendationFinder,
    ROBOT_VERSION,
    TargetVersion,
    split_args_from_name_or_path,
)
from robotidy.version import __version__


COLOR_SYSTEM = "auto"
click.rich_click.USE_MARKDOWN = True
click.rich_click.OPTION_GROUPS = {
    "robotidy": [
        {
            "name": "Run only selected transformers",
            "options": ["--transform"],
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
            "options": ["--spacecount", "--line-length", "--lineseparator", "--separator", "--startline", "--endline"],
        },
        {"name": "File exclusion", "options": ["--exclude", "--extend-exclude"]},
        {
            "name": "Other",
            "options": ["--target-version", "--verbose", "--color", "--output", "--version", "--help"],
        },
    ],
}

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])
HELP_MSG = f"""
Version: {__version__}

Robotidy is a tool for formatting Robot Framework source code.
See examples at the end of this help message too see how you can use Robotidy.
Full documentation available at https://robotidy.readthedocs.io .
"""
EPILOG = """
Examples:\n\n
# Format `path/to/src.robot` file\n
$ robotidy path/to/src.robot


# Format every Robot Framework file inside `dir_name` directory

$ robotidy dir_name


# List available transformers:

$ robotidy --list


# Display transformer documentation

$ robotidy --desc <TRANSFORMER_NAME>


# Format `src.robot` file using `SplitTooLongLine` transformer only

$ robotidy --transform SplitTooLongLine src.robot


# Format `src.robot` file using `SplitTooLongLine` transformer only and configured line length 140

$ robotidy --transform SplitTooLongLine:line_length=140 src.robot
"""


class TransformType(click.ParamType):
    name = "transform"

    def convert(self, value, param, ctx):
        name, args = split_args_from_name_or_path(value.replace(" ", ""))
        return name, args


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
            rec_finder = RecommendationFinder()
            similar = rec_finder.find(conf, list(allowed))
            raise click.NoSuchOption(conf, possibilities=similar)


def read_config(ctx: click.Context, param: click.Parameter, value: Optional[str]) -> Optional[str]:
    # if --config was not used, try to find pyproject.toml or robotidy.toml file
    if value:
        config = read_pyproject_config(value)
    else:
        config = find_and_read_config(ctx.params["src"] or (str(Path(".").resolve()),))
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
    return validate_regex(value)


def validate_target_version(
    ctx: click.Context,
    param: Union[click.Option, click.Parameter],
    value: Optional[str],
) -> Optional[int]:
    if value is None:
        return ROBOT_VERSION.major
    version = TargetVersion[value.upper()].value
    if version > ROBOT_VERSION.major:
        raise click.BadParameter(
            f"Target Robot Framework version ({version}) should not be higher than installed version ({ROBOT_VERSION})."
        )
    return version


def validate_regex(value: Optional[str]) -> Optional[Pattern]:
    try:
        return re.compile(value) if value is not None else None
    except re.error:
        raise click.BadParameter("Not a valid regular expression")


def print_transformer_docs(name, transformer):
    documentation = f"## Transformer {name}\n" + textwrap.dedent(transformer.__doc__)
    documentation += f"\nSee <https://robotidy.readthedocs.io/en/latest/transformers/{name}.html> for more examples."
    md = Markdown(documentation, code_theme="native", inline_code_lexer="robotframework")
    console.print(md)


def print_description(name: str, target_version: int):
    transformers = load_transformers(None, {}, allow_disabled=True, target_version=target_version)
    transformer_by_names = {transformer.__class__.__name__: transformer for transformer in transformers}
    if name == "all":
        for tr_name, transformer in transformer_by_names.items():
            print_transformer_docs(tr_name, transformer)
    elif name in transformer_by_names:
        print_transformer_docs(name, transformer_by_names[name])
    else:
        rec_finder = RecommendationFinder()
        similar = rec_finder.find_similar(name, transformer_by_names.keys())
        click.echo(f"Transformer with the name '{name}' does not exist.{similar}")
        return 1
    return 0


def print_transformers_list(target_version: int):
    from rich.table import Table

    table = Table(title="Transformers", header_style="bold red")
    table.add_column("Name", justify="left", no_wrap=True)
    table.add_column("Enabled by default")
    transformers = load_transformers(None, {}, allow_disabled=True, target_version=target_version)
    transformer_names = []
    for transformer in transformers:
        enabled = "[bold magenta]No" if not getattr(transformer, "ENABLED", True) else "Yes"
        transformer_names.append([transformer.__class__.__name__, enabled])
    for name, enabled in sorted(transformer_names):
        table.add_row(name, enabled)
    console.print(table)
    console.print(
        "To see detailed docs run:\n"
        "    [bold]robotidy --desc [bold magenta]transformer_name[/][/]\n"
        "or\n"
        "    [bold]robotidy --desc [bold blue]all[/][/]\n\n"
        "Non-default transformers needs to be selected explicitly with [bold cyan]--transform[/] or "
        "configured with param `enabled=True`.\n"
    )


@click.command(context_settings=CONTEXT_SETTINGS)  # epilog=EPILOG,
@click.option(
    "--transform",
    "-t",
    type=TransformType(),
    multiple=True,
    metavar="TRANSFORMER_NAME",
    help="Transform files from [PATH(S)] with given transformer",
)
@click.option(
    "--configure",
    "-c",
    type=TransformType(),
    multiple=True,
    metavar="TRANSFORMER_NAME:PARAM=VALUE",
    help="Configure transformers",
)
@click.argument(
    "src",
    nargs=-1,
    type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True, allow_dash=True),
    is_eager=True,
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
        f" [default: '{DEFAULT_EXCLUDES}']"
    ),
    show_default=False,
)
@click.option(
    "--extend-exclude",
    type=str,
    callback=validate_regex_callback,
    help=(
        "Like --exclude, but adds additional files and directories on top of the"
        " excluded ones. (Useful if you simply want to add to the default)"
    ),
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
    is_eager=True,
    callback=read_config,
    help="Read configuration from FILE path.",
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
    help="The number of spaces between cells in the plain text format.\n",
    show_default=True,
)
@click.option(
    "-ls",
    "--lineseparator",
    type=click.types.Choice(["native", "windows", "unix", "auto"]),
    default="native",
    help="Line separator to use in outputs.\n"
    "native:  use operating system's native line endings\n"
    "windows: use Windows line endings (CRLF)\n"
    "unix:    use Unix line endings (LF)\n"
    "auto:    maintain existing line endings (uses what's used in the first line)",
    show_default=True,
)
@click.option(
    "--separator",
    type=click.types.Choice(["space", "tab"]),
    default="space",
    help="Token separator to use in outputs.\n"
    "space:   use --spacecount spaces to separate tokens\n"
    "tab:     use a single tabulation to separate tokens\n",
    show_default=True,
)
@click.option(
    "-sl",
    "--startline",
    default=None,
    type=int,
    help="Limit robotidy only to selected area. If --endline is not provided, format text only at --startline. "
    "Line numbers start from 1.",
    show_default=True,
)
@click.option(
    "-el",
    "--endline",
    default=None,
    type=int,
    help="Limit robotidy only to selected area. " "Line numbers start from 1.",
    show_default=True,
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
    is_eager=True,
    is_flag=True,
    help="List available transformers and exit.",
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
    "-t",
    type=click.Choice([v.name.lower() for v in TargetVersion], case_sensitive=False),
    callback=validate_target_version,
    help="Only enable transformers supported in set target version. [default: installed Robot Framework version]",
)
@click.version_option(version=__version__, prog_name="robotidy")
@click.pass_context
@catch_exceptions
def cli(
    ctx: click.Context,
    transform: List[Tuple[str, List]],
    configure: List[Tuple[str, List]],
    src: Tuple[str, ...],
    exclude: Optional[Pattern],
    extend_exclude: Optional[Pattern],
    overwrite: bool,
    diff: bool,
    color: bool,
    check: bool,
    spacecount: int,
    lineseparator: str,
    verbose: bool,
    config: Optional[str],
    separator: Optional[str],
    startline: Optional[int],
    endline: Optional[int],
    line_length: int,
    list: bool,
    desc: Optional[str],
    output: Optional[Path],
    force_order: bool,
    target_version: int,
):
    """
    Robotidy is a tool for formatting Robot Framework source code.

    See examples at the end of this help message too see how you can use Robotidy.
    Full documentation available at https://robotidy.readthedocs.io .
    """
    if list:
        print_transformers_list(target_version)
        sys.exit(0)
    if desc is not None:
        return_code = print_description(desc, target_version)
        sys.exit(return_code)
    if not src:
        if ctx.default_map is not None:
            src = ctx.default_map.get("src", None)
        if not src:
            print("No source path provided. Run robotidy --help to see how to use robotidy")
            sys.exit(1)

    if exclude is None:
        exclude = re.compile(DEFAULT_EXCLUDES)

    if config and verbose:
        click.echo(f"Loaded {config} configuration file")

    if overwrite is None:
        # None is default, with check not set -> overwrite, with check set -> overwrite only when overwrite flag is set
        overwrite = not check

    if color:
        color = "NO_COLOR" not in os.environ

    formatting_config = GlobalFormattingConfig(
        space_count=spacecount,
        line_sep=lineseparator,
        start_line=startline,
        separator=separator,
        end_line=endline,
        line_length=line_length,
    )
    tidy = Robotidy(
        transformers=transform,
        transformers_config=configure,
        src=src,
        exclude=exclude,
        extend_exclude=extend_exclude,
        overwrite=overwrite,
        show_diff=diff,
        formatting_config=formatting_config,
        verbose=verbose,
        check=check,
        output=output,
        force_order=force_order,
        target_version=target_version,
        color=color,
    )
    status = tidy.transform_files()
    sys.exit(status)
