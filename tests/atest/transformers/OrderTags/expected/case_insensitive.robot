*** Settings ***
Documentation       OrderTags acceptance tests

*** Test Cases ***
No tags
    No Operation

Tags Upper Lower
    [Tags]    aa    Ab    ba    Bb    Ca    Cb
    My Keyword

One Tag
    [Tags]    one_tag
    One Tag Keyword

*** Keywords ***
My Keyword
    [Tags]    aa    Ab    ba    Bb    Ca    Cb
    No Operation

One Tag Keyword
    [Tags]    one_tag
    No Operation