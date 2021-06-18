.. _NormalizeSettingName:

NormalizeSettingName
================================

Normalize setting name.

NormalizeSettingName is included in default transformers but it can be also
run separately with::

    robotidy --transform NormalizeSettingName src

Ensure that setting names are title case without leading or trailing whitespace.

.. tabs::

    .. code-tab:: robotframework Before

        *** Settings ***
        library    library.py
        test template    Template
        FORCE taGS    tag1

        *** Keywords ***
        Keyword
            [arguments]    ${arg}
            [ SETUP]   Setup Keyword

    .. code-tab:: robotframework After

        *** Settings ***
        Library    library.py
        Test Template    Template
        Force Tags    tag1

        *** Keywords ***
        Keyword
            [Arguments]    ${arg}
            [Setup]   Setup Keyword

Supports global formatting params: ``--startline`` and ``--endline``.