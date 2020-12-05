from robotidy.transformers import load_transformers


class Robotidy:
    def __init__(self, transformers):
        self.transformers = load_transformers(set(transformers))
