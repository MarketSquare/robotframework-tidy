*** Settings ***
Documentation  doc
Suite Setup    Keyword
Suite Teardown    Keyword
Metadata    doc=1
Test Setup    Keyword
Test Teardown    Keyword
Test Template    Keyword
Force Tags    tag
Default Tags    tag
Library    stuff.py
Resource    resource.robot
Variables    vars.py


*** Test Cases ***
Test
    [Tags]    tag
    Keyword

Test 2
    [Setup]    Keyword
    [Template]    Keyword
    [Timeout]    1min
    Keyword

Test 3
    Keyword



*** Keywords ***
Keyword
    [Arguments]    ${arg}
    Keyword

Keyword 2
    Keyword
    [Return]    stuff
