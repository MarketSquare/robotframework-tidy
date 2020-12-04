import click
from robotidy.version import __version__
from robotidy.app import Robotidy
from robotidy.transformers import load_transfomers_names


class CommaSeparated(click.ParamType):
    name = "csv"

    def convert(self, value, param, ctx):
        return set(value.split(','))


@click.command()
@click.option(
    '--mode',
    type=click.Choice(load_transfomers_names(), case_sensitive=False),
    required=True,
    multiple=True
)
@click.version_option(__version__)
def cli(modes):
    tidy = Robotidy(modes)
    print(tidy.transformers)
