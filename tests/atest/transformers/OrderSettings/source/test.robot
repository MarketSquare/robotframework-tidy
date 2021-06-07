*** Test Cases ***
Test case 1
    [Documentation]  this is
    ...    doc
    [Teardown]  Teardown
    Keyword
    [Tags]
    ...  tag
    [Setup]  Setup  # comment
    Keyword

Test case 2
    [Template]  Template
    Keyword
    [Timeout]  timeout
    [Timeout]  timeout2  # this is error because it is duplicate

*** Keywords ***
Keyword
    [Teardown]  Keyword
    [Return]  ${value}
    [Arguments]  ${arg}
    [Documentation]  this is
    ...    doc
    [Tags]  sanity
    Keyword
    No Operation
    IF  ${condition}
        Log  ${stuff}
    END
    FOR  ${var}  IN  1  2
        Log  ${var}
    END
    Pass

Another Keyword ${var}
    No Operation
    [Timeout]
