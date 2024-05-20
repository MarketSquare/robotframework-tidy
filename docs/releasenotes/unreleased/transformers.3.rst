Align settings separately in AlignKeywordsSection and AlignTestCasesSection (#657)
----------------------------------------------------------------------------------

It is now possible to align settings separately from rest of the code in keyword / test case. Configure it
using ``align_settings_separately`` parameter::

    robotidy -c AlignKeywordsSection:align_settings_separately=True src
    robotidy -c AlignTestCasesSection:align_settings_separately=True src

Since this type of alignment depends on the width of the column it only works together with ``auto`` alignment type.

For example following code::

    *** Test Cases ***
    Test Password Policy Minimum Length Input Errors
        [Timeout]   10 min
        [Tags]    tag    tag
        Log    ${argument_name}
        Perform Action And Wait For Result    ${argument_name}

It is by default (with ``alignment_type=auto`` and ``align_settings_separately=False``) formatted to::

    *** Test Cases ***
    Test Password Policy Minimum Length Input Errors
        [Timeout]       10 min
        [Tags]          tag                 tag
        Log             ${argument_name}
        Perform Action And Wait For Result          ${argument_name}

With ``alignment_type=auto`` and ``align_settings_separately=True`` it is formatted to::

    *** Test Cases ***
    Test Password Policy Minimum Length Input Errors
        [Timeout]       10 min
        [Tags]          tag         tag
        Log     ${argument_name}
        Perform Action And Wait     ${argument_name}
