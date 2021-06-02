*** Settings ***
Documentation
Documentation  doc
Suite Setup
Suite Setup    Keyword
Suite Teardown    Keyword
Metadata
Metadata    doc=1
Test Setup
Test Setup    Keyword
Test Teardown
Test Teardown    Keyword
Test Template
Test Template    Keyword
Force Tags
Force Tags    tag
Default Tags
Default Tags    tag
Library
Library    stuff.py
Resource
Resource    resource.robot
Variables
Variables    vars.py


*** Test Cases ***
Test
    [Setup]
    [Template]
    [Tags]    tag
    Keyword

Test 2
    [Setup]    Keyword
    [Template]    Keyword
    [Timeout]    1min
    [Tags]
    Keyword
    [Teardown]

Test 3
    [Timeout]
    Keyword



*** Keywords ***
Keyword
    [Arguments]    ${arg}
    Keyword
    [Return]

Keyword 2
    [Arguments]
    Keyword
    [Return]    stuff
