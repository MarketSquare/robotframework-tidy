Disablers not working for last setting in the Settings section (#639)
---------------------------------------------------------------------

Robotidy disablers partly didn't work for the last setting in the ``*** Settings ***`` section. It was caused by
``OrderSettingsSection`` which modified every last setting resetting node position. Following code should now work
properly::

    *** Settings ***
    Test Tags   # robotidy: off
    ...    tag1
    ...    tag2
