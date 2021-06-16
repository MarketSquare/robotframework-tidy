.. _SplitTooLongLine:

SplitTooLongLine
================================

Split too long lines.
If any line in keyword call exceeds given length limit (configurable using ``line_length``, 120 by default) it will be
split::

    Keyword With Longer Name    ${arg1}    ${arg2}    ${arg3}  # let's assume that arg2 is at 120 char

To::

    Keyword With Longer Name    ${arg1}
    ...    ${arg2}    ${arg3}

Using ``split_on_every_arg`` flag (``False`` by default), you can force the formatter to put every argument in a new line::

    Keyword With Longer Name
    ...    ${arg1}
    ...    ${arg2}
    ...    ${arg3}

Supports global formatting params: ``space_count``, ``--startline`` and ``--endline``.