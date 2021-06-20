.. _OrderSettings:

OrderSettings
================================

Order settings like ``[Arguments]``, ``[Setup]``, ``[Return]`` inside Keywords and Test Cases.

OrderSettings is included in default transformers but it can be also
run separately with::

    robotidy --transform OrderSettings src

Keyword settings ``[Documentation]``, ``[Tags]``, ``[Timeout]``, ``[Arguments]`` are put before keyword body and
settings like ``[Teardown]``, ``[Return]`` are moved to the end of keyword.

.. tabs::

    .. code-tab:: robotframework Before

        *** Keywords ***
        Keyword
            [Teardown]    Keyword
            [Return]    ${value}
            [Arguments]    ${arg}
            [Documentation]    this is
            ...    doc
            [Tags]    sanity
            Pass

    .. code-tab:: robotframework After

       *** Keywords ***
        Keyword
            [Documentation]    this is
            ...    doc
            [Tags]    sanity
            [Arguments]    ${arg}
            Pass
            [Teardown]    Keyword
            [Return]    ${value}

Test case settings ``[Documentation]``, ``[Tags]``, ``[Template]``, ``[Timeout]``, ``[Setup]`` are put before test case body and
[Teardown] is moved to the end of test case.

Default order can be changed using following parameters:
  - ``keyword_before = documentation,tags,timeout,arguments``
  - ``keyword_after = teardown,return``
  - ``test_before = documentation,tags,template,timeout,setup``
  - ``test_after = teardown``

For example::

    robotidy --configure OrderSettings:test_before=setup,teardown:test_after=documentation,tags

.. tabs::

    .. code-tab:: robotframework Before

        *** Test Cases ***
        Test case 1
            [Documentation]    this is
            ...      doc
            [Teardown]    Teardown
            Keyword1
            [Tags]
            ...    tag
            [Setup]    Setup  # comment
            Keyword2

    .. code-tab:: robotframework After

        *** Test Cases ***
        Test case 1
            [Setup]    Setup  # comment
            [Teardown]    Teardown
            Keyword1
            Keyword2
            [Documentation]    this is
            ...    doc
            [Tags]
            ...    tag

Not all settings names need to be passed to given parameter. Missing setting names are not ordered. Example::

    robotidy --configure OrderSettings:keyword_before=:keyword_after=

It will order only test cases because all setting names for keywords are missing.

Supports global formatting params: ``--startline`` and ``--endline``.