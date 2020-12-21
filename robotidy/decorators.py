import inspect
import functools

from robotidy.utils import node_within_lines


class ConfigurableDecorator:
    def __init__(self, fun, **kwargs):
        self.fun = fun
        if 'default' in kwargs:
            self._value = kwargs['default']

    def __set_name__(self, owner, name):
        if not hasattr(owner, 'configurables'):
            owner.configurables = set()
        owner.configurables.add(name)

    def __set__(self, obj, value):
        self._value = self.fun(obj, value)
        return self._value

    def __get__(self, instance, owner):
        try:
            return self._value
        except AttributeError:
            raise AttributeError(f'{owner.__name__}.{self.fun.__name__} attribute was not initialized before use')


def configurable(function=None, **kwargs):
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

    It is possible to pass default value with `default=` argument::

        @configurable(default=10)

    If the same value is initialized also in `__init__` it will be overridden in `__init__`.
    The main difference is that if you set it in `__init__` it will go through parsing method (`some_value`).
    On the other hand `default=` saves value directly.
    """
    if function:
        return ConfigurableDecorator(function)
    else:
        def wrapper(function):
            return ConfigurableDecorator(function, **kwargs)

        return wrapper


def transformer(arg=None):
    """Decorator for transformer class. Only decorated classes are loaded and used to transform the source code."""

    # it allows to use transformer without ()
    if inspect.isclass(arg):
        return transformer()(arg)

    def decorator(cls):
        cls.is_transformer = True
        return cls

    return decorator


def return_node_untouched(node):
    return node


def check_start_end_line(func):
    """
    Do not transform node if it's not within passed start_line and end_line.
    """
    @functools.wraps(func)
    def wrapper(self, node):
        if not node_within_lines(
                node.lineno,
                node.end_lineno,
                self.formatting_config.start_line,
                self.formatting_config.end_line
        ):
            return return_node_untouched(node)
        return func(self, node)
    return wrapper
