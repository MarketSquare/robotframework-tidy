.. _RemoveEmptySettings:

RemoveEmptySettings
================================

Remove empty settings.

You can configure which settings are affected by parameter ``work_mode``. Possible values:
    - overwrite_ok (default): does not remove settings that are overwriting suite settings (Test Setup,
      Test Teardown, Test Template, Test Timeout or Default Tags)
    - always : works on every settings

Empty settings that are overwriting suite settings will be converted to be more explicit::

    No timeout
    [Documentation]    Empty timeout means no timeout even when Test Timeout has been used.
    [Timeout]

To::

    No timeout
    [Documentation]    Disabling timeout with NONE works too and is more explicit.
    [Timeout]    NONE

You can disable that behavior by changing ``more_explicit`` parameter value to ``False``.

Supports global formatting params: ``--startline`` and ``--endline``.