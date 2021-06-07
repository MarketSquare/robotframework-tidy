from collections import defaultdict
from difflib import unified_diff
from pathlib import Path
from typing import List, Tuple, Dict, Iterator, Iterable

import click
from robot.api import get_model
from robot.errors import DataError

from robotidy.transformers import load_transformers
from robotidy.utils import (
    StatementLinesCollector,
    decorate_diff_with_color,
    GlobalFormattingConfig
)

INCLUDE_EXT = ('.robot', '.resource')


class Robotidy:
    def __init__(self,
                 transformers: List[Tuple[str, List]],
                 transformers_config: List[Tuple[str, List]],
                 src: Tuple[str, ...],
                 overwrite: bool,
                 show_diff: bool,
                 formatting_config: GlobalFormattingConfig,
                 verbose: bool,
                 check: bool
                 ):
        self.sources = self.get_paths(src)
        self.overwrite = overwrite
        self.show_diff = show_diff
        self.check = check
        self.verbose = verbose
        self.formatting_config = formatting_config
        transformers_config = self.convert_configure(transformers_config)
        self.transformers = load_transformers(transformers, transformers_config)
        for transformer in self.transformers:
            # inject global settings TODO: handle it better
            setattr(transformer, 'formatting_config', self.formatting_config)

    def transform_files(self):
        changed_files = 0
        for source in self.sources:
            try:
                if self.verbose:
                    click.echo(f'Transforming {source} file')
                model = get_model(source)
                diff, old_model, new_model = self.transform(model)
                if diff:
                    changed_files += 1
                self.output_diff(model.source, old_model, new_model)
                if not self.check:
                    self.save_model(model)
            except DataError:
                click.echo(
                    f"Failed to decode {source}. Default supported encoding by Robot Framework is UTF-8. Skipping file"
                )
                pass
        if not self.check or not changed_files:
            return 0
        return 1

    def transform(self, model):
        old_model = StatementLinesCollector(model)
        for transformer in self.transformers:
            transformer.visit(model)
        new_model = StatementLinesCollector(model)
        return new_model != old_model, old_model, new_model

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
        click.echo(colorized_output.encode('ascii', 'ignore').decode('ascii'), color=True)

    def get_paths(self, src: Tuple[str, ...]):
        sources = set()
        for s in src:
            path = Path(s).resolve()
            if path.is_file():
                sources.add(path)
            elif path.is_dir():
                sources.update(self.iterate_dir(path.iterdir()))
            elif s == '-':
                sources.add(path)

        return sources

    def iterate_dir(self, paths: Iterable[Path]) -> Iterator[Path]:
        for path in paths:
            if path.is_file():
                if path.suffix not in INCLUDE_EXT:
                    continue
                yield path
            elif path.is_dir():
                yield from self.iterate_dir(path.iterdir())

    @staticmethod
    def convert_configure(configure: List[Tuple[str, List]]) -> Dict[str, List]:
        config_map = defaultdict(list)
        for transformer, args in configure:
            config_map[transformer].extend(args)
        return config_map
