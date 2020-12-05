import click
from robotidy.version import __version__
from robotidy.app import Robotidy
from robotidy.transformers import load_transfomers_names


@click.command()
@click.option(
    '--transformer',
    type=click.Choice(load_transfomers_names(), case_sensitive=False),
    required=True,
    multiple=True
)
@click.version_option(__version__)
def cli(transformer):
    tidy = Robotidy(transformer)
    print(tidy.transformers)
