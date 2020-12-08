import inspect


class configurable:  # noqa
    """
    Decorator to expose method as configurable parameter.
    Decorated method should return value.

    Example::

        @configurable
        def some_value(self, value):
            # parsing for value
            return value

        def other_method(self, arg):
           print(self.some_value)
    """
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


def transformer(arg=None):
    """Decorator for transformer class. Only decorated classes are loaded and used to transform the source code."""

    if inspect.isclass(arg):
        return transformer()(arg)

    def decorator(cls):
        cls.is_transformer = True
        return cls

    return decorator
