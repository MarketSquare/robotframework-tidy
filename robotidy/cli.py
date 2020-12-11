from typing import Tuple, Dict, List, Iterator, Iterable
from pathlib import Path
import click
from robotidy.version import __version__
from robotidy.app import Robotidy


INCLUDE_EXT = ('.robot', '.resource')


class TransformType(click.ParamType):
    name = "transform"

    def convert(self, value, param, ctx):
        name, *configs = value.split(':')
        configurations = {}
        try:
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
        if path.suffix not in INCLUDE_EXT:
            continue
        if path.is_file():
            yield path
        elif path.is_dir():
            yield from iterate_dir(path.iterdir())


def get_paths(src: Tuple[str, ...]):
    sources = set()
    for s in src:
        path = Path(s)
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
    help='Overwrite source files'
)
@click.option(
    '--diff',
    is_flag=True,
    help='Output diff of each processed file'
)
@click.version_option(version=__version__, prog_name='robotidy')
@click.pass_context
def cli(
        ctx: click.Context,
        transform: List[Tuple[str, Dict]],
        src: Tuple[str, ...],
        overwrite: bool,
        diff: bool
):
    sources = get_paths(src)
    tidy = Robotidy(transformers=transform, src=sources, overwrite=overwrite, show_diff=diff)
    tidy.transform_files()

