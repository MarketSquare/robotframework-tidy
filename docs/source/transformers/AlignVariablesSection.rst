.. _AlignVariablesSection:

AlignVariablesSection
==================================

Align variables in ``*** Variables ***`` section to columns.

AlignVariablesSection is included in the default transformers but it can be also run separately with::

   robotidy --transform AlignVariablesSection src

.. tabs::

    .. code-tab:: robotframework Before

        *** Variables ***
        ${VAR}  1
        ${LONGER_NAME}  2
        &{MULTILINE}  a=b
        ...  b=c

    .. code-tab:: robotframework After

        *** Variables ***
        ${VAR}          1
        ${LONGER_NAME}  2
        &{MULTILINE}    a=b
        ...             b=c

Align up to columns
-------------------
You can configure how many columns should be aligned to longest token in given column. The remaining columns
will use fixed length separator length ``--space_count``. By default only first two columns are aligned.

Example of how AlignVariablesSection transformer behaves with default configuration and multiple columns:

.. tabs::

    .. code-tab:: robotframework Before

        *** Variables ***
        ${VARIABLE 1}  10  # comment
        @{LIST}  a  b  c  d
        ${LONGER_NAME_THAT_GOES_AND_GOES}    longer value that goes and goes

    .. code-tab:: robotframework After

        *** Variables ***
        ${VARIABLE 1}                           10    # comment
        @{LIST}                                 a    b    c    d
        ${LONGER_NAME_THAT_GOES_AND_GOES}       longer value that goes and goes

You can configure it to align three columns::

    robotidy --configure AlignVariablesSection:up_to_column=3 src

.. tabs::

    .. code-tab:: robotframework Before

        *** Variables ***
        ${VARIABLE 1}  10  # comment
        @{LIST}  a  b  c  d
        ${LONGER_NAME_THAT_GOES_AND_GOES}    longer value that goes and goes

    .. code-tab:: robotframework After

        *** Variables ***
        ${VARIABLE 1}                           10                                  # comment
        @{LIST}                                 a                                   b    c    d
        ${LONGER_NAME_THAT_GOES_AND_GOES}       longer value that goes and goes

To align all columns set ``up_to_column`` to 0.

Select lines to transform
-------------------------
AlignVariablesSection does also support global formatting params ``startline`` and ``endline``::

    robotidy --startline 5 --endline 17 --configure AlignVariablesSection:up_to_column=3 src

.. tabs::

    .. code-tab:: robotframework Before

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

    .. code-tab:: robotframework After

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
