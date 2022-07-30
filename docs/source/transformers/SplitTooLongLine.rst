.. _SplitTooLongLine:

SplitTooLongLine
================================

Split too long lines.

.. |TRANSFORMERNAME| replace:: SplitTooLongLine
.. include:: enabled_hint.txt

If any line in the keyword call or variable exceeds given length limit (120 by default) it will be
split:

.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

            *** Variables ***
            @{LIST}    value    value2    value3  # let's assume that value2 is at 120 char

            *** Keywords ***
            Keyword
                Keyword With Longer Name    ${arg1}    ${arg2}    ${arg3}  # let's assume that arg2 is at 120 char

    .. tab-item:: After

        .. code:: robotframework

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

.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

            *** Keywords ***
            Keyword
                Keyword With Longer Name    ${arg1}    ${arg2}    ${arg3}  # let's assume that arg2 is at 120 char

    .. tab-item:: After

        .. code:: robotframework

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

.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

            *** Variables ***
            # let's assume character limit is at age=12
            &{USER_PROFILE}    name=John Doe    age=12     hobby=coding

     .. tab-item:: After

        .. code:: robotframework

            *** Variables ***
            # let's assume character limit is at age=12
            &{USER_PROFILE}    name=John Doe    age=12
            ...    hobby=coding

Assignments
------------
Assignments will be split to multi lines if they don't fit together with Keyword in one line:

.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

            *** Keywords ***
            Keyword
                ${first_assignment}    ${second_assignment}    Some Lengthy Keyword So That This Line Is Too Long    ${arg1}    ${arg2}

                ${first_assignment}    ${second_assignment}    ${third_assignment}    Some Lengthy Keyword So That This Line Is Too Long And Bit Over    ${arg1}    ${arg2}

    .. tab-item:: After

        .. code:: robotframework

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

Skip formatting
----------------
It is possible to use the following arguments to skip formatting of the code:

- :ref:`skip keyword call`
- :ref:`skip keyword call pattern`

It is also possible to use disablers (:ref:`disablers`) but ``skip`` option
makes it easier to skip all instances of given type of the code.
