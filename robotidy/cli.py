from pathlib import Path
from typing import (
    Tuple,
    Dict,
    List,
    Iterable,
    Optional,
    Any
)

import click
import toml

from robotidy.app import Robotidy
from robotidy.transformers import load_transformers
from robotidy.utils import (
    GlobalFormattingConfig,
    split_args_from_name_or_path,
    remove_rst_formatting
)
from robotidy.version import __version__


HELP_MSG = f"""
Version: {__version__}

Robotidy is a tool for formatting Robot Framework source code.
See examples at the end of this help message too see how you can use Robotidy.
For more documentation check README section at https://github.com/MarketSquare/robotframework-tidy
"""
EPILOG = """
Examples:
  # Format `path/to/src.robot` file
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


class RawHelp(click.Command):
    def format_help_text(self, ctx, formatter):
        if self.help:
            formatter.write_paragraph()
            for line in self.help.split('\n'):
                formatter.write_text(line)

    def format_epilog(self, ctx, formatter):
        if self.epilog:
            formatter.write_paragraph()
            for line in self.epilog.split('\n'):
                formatter.write_text(line)


class TransformType(click.ParamType):
    name = "transform"

    def convert(self, value, param, ctx):
        name = ''
        try:
            name, args = split_args_from_name_or_path(value)
        except ValueError:
            exc = f'Invalid {name} transformer configuration. ' \
                  f'Parameters should be provided in format name=value, delimited by :'
            raise ValueError(exc)
        return name, args


def find_project_root(srcs: Iterable[str]) -> Path:
    """Return a directory containing .git, or robotidy.toml.
    That directory will be a common parent of all files and directories
    passed in `srcs`.
    If no directory in the tree contains a marker that would specify it's the
    project root, the root of the file system is returned.
    """
    if not srcs:
        return Path("/").resolve()

    path_srcs = [Path(Path.cwd(), src).resolve() for src in srcs]

    # A list of lists of parents for each 'src'. 'src' is included as a
    # "parent" of itself if it is a directory
    src_parents = [
        list(path.parents) + ([path] if path.is_dir() else []) for path in path_srcs
    ]

    common_base = max(
        set.intersection(*(set(parents) for parents in src_parents)),
        key=lambda path: path.parts,
    )

    for directory in (common_base, *common_base.parents):
        if (directory / ".git").exists():
            return directory

        if (directory / "robotidy.toml").is_file():
            return directory

        if (directory / "pyproject.toml").is_file():
            return directory

    return directory


def find_and_read_config(src_paths: Iterable[str]) -> Dict[str, Any]:
    project_root = find_project_root(src_paths)
    config_path = project_root / 'robotidy.toml'
    if config_path.is_file():
        return read_robotidy_config(str(config_path))
    pyproject_path = project_root / 'pyproject.toml'
    if pyproject_path.is_file():
        return read_pyproject_config(str(pyproject_path))
    return {}


def load_toml_file(path: str) -> Dict[str, Any]:
    try:
        config = toml.load(path)
        click.echo(f"Loaded configuration from {path}")
        return config
    except (toml.TomlDecodeError, OSError) as e:
        raise click.FileError(
            filename=path, hint=f"Error reading configuration file: {e}"
        )


def read_pyproject_config(path: str) -> Dict[str, Any]:
    click.echo('Reading pyproject.toml')
    config = load_toml_file(path)
    config = config.get("tool", {}).get("robotidy", {})
    return {k.replace('--', '').replace('-', '_'): v for k, v in config.items()}


def read_robotidy_config(path: str) -> Dict[str, Any]:
    config = load_toml_file(path)
    return {k.replace('--', '').replace('-', '_'): v for k, v in config.items()}


def read_config(ctx: click.Context, param: click.Parameter, value: Optional[str]) -> Optional[str]:
    # if --config was not used, try to find pyproject.toml or robotidy.toml file
    if value:
        config = read_robotidy_config(value)
    else:
        config = find_and_read_config(ctx.params.get("src", ()))
    if not config:
        return
    # Sanitize the values to be Click friendly. For more information please see:
    # https://github.com/psf/black/issues/1458
    # https://github.com/pallets/click/issues/1567
    config = {
        k: str(v) if not isinstance(v, (list, dict)) else v
        for k, v in config.items()
    }

    default_map: Dict[str, Any] = {}
    if ctx.default_map:
        default_map.update(ctx.default_map)
    default_map.update(config)
    ctx.default_map = default_map


@click.command(cls=RawHelp, help=HELP_MSG, epilog=EPILOG)
@click.option(
    '--transform',
    '-t',
    type=TransformType(),
    multiple=True,
    metavar='TRANSFORMER_NAME',
    help="Transform files from [PATH(S)] with given transformer"
)
@click.option(
    '--configure',
    '-c',
    type=TransformType(),
    multiple=True,
    metavar='TRANSFORMER_NAME:PARAM=VALUE',
    help='Configure transformers'
)
@click.argument(
    "src",
    nargs=-1,
    type=click.Path(
        exists=True, file_okay=True, dir_okay=True, readable=True, allow_dash=True
    ),
    is_eager=True,
    metavar='[PATH(S)]'
)
@click.option(
    '--overwrite/--no-overwrite',
    default=True,
    help='Overwrite source files.',
    show_default=True
)
@click.option(
    '--diff',
    is_flag=True,
    help='Output diff of each processed file.',
    show_default=True
)
@click.option(
    '--check',
    is_flag=True,
    help="Don't overwrite files and just return status. Return code 0 means nothing would change. "
         "Return code 1 means that at least 1 file would change. Any internal error will overwrite this status.",
    show_default=True
)
@click.option(
    '-s',
    '--spacecount',
    type=click.types.INT,
    default=4,
    help='The number of spaces between cells in the plain text format.\n',
    show_default=True
)
@click.option(
    '-l',
    '--lineseparator',
    type=click.types.Choice(['native', 'windows', 'unix']),
    default='native',
    help="Line separator to use in outputs. The default is 'native'.\n"
         "native:  use operating system's native line separators\n"
         "windows: use Windows line separators (CRLF)\n"
         "unix:    use Unix line separators (LF)",
    show_default=True
)
@click.option(
    '-sl',
    '--startline',
    default=None,
    type=int,
    help="Limit robotidy only to selected area. If --endline is not provided, format text only at --startline. "
         "Line numbers start from 1.",
    show_default=True
)
@click.option(
    '-el',
    '--endline',
    default=None,
    type=int,
    help="Limit robotidy only to selected area. "
         "Line numbers start from 1.",
    show_default=True
)
@click.option(
    '-v',
    '--verbose',
    is_flag=True,
    show_default=True
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
    '--list-transformers',
    '--list',
    '-l',
    is_eager=True,
    is_flag=True,
    help='List available transformers and exit.'
)
@click.option(
    '--describe-transformer',
    '--desc',
    '-d',
    default=None,
    metavar='TRANSFORMER_NAME',
    help='Show documentation for selected transformer.'
)
@click.version_option(version=__version__, prog_name='robotidy')
@click.pass_context
def cli(
        ctx: click.Context,
        transform: List[Tuple[str, List]],
        configure: List[Tuple[str, List]],
        src: Tuple[str, ...],
        overwrite: bool,
        diff: bool,
        check: bool,
        spacecount: int,
        lineseparator: str,
        verbose: bool,
        config: Optional[str],
        startline: Optional[int],
        endline: Optional[int],
        list_transformers: bool,
        describe_transformer: Optional[str]
):
    if list_transformers:
        transformers = load_transformers(None, {})
        click.echo('Run --desc <transformer_name> to get more details. Transformers:')
        for transformer in transformers:
            click.echo(transformer.__class__.__name__)
        ctx.exit(0)
    if describe_transformer is not None:
        transformers = load_transformers(None, {})
        transformer_by_names = {transformer.__class__.__name__: transformer for transformer in transformers}
        if describe_transformer in transformer_by_names:
            click.echo(f"Transformer {describe_transformer}:")
            click.echo(remove_rst_formatting(transformer_by_names[describe_transformer].__doc__))
        else:
            click.echo(f"Transformer with the name '{describe_transformer}' does not exist")
        ctx.exit(0)

    if config and verbose:
        click.echo(f'Loaded {config} configuration file')

    formatting_config = GlobalFormattingConfig(
        space_count=spacecount,
        line_sep=lineseparator,
        start_line=startline,
        end_line=endline
    )
    tidy = Robotidy(
        transformers=transform,
        transformers_config=configure,
        src=src,
        overwrite=overwrite,
        show_diff=diff,
        formatting_config=formatting_config,
        verbose=verbose,
        check=check
    )
    status = tidy.transform_files()
    ctx.exit(status)
