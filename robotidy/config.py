from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Pattern, Tuple

from robotidy.files import get_paths
from robotidy.transformers import load_transformers


class Config:
    def __init__(
        self,
        formatting,
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
    ):
        self.sources = get_paths(src, exclude, extend_exclude, skip_gitignore)
        self.formatting = formatting
        self.overwrite = overwrite
        self.show_diff = show_diff
        self.verbose = verbose
        self.check = check
        self.output = output
        self.color = color
        transformers_config = self.convert_configure(transformers_config)
        self.transformers = load_transformers(
            transformers, transformers_config, force_order=force_order, target_version=target_version
        )
        for transformer in self.transformers:
            # inject global settings TODO: handle it better
            setattr(transformer, "formatting_config", self.formatting)

    @staticmethod
    def convert_configure(configure: List[Tuple[str, List]]) -> Dict[str, List]:
        config_map = defaultdict(list)
        for transformer, args in configure:
            config_map[transformer].extend(args)
        return config_map
