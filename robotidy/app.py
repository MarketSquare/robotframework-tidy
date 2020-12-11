from typing import List, Tuple, Dict, Set
from difflib import unified_diff

import click
from robot.api import get_model
from robot.parsing.model.visitor import ModelVisitor
from robotidy.transformers import load_transformers


class StatementLinesCollector(ModelVisitor):
    def __init__(self, model):
        self.text = ''
        self.visit(model)

    def visit_Statement(self, node):  # noqa
        for token in node.tokens:
            self.text += token.value


class Robotidy:
    def __init__(self,
                 transformers: List[Tuple[str, Dict]],
                 src: Set,
                 overwrite: bool,
                 show_diff: bool
                 ):
        self.sources = src
        self.overwrite = overwrite
        self.show_diff = show_diff
        transformer_names = [transformer[0] for transformer in transformers]
        self.transformers = load_transformers(set(transformer_names))
        self.configure_transformers(transformers)

    def configure_transformers(self, transformer_config: List[Tuple[str, Dict]]):
        for name, params in transformer_config:
            if not params:
                continue
            for param_name, value in params.items():
                if param_name in self.transformers[name].configurables:
                    setattr(self.transformers[name], param_name, value)
                else:
                    raise ValueError(f"Invalid configurable name: '{param_name}' for transformer: '{name}'")

    def transform_files(self):
        for source in self.sources:
            model = get_model(source)
            old_model = StatementLinesCollector(model)
            for transformer in self.transformers.values():
                transformer.visit(model)
            new_model = StatementLinesCollector(model)
            self.output_diff(model.source, old_model, new_model)
            self.save_model(model)

    def save_model(self, model):
        if self.overwrite:
            model.save()

    def output_diff(self, path: str, old_model: StatementLinesCollector, new_model: StatementLinesCollector):
        if not self.show_diff:
            return
        old = old_model.text.splitlines()
        new = new_model.text.splitlines()
        lines = [line for line in unified_diff(old, new, fromfile=f'{path}\tbefore', tofile=f'{path}\tafter')]
        colorized_output = self.color_diff(lines)
        # click.echo(colorized_output, color=True) FIXME: does not display colours
        print(colorized_output)

    def color_diff(self, contents: List[str]) -> str:
        """Inject the ANSI color codes to the diff."""
        for i, line in enumerate(contents):
            if line.startswith("+++") or line.startswith("---"):
                line = f"\033[1;37m{line}\033[0m"  # bold white, reset
            elif line.startswith("@@"):
                line = f"\033[36m{line}\033[0m"  # cyan, reset
            elif line.startswith("+"):
                line = f"\033[32m{line}\033[0m"  # green, reset
            elif line.startswith("-"):
                line = f"\033[31m{line}\033[0m"  # red, reset
            contents[i] = line
        return '\n'.join(contents)
