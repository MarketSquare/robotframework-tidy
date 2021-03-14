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
                 verbose: bool,
                 check: bool
                 ):
        self.sources = src
        self.overwrite = overwrite
        self.show_diff = show_diff
        self.check = check
        self.verbose = verbose
        self.formatting_config = formatting_config
        self.transformers = load_transformers(transformers)

    def transform_files(self):
        changed_files = 0
        for source in self.sources:
            if self.verbose:
                click.echo(f'Transforming {source} file')
            model = get_model(source)
            old_model = StatementLinesCollector(model)
            for transformer in self.transformers.values():
                # inject global settings TODO: handle it better
                setattr(transformer, 'formatting_config', self.formatting_config)
                transformer.visit(model)
            new_model = StatementLinesCollector(model)
            if new_model != old_model:
                changed_files += 1
            self.output_diff(model.source, old_model, new_model)
            if not self.check:
                self.save_model(model)
        if not self.check or not changed_files:
            return 0
        return 1

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
