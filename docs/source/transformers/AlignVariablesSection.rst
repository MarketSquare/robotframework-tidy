.. _AlignVariablesSection:

AlignVariablesSection
==================================

Align variables in ``*** Variables ***`` section to columns.

.. |TRANSFORMERNAME| replace:: AlignVariablesSection
.. include:: enabled_hint.txt

.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

            *** Variables ***
            ${VAR}  1
            ${LONGER_NAME}  2
            &{MULTILINE}  a=b
            ...  b=c

    .. tab-item:: After

        .. code:: robotframework

            *** Variables ***
            ${VAR}          1
            ${LONGER_NAME}  2
            &{MULTILINE}    a=b
            ...             b=c

Align up to columns
-------------------
You can configure how many columns should be aligned to longest token in given column. The remaining columns
will use fixed length separator length ``--spacecount``. By default only first two columns are aligned.

Example of how AlignVariablesSection transformer behaves with default configuration and multiple columns:

.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

            *** Variables ***
            ${VARIABLE 1}  10  # comment
            @{LIST}  a  b  c  d
            ${LONGER_NAME_THAT_GOES_AND_GOES}    longer value that goes and goes

    .. tab-item:: After

        .. code:: robotframework

            *** Variables ***
            ${VARIABLE 1}                           10    # comment
            @{LIST}                                 a    b    c    d
            ${LONGER_NAME_THAT_GOES_AND_GOES}       longer value that goes and goes

You can configure it to align three columns::

    robotidy --configure AlignVariablesSection:up_to_column=3 src

.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

            *** Variables ***
            ${VARIABLE 1}  10  # comment
            @{LIST}  a  b  c  d
            ${LONGER_NAME_THAT_GOES_AND_GOES}    longer value that goes and goes

    .. tab-item:: After

        .. code:: robotframework

            *** Variables ***
            ${VARIABLE 1}                           10                                  # comment
            @{LIST}                                 a                                   b    c    d
            ${LONGER_NAME_THAT_GOES_AND_GOES}       longer value that goes and goes

To align all columns set ``up_to_column`` to 0.

Select variable types to align
-------------------------------
It is possible to not align variables of given types. You can choose between following types: ``scalar`` (``$``), ``list`` (``@``),
``dict`` (``&``). Invalid variables - such as missing values or not left aligned - will be always aligned no matter the type.
You can configure types to skip using ``skip_types`` parameter::

    robotidy --configure AlignVariablesSection:skip_types=dict,list src

``skip_types`` accepts comma separated list of types.

Using above configuration code will be aligned in following way:

.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

            *** Variables ***
            ${VARIABLE 1}  10  # comment
            @{LIST}  a
            ...    b
            ...    c
            ...    d
            ${LONGER_NAME_THAT_GOES_AND_GOES}    longer value that goes and goes
            &{SOME_DICT}    key=value  key2=value

    .. tab-item:: After

        .. code:: robotframework

            *** Variables ***
            ${VARIABLE 1}                           10    # comment
            @{LIST}  a
            ...    b
            ...    c
            ...    d
            ${LONGER_NAME_THAT_GOES_AND_GOES}       longer value that goes and goes
            &{SOME_DICT}    key=value  key2=value


Fixed width of column
-------------------------
It's possible to set fixed minimal width of column. To configure it use ``min_width`` parameter::

    robotidy --configure AlignVariablesSection:min_width=20 src

This configuration respects ``up_to_column`` parameter:

.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

            *** Variables ***
            # some comment

            ${VARIABLE 1}    10    # comment
            @{LIST}                                 a    b    c    d
            ${LONGER_NAME_THAT_GOES_AND_GOES}       longer value that goes and goes

            &{MULTILINE}    a=b
            ...     b=c
            ...     d=1

    .. tab-item:: After

        .. code:: robotframework

            *** Variables ***
            # some comment

            ${VARIABLE 1}       10    # comment
            @{LIST}             a    b    c    d
            ${LONGER_NAME_THAT_GOES_AND_GOES}    longer value that goes and goes

            &{MULTILINE}        a=b
            ...                 b=c
            ...                 d=1

Select lines to align
-------------------------
AlignVariablesSection does also support global formatting params ``startline`` and ``endline``::

    robotidy --startline 5 --endline 17 --configure AlignVariablesSection:up_to_column=3 src

.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

            *** Settings ***
            Documentation    This is doc


            *** Variables ***
            # some comment

            ${VARIABLE 1}  10  # comment
            @{LIST}  a  b  c  d
            ${LONGER_NAME_THAT_GOES_AND_GOES}    longer value that goes and goes

                       &{MULTILINE}  a=b
            ...  b=c
            ...         d=1

            *** Keywords ***
            Keyword
                Keyword Call

    .. tab-item:: After

        .. code:: robotframework

            *** Settings ***
            Documentation    This is doc


            *** Variables ***
            # some comment

            ${VARIABLE 1}  10  # comment
            @{LIST}  a  b  c  d
            ${LONGER_NAME_THAT_GOES_AND_GOES}       longer value that goes and goes

            &{MULTILINE}                            a=b
            ...                                     b=c
            ...                                     d=1

            *** Keywords ***
            Keyword
                Keyword Call
