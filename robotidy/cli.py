import click
from robotidy.version import __version__
from robotidy.app import Robotidy
from robotidy.transformers import load_transfomers_names


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


@click.command()
@click.option(
    '--transform',
    type=TransformType(),
    multiple=True
)
@click.version_option(__version__)
def cli(transform):
    tidy = Robotidy(transform)
    print(tidy.transformers)
    print(tidy.transformers['DummyTransformer'].some_value)
    tidy.transformers['DummyTransformer'].some_value = 5
    print(tidy.transformers['DummyTransformer'].some_value)
