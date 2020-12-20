import sys
from typing import List, Tuple, Dict, Set
from difflib import unified_diff

import click
from robot.api import get_model

from robotidy.transformers import load_transformers
from robotidy.utils import (
    StatementLinesCollector,
    decorate_diff_with_color,
    GlobalFormattingConfig
)


class Robotidy:
    def __init__(self,
                 transformers: List[Tuple[str, Dict]],
                 src: Set,
                 overwrite: bool,
                 show_diff: bool,
                 formatting_config: GlobalFormattingConfig,
                 verbose: bool
                 ):
        self.sources = src
        self.overwrite = overwrite
        self.show_diff = show_diff
        self.verbose = verbose
        self.formatting_config = formatting_config
        self.transformers = self.find_and_load_transformers(transformers)
        self.configure_transformers(transformers)

    @staticmethod
    def find_and_load_transformers(transformers: List[Tuple[str, Dict]]):
        transformer_names = set(transformer[0] for transformer in transformers)
        transformers = load_transformers(transformer_names)
        if transformer_names and len(transformers) != len(transformer_names):
            missing = sorted(transformer_names.difference(set(transformers)))
            msg = 'Failed to load all requested transformers. Make sure you provided correct name. Missing:\n'
            msg += '\n'.join(missing)
            raise click.BadOptionUsage(
                option_name='transform',
                message=msg
            )
        return transformers

    def configure_transformers(self, transformer_config: List[Tuple[str, Dict]]):
        for name, params in transformer_config:
            if not params:
                continue
            for param_name, value in params.items():
                if param_name in self.transformers[name].configurables:
                    setattr(self.transformers[name], param_name, value)
                else:
                    # TODO: list possible configurables if provided wrong name
                    raise click.BadOptionUsage(
                        option_name='transform',
                        message=f"Invalid configurable name: '{param_name}' for transformer: '{name}'"
                    )

    def transform_files(self):
        for source in self.sources:
            stdin = False
            if str(source) == '-':
                stdin = True
                if self.verbose:
                    click.echo('Loading file from stdin')
                source = self.load_from_stdin()
            elif self.verbose:
                click.echo(f'Transforming {source} file')
            model = get_model(source)
            old_model = StatementLinesCollector(model)
            for transformer in self.transformers.values():
                # inject global settings TODO: handle it better
                setattr(transformer, 'formatting_config', self.formatting_config)
                transformer.visit(model)
            new_model = StatementLinesCollector(model)
            self.output_diff(model.source, old_model, new_model)
            if stdin:
                self.print_to_stdout(new_model)
            else:
                self.save_model(model)

    @staticmethod
    def load_from_stdin() -> str:
        return ''.join(sys.stdin)

    def print_to_stdout(self, collected_lines):
        if not self.show_diff:
            click.echo(collected_lines.text)

    def save_model(self, model):
        if self.overwrite:
            model.save()

    def output_diff(self, path: str, old_model: StatementLinesCollector, new_model: StatementLinesCollector):
        if not self.show_diff:
            return
        old = old_model.text.splitlines()
        new = new_model.text.splitlines()
        lines = list(unified_diff(old, new, fromfile=f'{path}\tbefore', tofile=f'{path}\tafter'))
        colorized_output = decorate_diff_with_color(lines)
        # click.echo(colorized_output, color=True)  # FIXME: does not display colours
        print(colorized_output)
