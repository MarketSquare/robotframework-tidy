.. _configuring-transformers:

Configuring Transformers
========================

Transformers can be configured through two different options: ``--transform`` (``-t``) and ``--configure`` (``-c``). They share the same
syntax for parameter names and values. The main difference is that ``--transform`` is also used to select what
transformers will be used. For example::

    robotidy --transform NormalizeNewLines:test_case_lines=2 src
    robotidy --configure NormalizeNewLines:test_case_lines=2 src

In first command robotidy will run only ``NormalizeNewLines`` transformer and it will configure it with ``test_case_lines = 2``.
In second command robotidy will run all of the transformers and will configure ``NormalizeNewLines`` with ``test_case_lines = 2``.

You can also run all transformers except selected ones. For that you need to configure transformer you want to exclude
with ``enabled`` parameter::

    robotidy --configure TRANSFORMER_NAME:enabled=False src

This parameter can be also used to run non default transformer together with default ones::

    robotidy -c SmartSortKeywords:enabled=True src

.. note::
    To see list of available transformers run:

    .. code-block:: console

        robotidy --list

The basic syntax for supplying parameters is ``TRANSFORMER_NAME:param=value``. You can chain multiple parameters using '``:``'::

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
        "AlignSettingsSection: min_width = 18"
    ]
