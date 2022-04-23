.. _NormalizeNewLines:

NormalizeNewLines
================================

Normalize new lines.

.. |TRANSFORMERNAME| replace:: NormalizeNewLines
.. include:: enabled_hint.txt

Ensure that there is exactly:

- ``section_lines = 1`` empty lines between sections,

- ``test_case_lines = 1`` empty lines between test cases,

- ``keyword_lines = test_case_lines`` empty lines between keywords.

Removes empty lines after section (and before any data) and appends 1 empty line at the end of file.

.. tabs::

    .. code-tab:: robotframework Before

        This data is ignored at runtime but should be preserved by Tidy.
        *** Variables ***
        # standalone      comment
        ${VALID}          Value
        # standalone

        *** Test Cases ***


        Test
            [Documentation]    This is a documentation
            ...    in two lines
            Some Lines
            No Operation
            [Teardown]    1 minute    args

        Test Without Arg
        Mid Test
            My Step 1    args    args 2    args 3    args 4    args 5    args 6
            ...    args 7    args 8    args 9    # step 1 comment

        *** Keywords ***
        Keyword
            No Operation
        Other Keyword
        Another Keyword
            There
            Are
            More
        *** Settings ***
        Library  library.py

    .. code-tab:: robotframework After

        This data is ignored at runtime but should be preserved by Tidy.

        *** Variables ***
        # standalone      comment
        ${VALID}          Value
        # standalone

        *** Test Cases ***
        Test
            [Documentation]    This is a documentation
            ...    in two lines
            Some Lines
            No Operation
            [Teardown]    1 minute    args

        Test Without Arg

        Mid Test
            My Step 1    args    args 2    args 3    args 4    args 5    args 6
            ...    args 7    args 8    args 9    # step 1 comment

        *** Keywords ***
        Keyword
            No Operation

        Other Keyword

        Another Keyword
            There
            Are
            More

        *** Settings ***
        Library  library.py

Parameters ``section_lines``, ``test_case_lines`` and ``keyword_lines`` can be configured to other values::

    robotidy --configure NormalizeNewLines:section_lines=3 src

.. tabs::

    .. code-tab:: robotframework Before

        *** Settings ***
        Library  Collections

        *** Keywords ***
        Keyword
            Log  stuff

    .. code-tab:: robotframework After

        *** Settings ***
        Library  Collections



        *** Keywords ***
        Keyword
            Log  stuff


Consecutive empty lines inside settings, variables, keywords and test cases are also removed
(configurable via ``consecutive_lines = 1``).

.. tabs::
    .. code-tab:: robotframework Before

        *** Settings ***

        Resource    resource.robot


        Default Tags    tag

        Documentation    doc




        *** Test Cases ***
        Test Capitalized

            Pass Execution

    .. code-tab:: robotframework After

        *** Settings ***
        Resource    resource.robot

        Default Tags    tag

        Documentation    doc

        *** Test Cases ***
        Test Capitalized
            Pass Execution

If set to 0 all empty lines will be removed::

    robotidy --configure NormalizeNewLines:consecutive_lines=0 src

.. tabs::
    .. code-tab:: robotframework Before

        *** Settings ***

        Resource    resource.robot


        Default Tags    tag

        Documentation    doc




        *** Test Cases ***
        Test Capitalized

            Pass Execution

    .. code-tab:: robotframework After

        *** Settings ***
        Resource    resource.robot
        Default Tags    tag
        Documentation    doc

        *** Test Cases ***
        Test Capitalized
            Pass Execution

If the suite contains Test Template tests will not be separated by empty lines unless ``separate_templated_tests``
is set to True.

.. tabs::

    .. code-tab:: robotframework ``separate_templated_tests=False`` (default)

        *** Settings ***
        Test Template    Template For Tests In This Suite

        *** Test Cases ***
        Test    arg1   arg2
        Test Without Arg
        Mid Test
            My Step 1    args    args 2    args 3

    .. code-tab:: robotframework ``separate_templated_tests=True``

        *** Settings ***
        Test Template    Template For Tests In This Suite

        *** Test Cases ***
        Test    arg1   arg2

        Test Without Arg

        Mid Test
            My Step 1    args    args 2    args 3
