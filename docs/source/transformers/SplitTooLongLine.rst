.. _SplitTooLongLine:

SplitTooLongLine
================================

Split too long lines.

.. |TRANSFORMERNAME| replace:: SplitTooLongLine
.. include:: enabled_hint.txt

If any line in keyword call exceeds given length limit (configurable using ``line_length``, 120 by default) it will be
split.

.. tabs::

    .. code-tab:: robotframework Before

        Keyword With Longer Name    ${arg1}    ${arg2}    ${arg3}  # let's assume that arg2 is at 120 char

    .. code-tab:: robotframework After

        Keyword With Longer Name    ${arg1}
        ...    ${arg2}    ${arg3}

Using ``split_on_every_arg`` flag (``False`` by default), you can force the formatter to put every argument in a new line::

    robotidy --configure SplitTooLongLine:split_on_every_arg=True src

.. tabs::

    .. code-tab:: robotframework Before

        Keyword With Longer Name    ${arg1}    ${arg2}    ${arg3}  # let's assume that arg2 is at 120 char

    .. code-tab:: robotframework After

        Keyword With Longer Name
        ...    ${arg1}
        ...    ${arg2}
        ...    ${arg3}

Supports global formatting params: ``spacecount``, ``--startline`` and ``--endline``.