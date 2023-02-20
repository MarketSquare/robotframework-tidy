import os
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Pattern, Tuple

try:
    from robot.api import Languages  # RF 6.0
except ImportError:
    Languages = None

from robotidy.files import get_paths
from robotidy.transformers import load_transformers


class FormattingConfig:
    def __init__(
        self,
        space_count: int,
        indent: Optional[int],
        continuation_indent: Optional[int],
        line_sep: str,
        start_line: Optional[int],
        end_line: Optional[int],
        separator: str,
        line_length: int,
    ):
        self.start_line = start_line
        self.end_line = end_line
        self.space_count = space_count
        self.line_length = line_length

        if indent is None:
            indent = space_count
        if continuation_indent is None:
            continuation_indent = space_count

        if separator == "space":
            self.separator = " " * space_count
            self.indent = " " * indent
            self.continuation_indent = " " * continuation_indent
        elif separator == "tab":
            self.separator = "\t"
            self.indent = "\t"
            self.continuation_indent = "\t"

        self.line_sep = self.get_line_sep(line_sep)

    @staticmethod
    def get_line_sep(line_sep):
        if line_sep == "windows":
            return "\r\n"
        elif line_sep == "unix":
            return "\n"
        elif line_sep == "auto":
            return "auto"
        else:
            return os.linesep


class Config:
    def __init__(
        self,
        formatting: FormattingConfig,
        skip,
        transformers: List[Tuple[str, List]],
        transformers_config: List[Tuple[str, List]],
        src: Tuple[str, ...],
        exclude: Optional[Pattern],
        extend_exclude: Optional[Pattern],
        skip_gitignore: bool,
        overwrite: bool,
        show_diff: bool,
        verbose: bool,
        check: bool,
        output: Optional[Path],
        force_order: bool,
        target_version: int,
        color: bool,
        language: Optional[List[str]],
    ):
        self.sources = get_paths(src, exclude, extend_exclude, skip_gitignore)
        self.formatting = formatting
        self.overwrite = overwrite
        self.show_diff = show_diff
        self.verbose = verbose
        self.check = check
        self.output = output
        self.color = color
        self.language = self.get_languages(language)
        transformers_config = self.convert_configure(transformers_config)
        self.transformers = []
        self.transformers_lookup = dict()
        self.load_transformers(transformers, transformers_config, force_order, target_version, skip)

    def load_transformers(self, transformers, transformers_config, force_order, target_version, skip):
        transformers = load_transformers(
            transformers, transformers_config, force_order=force_order, target_version=target_version, skip=skip
        )
        for transformer in transformers:
            # inject global settings TODO: handle it better
            setattr(transformer.instance, "formatting_config", self.formatting)
            setattr(transformer.instance, "transformers", self.transformers_lookup)
            setattr(transformer.instance, "languages", self.language)
            self.transformers.append(transformer.instance)
            self.transformers_lookup[transformer.name] = transformer.instance

    @staticmethod
    def convert_configure(configure: List[Tuple[str, List]]) -> Dict[str, List]:
        config_map = defaultdict(list)
        for transformer, args in configure:
            config_map[transformer].extend(args)
        return config_map

    @staticmethod
    def get_languages(lang):
        if Languages is None:
            return None
        return Languages(lang)
