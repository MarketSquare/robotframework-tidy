.. _OrderSettings:

OrderSettings
================================

Order settings like ``[Arguments]``, ``[Setup]``, ``[Tags]`` inside Keywords and Test Cases.

.. |TRANSFORMERNAME| replace:: OrderSettings
.. include:: enabled_hint.txt

Test case settings ``[Documentation]``, ``[Tags]``, ``[Template]``, ``[Timeout]``, ``[Setup]`` are put before test case
body and ``[Teardown]`` is moved to the end of test case.

Keyword settings ``[Documentation]``, ``[Tags]``, ``[Timeout]``, ``[Arguments]``, ``[Setup]`` are put before keyword
body and settings like ``[Teardown]``, ``[Return]`` are moved to the end of keyword.

.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

            *** Test Cases ***
            Test
                [Setup]    Setup
                [Teardown]    Teardown
                [Documentation]    Test documentation.
                [Tags]    tags
                [Template]    Template
                [Timeout]    60 min
                Test Step


            *** Keywords ***
            Keyword
                [Teardown]    Keyword
                [Return]    ${value}
                [Arguments]    ${arg}
                [Documentation]    this is
                ...    doc
                [Setup]    Setup
                [Tags]    sanity
                Pass

    .. tab-item:: After

        .. code:: robotframework

            *** Test Cases ***
            Test
                [Documentation]    Test documentation.
                [Tags]    tags
                [Template]    Template
                [Timeout]    60 min
                [Setup]    Setup
                Test Step
                [Teardown]    Teardown


            *** Keywords ***
            Keyword
                [Documentation]    this is
                ...    doc
                [Tags]    sanity
                [Arguments]    ${arg}
                [Setup]    Setup
                Pass
                [Teardown]    Keyword
                [Return]    ${value}


Configure order of the settings
----------------------------------

Default order can be changed using following parameters:

- ``keyword_before = documentation,tags,arguments,timeout,setup``
- ``keyword_after = teardown,return``
- ``test_before = documentation,tags,template,timeout,setup``
- ``test_after = teardown``

For example::

    robotidy --configure OrderSettings:test_before=setup,teardown:test_after=documentation,tags

It is not required to overwrite all orders - for example configuring only ``test_before`` and ``test_after`` keeps
keyword order as default.

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


            *** Keywords ***
            Keyword
                [Documentation]    this is
                ...    doc
                [Tags]    sanity
                [Arguments]    ${arg}
                [Setup]    Setup
                Pass
                [Teardown]    Keyword
                [Return]    ${value}

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


            *** Keywords ***
            Keyword
                [Documentation]    this is
                ...    doc
                [Tags]    sanity
                [Arguments]    ${arg}
                [Setup]    Setup
                Pass
                [Teardown]    Keyword
                [Return]    ${value}

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

Splitting configuration
-----------------------

Robotidy combines split configuration. It is possible to configure the same transformer in multiple CLI commands or
configuration entries::

    robotidy --configure OrderSettings:keyword_before=documentation,tags,timeout,arguments,setup --configure OrderSettings:keyword_after=teardown,return

Configuration files can also contain spaces for better readability.

  .. code-block:: toml

    [tool.robotidy]
    configure = [
        "OrderSettings: keyword_before = documentation, tags, timeout, arguments, setup",
        "OrderSettings: keyword_after = teardown, return",
    ]

Settings comments
---------------------

Comments next to settings will be moved together.

.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

            *** Keywords ***
            Keyword
                # comment about step
                Step
                # comment about arguments
                [Arguments]    ${arg}

    .. tab-item:: After

        .. code:: robotframework

            *** Keywords ***
            Keyword
                # comment about arguments
                [Arguments]    ${arg}
                # comment about step
                Step
