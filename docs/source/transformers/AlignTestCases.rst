.. _AlignTestCases:

AlignTestCases
================================

Align Test Cases to columns.

AlignTestCases is not included in default transformers that's why you need to call it with ``--transform`` explicitly::

    robotidy --transform AlignTestCases src

Or configure `enable` parameter::

    robotidy --configure AlignTestCases:enabled=True

Currently only templated tests are supported. Examples:

.. tabs::

   .. code-tab:: robotframework Before

        *** Settings ***
        Test Template    Templated Keyword

        *** Test Cases ***    baz    qux
        # some comment
        test1    hi    hello
        test2 long test name    asdfasdf    asdsdfgsdfg

   .. code-tab:: robotframework After

        *** Settings ***
        Test Template    Templated Keyword

        *** Test Cases ***      baz         qux
        # some comment
        test1                   hi          hello
        test2 long test name    asdfasdf    asdsdfgsdfg
                                bar1        bar2

.. tabs::

   .. code-tab:: robotframework Before

        *** Settings ***
        Test Template    Dummy

        *** Test Cases ***
        Test1    ARG1
            [Tags]    sanity
            [Documentation]  Validate Test1
        Test2    ARG2
            [Tags]    smoke
            [Documentation]  Validate Test2

   .. code-tab:: robotframework After


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
If you don't want to align test case section that does not contain header names then configure `only_with_headers` parameter::

    robotidy -c AlignSettingsSection:only_with_hedaers:True <src>

Supports global formatting params: ``--startline``, ``--endline``.
