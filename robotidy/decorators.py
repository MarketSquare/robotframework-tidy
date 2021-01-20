import inspect
import functools

from robotidy.utils import node_within_lines


TRANSFORMERS = set()


def transformer(arg=None):
    """Decorator for transformer class. Only decorated classes are loaded and used to transform the source code."""

    # it allows to use transformer without ()

    if inspect.isclass(arg):
        TRANSFORMERS.add(arg.__name__)
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
