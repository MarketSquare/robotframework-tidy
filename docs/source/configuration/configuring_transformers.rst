.. _configuring-transformers:

Configuring Transformers
========================

Transformers can be configured through two different options: ``--transform`` and ``--configure``. They share the same
syntax for parameter names and values. The main difference is that ``--transform`` is also used to select what
transformers will be used. For example::

    robotidy --transform NormalizeNewLines:test_case_lines=2 src
    robotidy --configure NormalizeNewLines:test_case_lines=2 src

In first command robotidy will run only ``NormalizeNewLines`` transformer and it will configure it with ``test_case_lines = 2``.
In second command robotidy will run all of the transformers but will configure ``NormalizeNewLines`` with ``test_case_lines = 2``.

.. note::
    To see list of available transformers run:

    .. code-block:: console

        robotidy --list

The basic syntax for supplying parameters is ``TRANSFORMER_NAME:param=value``. You can chain multiple parameters using '``:``'::

    robotidy --configure TRANSFORMER_NAME:param=value:param=value2 src

To see how to configure transformers using configuration files see :ref:`config-file`.