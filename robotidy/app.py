import os
import sys
from collections import defaultdict
from difflib import unified_diff
from pathlib import Path
from typing import Dict, List, Optional, Pattern, Tuple

try:
    import rich_click as click
except ImportError:
    import click

from robot.api import get_model
from robot.errors import DataError

from robotidy.disablers import RegisterDisablers
from robotidy.files import get_paths
from robotidy.transformers import load_transformers
from robotidy.utils import GlobalFormattingConfig, ModelWriter, StatementLinesCollector, decorate_diff_with_color


class Robotidy:
    def __init__(
        self,
        transformers: List[Tuple[str, List]],
        transformers_config: List[Tuple[str, List]],
        src: Tuple[str, ...],
        exclude: Optional[Pattern],
        extend_exclude: Optional[Pattern],
        skip_gitignore: bool,
        overwrite: bool,
        show_diff: bool,
        formatting_config: GlobalFormattingConfig,
        verbose: bool,
        check: bool,
        output: Optional[Path],
        force_order: bool,
        target_version: int,
        color: bool,
    ):
        self.sources = get_paths(src, exclude, extend_exclude, skip_gitignore)
        self.overwrite = overwrite
        self.show_diff = show_diff
        self.check = check
        self.verbose = verbose
        self.formatting_config = formatting_config
        self.output = output
        self.color = color
        transformers_config = self.convert_configure(transformers_config)
        self.transformers = load_transformers(
            transformers, transformers_config, force_order=force_order, target_version=target_version
        )
        for transformer in self.transformers:
            # inject global settings TODO: handle it better
            setattr(transformer, "formatting_config", self.formatting_config)

    def transform_files(self):
        changed_files = 0
        disabler_finder = RegisterDisablers(self.formatting_config.start_line, self.formatting_config.end_line)
        for source in self.sources:
            try:
                stdin = False
                if str(source) == "-":
                    stdin = True
                    if self.verbose:
                        click.echo("Loading file from stdin")
                    source = self.load_from_stdin()
                elif self.verbose:
                    click.echo(f"Transforming {source} file")
                model = get_model(source)
                disabler_finder.visit(model)
                if disabler_finder.file_disabled:
                    continue
                diff, old_model, new_model = self.transform(model, disabler_finder.disablers)
                if diff:
                    changed_files += 1
                self.output_diff(model.source, old_model, new_model)
                if stdin:
                    self.print_to_stdout(new_model)
                elif diff:
                    self.save_model(model.source, model)
            except DataError:
                click.echo(
                    f"Failed to decode {source}. Default supported encoding by Robot Framework is UTF-8. Skipping file"
                )
                pass
        if not self.check or not changed_files:
            return 0
        return 1

    def transform(self, model, disablers):
        old_model = StatementLinesCollector(model)
        for transformer in self.transformers:
            setattr(transformer, "disablers", disablers)  # set dynamically to allow using external transformers
            transformer.visit(model)
        new_model = StatementLinesCollector(model)
        return new_model != old_model, old_model, new_model

    @staticmethod
    def load_from_stdin() -> str:
        return sys.stdin.read()

    def print_to_stdout(self, collected_lines):
        if not self.show_diff:
            click.echo(collected_lines.text)

    def save_model(self, source, model):
        if self.overwrite:
            output = self.output or model.source
            ModelWriter(output=output, newline=self.get_line_ending(source)).write(model)

    def get_line_ending(self, path: str):
        if self.formatting_config.line_sep == "auto":
            with open(path) as f:
                f.readline()
                if f.newlines is None:
                    return os.linesep
                if isinstance(f.newlines, str):
                    return f.newlines
                else:
                    return f.newlines[0]
        return self.formatting_config.line_sep

    def output_diff(
        self,
        path: str,
        old_model: StatementLinesCollector,
        new_model: StatementLinesCollector,
    ):
        if not self.show_diff:
            return
        old = [l + "\n" for l in old_model.text.splitlines()]
        new = [l + "\n" for l in new_model.text.splitlines()]
        lines = list(unified_diff(old, new, fromfile=f"{path}\tbefore", tofile=f"{path}\tafter"))
        if not lines:
            return
        if self.color:
            output = decorate_diff_with_color(lines)
        else:
            output = "".join(lines)
        click.echo(output.encode("ascii", "ignore").decode("ascii"), color=self.color)

    @staticmethod
    def convert_configure(configure: List[Tuple[str, List]]) -> Dict[str, List]:
        config_map = defaultdict(list)
        for transformer, args in configure:
            config_map[transformer].extend(args)
        return config_map
