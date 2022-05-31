*** Test Cases ***
Multiple cases
    Run Keyword And Continue On Failure
    ...    Run Keyword If    ${True}
    ...      Run keywords
    ...        log    foo    AND
    ...        Log    bar
    ...    ELSE
    ...      log    baz

ELSE markers
    Run Keyword And Continue On Failure
    ...    Run Keyword If    ${True}
    ...      Run Keyword If    ${False}
    ...        Log    bar
    ...      ELSE IF  ${True}
    ...        Log  Else If
    ...    ELSE
    ...      log    Else

Nested
    Run Keyword And Continue On Failure    Run Keyword And Continue On Failure   Run Keyword And Continue On Failure    Log  Buh

Normal
    Run Keyword And Continue On Failure    Keyword    arg

WUKS
    Wait Until Keyword Succeeds    2 min	5 sec	Keyword  argument

Repeat
    Repeat Keyword  2 minutes  Keyword    arg

Run Keyword If
    Run Keyword If    ${condition}
    ...        Keyword    2
    ...    ELSE IF   ${other_condition}
    ...        No Operation
    ...    ELSE IF   ${condition}
    ...        Keyword    1   2
    ...    ELSE
    ...        No Operation

    # no branches
    Run Keyword If    ${condition}    Keyword    ${argument}    ${another_argument}

    # with run keywords
    Run Keyword If    ${condition}    Run Keywords    Keyword    Keyword

    # invalid - no condition
    Run Keyword If    ${condition}    Keyword    2    ELSE IF

    # invalid - empty
    Run Keyword If

Assign
    ${var}    Run Keyword If    ${True}    Keyword    Keyword
    ${var}    ${var}    Run Keyword If    ${True}    Keyword    ELSE IF    ${False}    Keyword2
    @{var}    Run Keyword If    ${True}    Run Keywords    Keyword    Keyword

Run Keywords
    Run Keywords
    ...    No Operation
    ...    No Operation

    Run Keywords
    ...    Log  1    AND
    ...    Log  2    AND    Log    3

    Run Keywords    No Operation    AND    No Operation

     Run Keywords
     ...    Log  1    \AND
     ...    Log  2

    Run Keywords
    ...    Run Keyword If  ${True}    Log  1  AND
    ...    Run Keyword If  ${True}    Log  2

    # invalid
    Run Keywords

    Run Keywords    AND

*** Keywords ***
Keyword
    [Arguments]    ${arg}
    No Operation

Run Keywords
    Run Keywords    No Operation    No Operation
