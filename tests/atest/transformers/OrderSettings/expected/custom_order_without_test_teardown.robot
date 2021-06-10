*** Test Cases ***
Test case 1
    [Documentation]  this is
    ...    doc
    [Tags]
    ...  tag
    [Setup]  Setup  # comment
    [Teardown]  Teardown
    Keyword
    Keyword

Test case 2
    [Template]  Template
    [Timeout]  timeout
    Keyword
    [Timeout]  timeout2  # this is error because it is duplicate

Test case with comment at the end
    [Teardown]  Keyword
    #  comment

# comment

Test case 3
    Golden Keyword

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

Keyword With Comment
    Keyword
    [Return]  ${value}
    # I am comment

Keyword With Empty Line And Comment
    Keyword
    [Return]  ${value}

# I am comment in new line

Another Keyword
    No Operation
    # innocent comment

Comment Before setting
    Keyword
    # I want to be here
    [Return]    ${value}

Return first and comment last
    Keyword
    [Return]  stuff
    # I want to be here

# what will happend with me?
