.. _OrderSettings:

OrderSettings
================================

Order settings like ``[Arguments]``, ``[Setup]``, ``[Return]`` inside Keywords and Test Cases.

.. |TRANSFORMERNAME| replace:: OrderSettings
.. include:: enabled_hint.txt

Keyword settings ``[Documentation]``, ``[Tags]``, ``[Timeout]``, ``[Arguments]`` are put before keyword body and
settings like ``[Teardown]``, ``[Return]`` are moved to the end of keyword.

.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

            *** Keywords ***
            Keyword
                [Teardown]    Keyword
                [Return]    ${value}
                [Arguments]    ${arg}
                [Documentation]    this is
                ...    doc
                [Tags]    sanity
                Pass

    .. tab-item:: After

        .. code:: robotframework

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
``[Teardown]`` is moved to the end of test case.

Default order can be changed using following parameters:

- ``keyword_before = documentation,tags,timeout,arguments``
- ``keyword_after = teardown,return``
- ``test_before = documentation,tags,template,timeout,setup``
- ``test_after = teardown``

For example::

    robotidy --configure OrderSettings:test_before=setup,teardown:test_after=documentation,tags

.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

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

    .. tab-item:: After

        .. code:: robotframework

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

Setting name cannot be present in both before/after parts. For example ``keyword_before=tags:keyword_after=tags``
configuration is invalid because ``tags`` cannot be ordered both before and after. It is important if you are
overwriting default order - in most cases you need to overwrite both before/after parts.
This configuration is invalid because teardown is by default part of the ``test_after``::

    robotidy --configure OrderSettings:test_before=teardown

We need to overwrite both orders::

    robotidy --configure OrderSettings:test_before=teardown:test_after=
