*** Settings ***
Documentation       OrderTags acceptance tests

*** Test Cases ***
No tags
    No Operation

Tags Upper Lower
    [Tags]    Ab    Bb    Ca    Cb    aa    ba
    My Keyword

*** Keywords ***
My Keyword
    [Tags]    Ab    Bb    Ca    Cb    aa    ba
    No Operation