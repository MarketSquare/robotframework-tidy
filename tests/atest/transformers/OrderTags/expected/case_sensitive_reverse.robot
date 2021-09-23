*** Settings ***
Documentation       OrderTags acceptance tests

*** Test Cases ***
No tags
    No Operation

Tags Upper Lower
    [Tags]    ba    aa    Cb    Ca    Bb    Ab
    My Keyword

*** Keywords ***
My Keyword
    [Tags]    ba    aa    Cb    Ca    Bb    Ab
    No Operation