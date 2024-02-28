.. _external-transformers:

External transformers
======================
It is possible to develop your own transformers. You can use module name (if it is installed in your env) or path to
file with class to run external transformers with *robotidy*::

    robotidy --transform MyTransformers.YourCustomTransformer src
    robotidy --transform C:\transformers\YourCustomTransformer2.py src
    robotidy --custom-transformers C:\transformers\YourCustomTransformer2.py src

External transformers can be configured in the same way internal transformers are configured - see :ref:`configuring-transformers`.

You can use both ``--transform`` and ``--custom-transformers`` options to load custom user transformer. The main difference
is that ``--transform`` works like include and will only run transformers listed with ``--transform``. While ``--custom-transformers``
will run default transformers first and then user transformers.

Importing whole modules
---------------------------

Importing transformers from module works similarly to how custom libraries are imported in Robot Framework. If the the
file has the same name as transformer it will be auto imported. For example following import::

    robotidy --custom-transformers CustomFormatter.py src

will auto import class ``CustomFormatter`` from the file.

If the file does not contain class with the same name, it is directory, or it is Python module with ``__init__.py`` file
Robotidy will import multiple transformers. By default it imports every class that inherits from
``robot.api.api.parsing.ModelTransformer`` or ``robotidy.transformers.Transformer`` and executes them in order they
were imported.

Following ``__init__.py``:

  .. code-block:: python

    from robotidy.transformers import Transformer

    from other_file import TransformerB

    class TransformerA(Transformer)

will import TransformerB and TransformerA.

If you want to use different order you can define ``TRANSFORMERS`` list in the ``__init__.py``:

  .. code-block:: python

    TRANSFORMERS = [
        "TransformerA",
        "TransformerB"
    ]

Transformer development
---------------------------

You can use the same syntax ``robotidy`` is using for developing internal transformers. Your transformer should inherit
from ``robotidy.transformers.Transformer`` or ``robot.api.parsing.ModelTransformer`` parent class.

  .. code-block:: python

    from robot.api.parsing import ModelTransformer


    class YourCustomTransformer(ModelTransformer):
        """
        This transformer will remove tests with
        word "deprecated" in the test case name
        """
        def visit_TestCase(self, node):
            if 'deprecated' in node.name:
                return None
            return node

Configurable params should be supplied through ``__init__`` together with the type and default value

  .. code-block:: python

    from robot.api.parsing import EmptyLine, ModelTransformer


    class ExternalTransformer(ModelTransformer):
        """
        This transformer add `param` number of empty lines at the end of
        *** Settings *** section.
        """
        def __init__(self, param: int = 10):
            self.param = param

        def visit_SettingSection(self, node):  # noqa
            empty_line = EmptyLine.from_params()
            node.body += [empty_line] * self.param
            return node

ModelTransformer vs Transformer
--------------------------------
Instead of using RobotFramework ``ModelTransformer`` class directly, it is possible to inherit from Robotidy ``Transformer``
class:

  .. code-block:: python

    from robotidy.transformers import Transformer


    class ExternalTransformer(Transformer):
        pass

``Transformer`` also inherits from ``ModelTransformer`` but provides more utility methods (and better lint support).
