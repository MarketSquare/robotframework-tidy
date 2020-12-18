from typing import Tuple, Dict, List, Iterator, Iterable
from pathlib import Path
import click
from robotidy.version import __version__
from robotidy.app import Robotidy
from robotidy.utils import GlobalFormattingConfig


INCLUDE_EXT = ('.robot', '.resource')


class TransformType(click.ParamType):
    name = "transform"

    def convert(self, value, param, ctx):
        name = ''
        try:
            name, *configs = value.split(':')
            if '=' in name:
                raise ValueError
            configurations = {}
            for config in configs:
                key, value = config.split('=', maxsplit=1)
                configurations[key] = value
        except ValueError:
            exc = f'Invalid {name} transformer configuration. ' \
                  f'Parameters should be provided in format name=value, delimited by :'
            raise ValueError(exc)
        return name, configurations


def iterate_dir(paths: Iterable[Path]) -> Iterator[Path]:
    for path in paths:
        if path.is_file():
            if path.suffix not in INCLUDE_EXT:
                continue
            yield path
        elif path.is_dir():
            yield from iterate_dir(path.iterdir())


def get_paths(src: Tuple[str, ...]):
    sources = set()
    for s in src:
        path = Path(s).resolve()
        if path.is_file():
            sources.add(path)
        elif path.is_dir():
            sources.update(iterate_dir(path.iterdir()))
        elif s == '-':
            sources.add(path)

    return sources


@click.command()
@click.option(
    '--transform',
    type=TransformType(),
    multiple=True
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
    help='Overwrite source files.'
)
@click.option(
    '--diff',
    is_flag=True,
    help='Output diff of each processed file.'
)
@click.option(
    '-s',
    '--spacecount',
    type=click.types.INT,
    default=4,
    help='The number of spaces between cells in the plain text format.\n'
         'Default is 4.'
)
@click.option(
    '-l',
    '--lineseparator',
    type=click.types.Choice(['native', 'windows', 'unix']),
    default='native',
    help="Line separator to use in outputs. The default is 'native'.\n"
         "native:  use operating system's native line separators\n"
         "windows: use Windows line separators (CRLF)\n"
         "unix:    use Unix line separators (LF)"
)
@click.option(
    '-p',
    '--usepipes',
    is_flag=True,
    help="Use pipe ('|') as a column separator in the plain text format."
)
@click.version_option(version=__version__, prog_name='robotidy')
@click.pass_context
def cli(
        ctx: click.Context,
        transform: List[Tuple[str, Dict]],
        src: Tuple[str, ...],
        overwrite: bool,
        diff: bool,
        spacecount: int,
        lineseparator: str,
        usepipes: bool
):
    formatting_config = GlobalFormattingConfig(
        use_pipes=usepipes,
        space_count=spacecount,
        line_sep=lineseparator
    )
    sources = get_paths(src)
    tidy = Robotidy(
        transformers=transform,
        src=sources,
        overwrite=overwrite,
        show_diff=diff,
        formatting_config=formatting_config
    )
    tidy.transform_files()

