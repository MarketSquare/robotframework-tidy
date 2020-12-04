import click
from robotidy.version import __version__
from robotidy.app import Robotidy
from robotidy.transformers import load_transfomers_names


@click.command()
@click.option(
    '--mode',
    type=click.Choice(load_transfomers_names(), case_sensitive=False),
    required=True,
    multiple=True
)
@click.version_option(__version__)
def cli(mode):
    tidy = Robotidy(mode)
    print(tidy.transformers)
