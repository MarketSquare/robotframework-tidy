*** Settings ***
Documentation       OrderTags acceptance tests

*** Test Cases ***
No tags
    No Operation

Tags Upper Lower
    [Tags]    ba    Ab    Bb    Ca    Cb    aa
    My Keyword

*** Keywords ***
My Keyword
    [Tags]    ba    Ab    Bb    Ca    Cb    aa
    No Operation