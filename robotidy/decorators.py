class configurable:  # noqa
    def __init__(self, fun):
        self.fun = fun

    def __set_name__(self, owner, name):
        if not hasattr(owner, 'configurables'):
            owner.configurables = set()
        owner.configurables.add(name)

    def __set__(self, obj, value):
        if not obj:
            return self
        self._value = self.fun(obj, value)
        return self._value

    def __get__(self, instance, owner):
        try:
            return self._value
        except AttributeError:
            raise AttributeError(f'{owner.__name__}.{self.fun.__name__} attribute was not initialized before use')


def transformer(cls):
    cls.is_transformer = True
    return cls
