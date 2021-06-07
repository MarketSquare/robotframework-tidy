*** Test Cases ***
Test case 1
    Keyword
    Keyword
    [Documentation]  this is
    ...    doc
    [Tags]
    ...  tag
    [Setup]  Setup  # comment
    [Teardown]  Teardown

Test case 2
    Keyword
    [Timeout]  timeout2  # this is error because it is duplicate
    [Template]  Template
    [Timeout]  timeout

*** Keywords ***
Keyword
    Keyword
    No Operation
    IF  ${condition}
        Log  ${stuff}
    END
    FOR  ${var}  IN  1  2
        Log  ${var}
    END
    Pass
    [Documentation]  this is
    ...    doc
    [Tags]  sanity
    [Arguments]  ${arg}
    [Teardown]  Keyword
    [Return]  ${value}

Another Keyword ${var}
    No Operation
    [Timeout]
