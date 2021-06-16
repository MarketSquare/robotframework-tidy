.. _OrderSettings:

OrderSettings
================================

Order settings like ``[Arguments]``, ``[Setup]``, ``[Return]`` inside Keywords and Test Cases.

Keyword settings ``[Documentation]``, ``[Tags]``, ``[Timeout]``, ``[Arguments]`` are put before keyword body and
settings like ``[Teardown]``, ``[Return]`` are moved to the end of keyword::

   *** Keywords ***
    Keyword
        [Teardown]  Keyword
        [Return]  ${value}
        [Arguments]  ${arg}
        [Documentation]  this is
        ...    doc
        [Tags]  sanity
        Pass

To::

   *** Keywords ***
    Keyword
        [Documentation]  this is
        ...    doc
        [Tags]  sanity
        [Arguments]  ${arg}
        Pass
        [Teardown]  Keyword
        [Return]  ${value}

Test case settings ``[Documentation]``, ``[Tags]``, ``[Template]``, ``[Timeout]``, ``[Setup]`` are put before test case body and
[Teardown] is moved to the end of test case.

Default order can be changed using following parameters:
  - ``keyword_before = documentation,tags,timeout,arguments``
  - ``keyword_after = teardown,return``
  - ``test_before = documentation,tags,template,timeout,setup``
  - ``test_after = teardown``

Not all settings names need to be passed to given parameter. Missing setting names are not ordered. Example::

    robotidy --configure OrderSettings:keyword_before=:keyword_after=

It will order only test cases because all setting names for keywords are missing.

Supports global formatting params: ``--startline`` and ``--endline``.