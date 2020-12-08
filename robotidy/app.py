from robotidy.transformers import load_transformers


class Robotidy:
    def __init__(self, transformers):
        transformer_names = [transformer[0] for transformer in transformers]
        self.transformers = load_transformers(set(transformer_names))
        self.configure_transformers(transformers)

    def configure_transformers(self, transformer_config):
        for name, params in transformer_config:
            if not params:
                continue
            for param_name, value in params.items():
                if param_name in self.transformers[name].configurables:
                    setattr(self.transformers[name], param_name, value)
                else:
                    raise ValueError(f"Invalid configurable name: '{param_name}' for transformer: '{name}'")
