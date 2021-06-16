.. _NormalizeSettingName:

NormalizeSettingName
================================

Normalize setting name.
Ensure that setting names are title case without leading or trailing whitespace. For example from::

    *** Settings ***
    library    library.py
    test template    Template
    FORCE taGS    tag1

    *** Keywords ***
    Keyword
        [arguments]    ${arg}
        [ SETUP]   Setup Keyword

To::

    *** Settings ***
    Library    library.py
    Test Template    Template
    Force Tags    tag1

    *** Keywords ***
    Keyword
        [Arguments]    ${arg}
        [Setup]   Setup Keyword

Supports global formatting params: ``--startline`` and ``--endline``.