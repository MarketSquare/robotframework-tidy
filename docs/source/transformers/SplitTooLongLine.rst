.. _SplitTooLongLine:

SplitTooLongLine
================================

Split too long lines.

.. |TRANSFORMERNAME| replace:: SplitTooLongLine
.. include:: enabled_hint.txt

If any line in the keyword call or variable exceeds given length limit (120 by default) it will be
split:

.. tabs::

    .. code-tab:: robotframework Before

        *** Variables ***
        @{LIST}    value    value2    value3  # let's assume that value2 is at 120 char

        *** Keywords ***
        Keyword
            Keyword With Longer Name    ${arg1}    ${arg2}    ${arg3}  # let's assume that arg2 is at 120 char

    .. code-tab:: robotframework After

        *** Variables ***
        # let's assume that value2 is at 120 char
        @{LIST}
        ...    value
        ...    value2
        ...    value3

        *** Keywords ***
        Keyword
            # let's assume that arg2 is at 120 char
            Keyword With Longer Name
            ...    ${arg1}
            ...    ${arg2}
            ...    ${arg3}

Allowed line length
--------------------

Allowed line length is configurable using global parameter ``--line-length``::

    robotidy --line-length 140 src.robot

Or using dedicated for this transformer parameter ``line_length``::

    robotidy --configure SplitTooLongLine:line_length=140 src.robot

Split argument on every line
----------------------------
Using ``split_on_every_arg`` flag (``True`` by default), you can force the formatter to fill arguments in one line
until character limit::

    robotidy --configure SplitTooLongLine:split_on_every_arg=False src

.. tabs::

    .. code-tab:: robotframework Before

        *** Keywords ***
        Keyword
            Keyword With Longer Name    ${arg1}    ${arg2}    ${arg3}  # let's assume that arg2 is at 120 char

    .. code-tab:: robotframework After

        *** Keywords ***
        Keyword
            # let's assume that arg2 is at 120 char
            Keyword With Longer Name    ${arg1}
            ...    ${arg2}    ${arg3}

Split values on every line
--------------------------
Using ``split_on_every_value`` flag (``True`` by default), you can force the formatter to fill values in one line
until character limit::

    robotidy --configure SplitTooLongLine:split_on_every_value=False src

.. tabs::

    .. code-tab:: robotframework Before

        *** Variables ***
        # let's assume character limit is at age=12
        &{USER_PROFILE}    name=John Doe    age=12     hobby=coding

    .. code-tab:: robotframework After

        *** Variables ***
        # let's assume character limit is at age=12
        &{USER_PROFILE}    name=John Doe    age=12
        ...    hobby=coding

Assignments
------------
Assignments will be split to multi lines if they don't fit together with Keyword in one line:

.. tabs::

    .. code-tab:: robotframework Before

        *** Keywords ***
        Keyword
            ${first_assignment}    ${second_assignment}    Some Lengthy Keyword So That This Line Is Too Long    ${arg1}    ${arg2}

            ${first_assignment}    ${second_assignment}    ${third_assignment}    Some Lengthy Keyword So That This Line Is Too Long And Bit Over    ${arg1}    ${arg2}

    .. code-tab:: robotframework After

        *** Keywords ***
        Keyword
            ${first_assignment}    ${second_assignment}    Some Lengthy Keyword So That This Line Is Too Long
            ...    ${arg1}
            ...    ${arg2}

            ${first_assignment}
            ...    ${second_assignment}
            ...    ${third_assignment}
            ...    Some Lengthy Keyword So That This Line Is Too Long And Bit Over
            ...    ${arg1}
            ...    ${arg2}

Supports global formatting params: ``spacecount``, ``--startline`` and ``--endline``.