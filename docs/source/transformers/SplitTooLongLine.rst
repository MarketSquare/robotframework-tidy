.. _SplitTooLongLine:

SplitTooLongLine
================================

Split too long lines.

.. |TRANSFORMERNAME| replace:: SplitTooLongLine
.. include:: enabled_hint.txt

If line exceeds given length limit (120 by default) it will be split:

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

Missing functionality
----------------------
``SplitTooLongLine`` does not support splitting all Robot Framework types. Currently it will only work on too
long keyword calls, variables and selected settings (tags and arguments). Missing types will be covered in the future
updates.

Allowed line length
--------------------

Allowed line length is configurable using global parameter ``--line-length``::

    robotidy --line-length 140 src.robot

Or using dedicated for this transformer parameter ``line_length``::

    robotidy --configure SplitTooLongLine:line_length=140 src.robot

Split argument on every line
----------------------------
Using ``split_on_every_arg`` flag (``True`` by default), you can force the formatter to fill keyword arguments
in one line until character limit::

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

Split settings arguments on every line
---------------------------------------
Using ``split_on_every_setting_arg`` flag (``True`` by default), you can force the formatter to fill settings arguments
in one line until character limit::

    robotidy --configure SplitTooLongLine:split_on_every_setting_arg=False src

.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

            *** Keywords ***
            Arguments
                [Arguments]    ${short}    ${veryLongAndJavaLikeArgumentThatWillGoOverAllowedLength}    ${veryLongAndJavaLikeArgumentThatWillGoOverAllowedLength}
                Step

    .. tab-item:: After (default)

        .. code:: robotframework

            *** Keywords ***
            Arguments
                [Arguments]
                ...    ${short}
                ...    ${veryLongAndJavaLikeArgumentThatWillGoOverAllowedLength}
                ...    ${veryLongAndJavaLikeArgumentThatWillGoOverAllowedLength}
                Step

    .. tab-item:: After (split_on_every_setting_arg set to False)

        .. code:: robotframework

            *** Keywords ***
            Arguments
                [Arguments]    ${short}    ${veryLongAndJavaLikeArgumentThatWillGoOverAllowedLength}
                ...    ${veryLongAndJavaLikeArgumentThatWillGoOverAllowedLength}
                Step

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

Ignore comments
----------------

To not count length of the comment to line length use :ref:`skip comments` option::

    robotidy --configure SplitTooLongLine:skip_comments=True <src>

This allows to accept and do not format lines that are longer than allowed length because of the added comment.

Skip formatting
----------------
It is possible to use the following arguments to skip formatting of the code:

- :ref:`skip keyword call`
- :ref:`skip keyword call pattern`
- :ref:`skip settings`
- :ref:`skip comments`
- :ref:`skip sections`

It is also possible to use disablers (:ref:`disablers`) but ``skip`` option
makes it easier to skip all instances of given type of the code.
