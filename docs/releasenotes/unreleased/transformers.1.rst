Aligning test cases with [Template] (#657)
------------------------------------------

Robotidy now aligns test cases with ``[Template]``. It is done by ``AlignTestCasesSection``.

Note that there is also ``AlignTemplatedTestCases`` which uses completely different approach for aligning test cases
and only supports suites with ``Test Template`` setting.

Previously, following code::

    *** Test Cases ***
    Testing Random List
        [Template]    Validate Random List Selection
        ${SIMPLE LIST}    2
        ${MIXED LIST}         3
        ${NESTED LIST}    4

would not be aligned and would be formatted to::

    *** Test Cases ***
    Testing Random List
        [Template]    Validate Random List Selection
        ${SIMPLE LIST}    2
        ${MIXED LIST}    3
        ${NESTED LIST}    4

Now test cases with ``[Template]`` are formatted properly::

    *** Test Cases ***
    Testing Random List
        [Template]    Validate Random List Selection
        ${SIMPLE LIST}      2
        ${MIXED LIST}       3
        ${NESTED LIST}      4
