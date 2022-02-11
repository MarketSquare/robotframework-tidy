.. _DiscardEmptySections:

DiscardEmptySections
================================

Remove empty sections.

.. |TRANSFORMERNAME| replace:: DiscardEmptySections
.. include:: enabled_hint.txt

.. tabs::

    .. code-tab:: robotframework Before

        *** Settings ***


        *** Test Cases ***
        Test
            [Documentation]  doc
            [Tags]  sometag
            Pass
            Keyword
            One More


        *** Keywords ***
        # This section is not considered empty.


        *** Variables ***

        *** Comments ***
        robocop: disable=all

    .. code-tab:: robotframework After

        *** Test Cases ***
        Test
            [Documentation]  doc
            [Tags]  sometag
            Pass
            Keyword
            One More


        *** Keywords ***
        # This section is not considered empty.


        *** Comments ***
        robocop: disable=all


Remove sections only with comments
-----------------------------------
Sections are considered empty if there are only empty lines inside.
You can remove sections with only comments by setting ``allow_only_comments`` parameter to False. ``*** Comments ***``
section with only comments is always considered as non-empty::

    robotidy --configure DiscardEmptySection:allow_only_comments=True

.. tabs::

    .. code-tab:: robotframework ``allow_only_comments=True`` (default)

        *** Test Cases ***
        Test
            [Documentation]  doc
            [Tags]  sometag
            Pass
            Keyword
            One More

        *** Keywords ***
        # This section is considered to be empty.

        *** Comments ***
        # robocop: disable=all

    .. code-tab:: robotframework ``allow_only_comments=False``

        *** Test Cases ***
        Test
            [Documentation]  doc
            [Tags]  sometag
            Pass
            Keyword
            One More

        *** Comments ***
        # robocop: disable=all


Supports global formatting params: ``--startline`` and ``--endline``.