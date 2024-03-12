.. _disablers:

Disablers
=========

.. rubric:: Disablers

You can disable formatting of statement or in span of lines using ``# robotidy: off`` marker.

To skip the formatting for one statement:

.. code-block:: robotframework

    Keyword That Is Longer Than Allowed Line Length  ${arg}  # robotidy: off

To skip multiple lines:

.. code-block:: robotframework

    *** Test Cases ***
    Test that will be formatted
        Step

    # robotidy: off
    Test that will not be formatted
        Step

    # robotidy: on
    Another test that will be formatted
        Step

You can also disable the formatting in the whole section if you put ``# robotidy: off`` in the section header:

.. code-block:: robotframework

    *** Test Cases ***
    Formatted
        Step

    *** Keywords ***  # robotidy: off
    Not Formatted
        Step

Enable formatting again
------------------------

``# robotidy: on`` marker is used to enable the formatting again - but is not required. ``# robotidy: off`` will disable
the formatting to the end of the current block:

.. code-block:: robotframework

    *** Keywords ***
    Keyword
        Keyword That Is Formatted
        IF    $condition
            Formatted
        ELSE
            Formatted
            # robotidy: off
            Not Formatted
            WHILE    $condition
                Not Formatted
            END
        END
        Formatted

Disable only selected transformers
-----------------------------------

It is possible to disable only selected transformers by passing their names to disabler in comma separated list:

.. code-block:: robotframework

    *** Test Cases ***
    Formatted Partially
        Step
        ...    ${arg}  # robotidy: off=AlignTestCasesSection,NormalizeSeparators
        Step 2

    *** Keywords ***  # robotidy: off = NormalizeNewLines
    Not Formatted
        Step

Disable formatting of whole file
--------------------------------

It's possible to disable the formatting in whole file by putting ``# robotidy: off`` on the first line:

.. code-block:: robotframework

    # robotidy: off
    *** Settings ***
    Library    Collections

File disablers can be also placed in first comment section in the file:

.. code-block:: robotframework

    *** Comments ***
    # Following line disables formatting this file with Robotidy
    # robotidy: off

    *** Settings ***
    Library    Collections

File disablers supports also disabling selected transformers:

.. code-block:: robotframework

    # robotidy: off = RenameVariables

    *** Settings ***
    Library    Collections
