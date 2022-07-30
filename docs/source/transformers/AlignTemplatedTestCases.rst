.. _AlignTemplatedTestCases:

AlignTemplatedTestCases
================================

Align templated Test Cases to columns.

For non-templated test cases use ``AlignTestCasesSection`` transformer.

.. |TRANSFORMERNAME| replace:: AlignTestCases
.. include:: disabled_hint.txt

Examples:

.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

            *** Settings ***
            Test Template    Templated Keyword

            *** Test Cases ***    baz    qux
            # some comment
            test1    hi    hello
            test2 long test name    asdfasdf    asdsdfgsdfg

    .. tab-item:: After

        .. code:: robotframework

            *** Settings ***
            Test Template    Templated Keyword

            *** Test Cases ***      baz         qux
            # some comment
            test1                   hi          hello
            test2 long test name    asdfasdf    asdsdfgsdfg
                                    bar1        bar2

.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

            *** Settings ***
            Test Template    Dummy

            *** Test Cases ***
            Test1    ARG1
                [Tags]    sanity
                [Documentation]  Validate Test1
            Test2    ARG2
                [Tags]    smoke
                [Documentation]  Validate Test2

    .. tab-item:: After

        .. code:: robotframework

            *** Settings ***
            Test Template    Dummy

            *** Test Cases ***
            Test1     ARG1
                      [Tags]              sanity
                      [Documentation]     Validate Test1
            Test2     ARG2
                      [Tags]              smoke
                      [Documentation]     Validate Test2

Align only test case section with named headers
------------------------------------------------
If you don't want to align test case section that does not contain header names then configure ``only_with_headers`` parameter::

    robotidy -c AlignSettingsSection:only_with_hedaers=True <src>

Fixed width of column
-------------------------
It's possible to set fixed minimal width of column. To configure it use ``min_width`` parameter::

    robotidy --configure AlignTestCases:min_width=30 src

This configuration respects ``up_to_column`` parameter.

.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

            *** Test Cases ***    baz    qux
            # some comment
            test1    hi    hello
            test2 long test name    asdfasdf    asdsdfgsdfg
                bar1  bar2

    .. tab-item:: After

        .. code:: robotframework

            *** Test Cases ***            baz                           qux
            # some comment
            test1                         hi                            hello
            test2 long test name          asdfasdf                      asdsdfgsdfg
                                          bar1                          bar2
