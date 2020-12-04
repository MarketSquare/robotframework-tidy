from robotidy.transformers import load_transformers


class Robotidy:
    def __init__(self, modes):
        self.transformers = load_transformers(set(modes))
