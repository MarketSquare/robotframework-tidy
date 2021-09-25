.. _DiscardEmptySections:

DiscardEmptySections
================================

Remove empty sections.

DiscardEmptySections is included in the default transformers but it can be also run separately with::

   robotidy --transform DiscardEmptySections src

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
        # This section is considered to be empty.


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


        *** Comments ***
        robocop: disable=all

Sections are considered empty if there is no data or there are only comments inside (with the exception
for ``*** Comments ***`` section).
You can leave sections with only comments by setting ``allow_only_comments`` parameter to True::

    robotidy --configure DiscardEmptySection:allow_only_comments=True

.. tabs::

    .. code-tab:: robotframework ``allow_only_comments=False`` (default)

        *** Test Cases ***
        Test
            [Documentation]  doc
            [Tags]  sometag
            Pass
            Keyword
            One More

        *** Comments ***
        robocop: disable=all

    .. code-tab:: robotframework ``allow_only_comments=True``

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
        robocop: disable=all

Supports global formatting params: ``--startline`` and ``--endline``.