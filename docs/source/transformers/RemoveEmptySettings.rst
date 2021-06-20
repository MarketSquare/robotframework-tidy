.. _RemoveEmptySettings:

RemoveEmptySettings
================================

Remove empty settings.

RemoveEmptySettings is included in default transformers but it can be also
run separately with::

    robotidy --transform RemoveEmptySettings src

.. tabs::

    .. code-tab:: robotframework Before

        *** Settings ***
        Documentation
        Suite Setup
        Metadata
        Metadata    doc=1
        Test Setup
        Test Teardown    Teardown Keyword
        Test Template
        Test Timeout
        Force Tags
        Default Tags
        Library
        Resource
        Variables

        *** Test Cases ***
        Test
            [Setup]
            [Template]    #  comment    and    comment
            [Tags]    tag
            Keyword

    .. code-tab:: robotframework After

        *** Settings ***
        Metadata    doc=1
        Test Teardown    Teardown Keyword

        *** Test Cases ***
        Test
            [Tags]    tag
            Keyword

You can configure which settings are affected by parameter ``work_mode``. Possible values:
- overwrite_ok (default): does not remove settings that are overwriting suite settings (Test Setup,
Test Teardown, Test Template, Test Timeout or Default Tags)
- always : works on every settings

Empty settings that are overwriting suite settings will be converted to be more explicit (given that there is
related suite settings present). You can disable that behavior by changing ``more_explicit``
parameter value to ``False``::

    robotidy --configure RemoveEmptySettings:more_explicit=False src

.. tabs::

    .. code-tab:: robotframework Before

        *** Settings ***
        Test Timeout  1min
        Force Tags

        *** Test Case ***
        Test
            [Documentation]    Empty timeout means no timeout even when Test Timeout has been used.
            [Timeout]
            No timeout

    .. code-tab:: robotframework After (default)

        *** Settings ***
        Test Timeout  1min

        *** Test Case ***
        Test
            [Documentation]    Empty timeout means no timeout even when Test Timeout has been used.
            [Timeout]    NONE
            No timeout

    .. code-tab:: robotframework After ``more_explicit`` = False

        *** Settings ***
        Test Timeout  1min

        *** Test Case ***
        Test
            [Documentation]    Empty timeout means no timeout even when Test Timeout has been used.
            [Timeout]
            No timeout

If you want to remove all empty settings even if they are overwriting suite settings (like in above example) then
set ``work_mode`` to ``always``::

    robotidy --configure RemoveEmptySettings:work_mode=always src

.. tabs::

    .. code-tab:: robotframework Before

        *** Settings ***
        Test Timeout  1min
        Force Tags

        *** Test Case ***
        Test
            [Documentation]    Empty timeout means no timeout even when Test Timeout has been used.
            [Timeout]
            No timeout

    .. code-tab:: robotframework After

        *** Settings ***
        Test Timeout  1min

        *** Test Case ***
        Test
            [Documentation]    Empty timeout means no timeout even when Test Timeout has been used.
            No timeout

Supports global formatting params: ``--startline`` and ``--endline``.