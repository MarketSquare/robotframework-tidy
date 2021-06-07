*** Test Cases ***
Test case 1
    [Documentation]  this is
    ...    doc
    [Tags]
    ...  tag
    [Setup]  Setup  # comment
    Keyword
    Keyword
    [Teardown]  Teardown

Test case 2
    [Template]  Template
    [Timeout]  timeout
    Keyword
    [Timeout]  timeout2  # this is error because it is duplicate

*** Keywords ***
Keyword
    [Documentation]  this is
    ...    doc
    [Tags]  sanity
    [Arguments]  ${arg}
    Keyword
    No Operation
    IF  ${condition}
        Log  ${stuff}
    END
    FOR  ${var}  IN  1  2
        Log  ${var}
    END
    Pass
    [Teardown]  Keyword
    [Return]  ${value}

Another Keyword ${var}
    [Timeout]
    No Operation
