from typing import List, Tuple, Dict, Set
from robot.api import get_model
from robotidy.transformers import load_transformers


class Robotidy:
    def __init__(self,
                 transformers: List[Tuple[str, Dict]],
                 src: Set,
                 overwrite: bool
                 ):
        self.sources = src
        self.overwrite = overwrite
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
            for transformer in self.transformers.values():
                transformer.visit(model)
            model.save()

    def save_model(self, model):
        if self.overwrite:
            model.save()
