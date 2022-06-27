.. _AlignTestCasesSection:

AlignTestCasesSection
================================
Align ``*** Test Cases ***`` section to columns.


.. |TRANSFORMERNAME| replace:: _AlignTestCasesSection
.. include:: enabled_hint.txt


Align keyword calls and settings into columns with predefined width in non-templated test cases.
There are two possible alignment types (configurable via ``alignment_type``):

- ``fixed`` (default): pad the tokens to the fixed width of the column
- ``auto``: pad the tokens to the width of the longest token in the column

The width of the column sets limit to the maximum width of the column. Default width is ``24``
(see :ref:`widths tests` for information how to configure it).

With ``fixed`` alignment each column have fixed width (and tokens that does not fit
go into ``overflow`` state - see :ref:`overflow tests`).

``auto`` alignment align tokens to the longest token in the column - the column width can be shorter than
configured width (but no longer).

See examples of the alignment types:

.. tabs::

    .. code-tab:: robotframework Before

        *** Test Cases ***
        Test case
            ${short}    Short Keyword    short arg
            ${other_val}    Short Keyword
            ...    arg
            ...    value

    .. code-tab:: robotframework ``fixed`` (default)

        *** Test Cases ***
        Test case
            ${short}                Short Keyword           short arg
            ${other_val}            Short Keyword
            ...                     arg
            ...                     value

    .. code-tab:: robotframework ``auto``

        *** Test Cases ***
        Test case
            ${short}        Short Keyword       short arg
            ${other_val}    Short Keyword
            ...             arg
            ...             value

The ``auto`` alignment often leads to more compact code. But ``fixed`` setting offers more stability - adding new,
slightly longer variable or keyword call will not change alignment of the other lines.

.. _widths tests:

Widths
-------
The column width is configurable via ``widths`` parameter. The default value is ``24``.
It's possible to configure width of the several columns (using comma separated list of integers)::

    robotidy -c AlignKeywordsSection:widths=20

::

    robotidy -c AlignKeywordsSection:widths=10,10,24,30

The last width will be used for the remaining columns. In previous example we configured widths for the 4 columns.
The last width (``30``) will be used for 5th, 6th.. and following columns.

Use width ``0`` to disable column width limit. In ``auto`` alignment type it will always align whole column to the
longest token (no matter how long the token is).

.. _overflow tests:

Overflow
---------
Tokens that do not fit in the column go into ``overflow`` state. There are several ways to deal with them (configurable
via ``handle_too_long`` parameter):

- ``overflow`` (default): align token to the next column
- ``compact_overflow``: try to fit next token between current (overflowed) token and the next column
- ``ignore_rest``: ignore remaining tokens in the line
- ``ignore_line``: ignore whole line

See example (for ``fixed`` alignment type and default width ``24``):

.. tabs::

    .. code-tab:: robotframework Before

        *** Test Cases ***
        Test case
            # keyword call Looo.. does not fit default column width (24)
            ${assign}    Looooooooonger Keyword Name    ${argument}    last
            Short    Short    Short    Short
            Single
            Multi    ${arg}
            ...    ${arg}

    .. code-tab:: robotframework ``overflow`` (default)

        *** Test Cases ***
        Test case
            # we are "overflowing" to the next column - taking 24 * 2 = 48 width
            ${assign}               Looooooooonger Keyword Name                     ${argument}             Short
            Short                   Short                   Short                   Short
            Single
            Multi                   ${arg}
            ...                     ${arg}

    .. code-tab:: robotframework compact_overflow

        *** Test Cases ***
        Test case
            # ${argument} is fit between columns, and next argument ("last") is aligned correctly
            ${assign}               Looooooooonger Keyword Name    ${argument}      last
            Short                   Short                   Short                   Short
            Single
            Multi                   ${arg}
            ...                     ${arg}

    .. code-tab:: robotframework ignore_rest

        *** Test Cases ***
        Test case
            # tokens after too long token are not aligned
            ${assign}               Looooooooonger Keyword Name    ${argument}    Short
            Short                   Short                   Short                   Short
            Single
            Multi                   ${arg}
            ...                     ${arg}

    .. code-tab:: robotframework ignore_line

        *** Test Cases ***
        Test case
            # the wole line containing too long token is ignored
            ${assign}    Looooooooonger Keyword Name    ${argument}    Short
            Short                   Short                   Short                   Short
            Single
            Multi                   ${arg}
            ...                     ${arg}


Alignment of the indented blocks
--------------------------------
Indented blocks (``FOR``, ``IF``, ``WHILE``, ``TRY..EXCEPT..``) are aligned independently.

.. tabs::

    .. code-tab:: robotframework Before

        *** Test Cases ***
        Test case
            ${assign}    Keyword
            FOR  ${var}  IN  1  2  3
               ${variable}    Keyword    ${var}
               Another Keyword
               FOR  ${var2}  IN  1  2  3
                   Short   1   2
                   ${assign}    Longer Keyword
                   ...    ${multiline}    ${arg}
               END
            END
           Keyword Call    ${value}  # aligned together with keyword call before FOR loop

    .. code-tab:: robotframework Before

        *** Test Cases ***
        Test case
            ${assign}               Keyword
            FOR    ${var}    IN    1    2    3
                ${variable}             Keyword                 ${var}
                Another Keyword
                FOR    ${var2}    IN    1    2    3
                    Short                   1                       2
                    ${assign}               Longer Keyword
                    ...                     ${multiline}            ${arg}
                END
            END
            Keyword Call            ${value}  # aligned together with keyword call before FOR loop

Currently, inline IFs are ignored. Block headers (``FOR ${var} IN @{LIST}`` or ``IF  $condition``) are not aligned.

Split too long lines
---------------------
``AlignTestCasesSection`` will split the lines if the lines after the alignment would exceed the limits set
in the :ref:`SplitTooLongLine` transformer.

.. note::
    Currently, only ``--configure SplitTooLongLine:split_on_every_arg=True`` mode is supported.

Using this configuration (``SplitTooLongLine`` is enabled by default)::

    robotidy -c AlignTestCasesSection:enabled=True:widths=14,24 --line-length 80 src

will result in the following transformation:

.. tabs::

    .. code-tab:: robotframework Before

        *** Test Cases ***
        Test case
            # fits now but it will not fit after the alignment
            Keyword    argument1    argument2    argument3    argument4

            # does not fit before the alignment
            Longer Keyword Name That Could Happen    argument value with sentence that goes over

            # fits, will not be split
            Keyword    argument

    .. code-tab:: robotframework After

        *** Test Cases ***
        Test case
            # fits now but it will not fit after the alignment
            Keyword
            ...           argument1
            ...           argument2
            ...           argument3
            ...           argument4

            # does not fit before the alignment
            Longer Keyword Name That Could Happen
            ...           argument value with sentence that goes over

            # fits, will be aligned but not split
            Keyword       argument


Skip formatting
----------------
It is possible to use the following arguments to skip formatting of the code:

- :ref:`skip documentation`
- :ref:`skip return values`
- :ref:`skip keyword call`
- :ref:`skip keyword call pattern`
- :ref:`skip settings`

It is highly recommended to use one of the ``skip`` options if you wish to use the alignment but you have part of the code
that looks better with manual alignment. It is also possible to use disablers (:ref:`disablers`) but ``skip`` option
makes it easier to skip all instances of given type of the code.
