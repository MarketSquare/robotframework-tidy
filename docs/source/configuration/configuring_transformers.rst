.. _configuring-transformers:

Configuring Transformers
========================

Transformers can be configured through three different options: ``--transform`` (``-t``), ``--load-transformer`` and
``--configure`` (``-c``). They share the same syntax for parameter names and values.

- ``--configure`` simply provides the configuration to the transformer,
- ``--transform`` is used to include only transformers that have ``--transform`` option,
- ``--load-transformer`` is used to load user transformers. Read more at :ref:`external-transformers`.

For example::

    robotidy --transform NormalizeNewLines:test_case_lines=2 src
    robotidy --configure NormalizeNewLines:test_case_lines=2 src
    robotidy --configure NormalizeNewLines:test_case_lines=1 --load-transformer MyCustomTransformer.py:param=value src

With first command robotidy will run only ``NormalizeNewLines`` transformer and it will configure it with ``test_case_lines = 2``.

Second command robotidy will run all of the transformers and will configure ``NormalizeNewLines`` with ``test_case_lines = 2``.

Third command will run all of the transformers, configure ``NormalizeNewLines`` with ``test_case_lines = 1`` and
import user transformer ``MyCustomTransformer`` with `param=value` configuration.

You can also run all transformers except selected ones. For that you need to configure transformer you want to exclude
with ``enabled`` parameter::

    robotidy --configure TRANSFORMER_NAME:enabled=False src

This parameter can be also used to run non default transformer together with default ones::

    robotidy -c SmartSortKeywords:enabled=True src

.. note::
    To see list of available transformers run:

    .. code-block:: console

        robotidy --list

The basic syntax for supplying parameters is ``TRANSFORMER_NAME:param=value``. You can chain multiple parameters using ``:``::

    robotidy --configure TRANSFORMER_NAME:param=value:param=value2 src

To see how to configure transformers using configuration files see :ref:`config-file`.

Migrating from robot.tidy
-------------------------
If you want to achieve the output closest to the output from old robot.tidy use following configuration::

    [tool.robotidy]
    configure = [
        "MergeAndOrderSections: order = settings,variables,testcases,keywords,comments",
        "OrderSettings: keyword_before = arguments,documentation,tags,timeout",
        "OrderSettingsSection: new_lines_between_groups = 0",
        "AlignSettingsSection: min_width = 18",
        "AlignVariablesSection: min_width = 18"
    ]
