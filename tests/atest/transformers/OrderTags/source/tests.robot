*** Settings ***
Documentation       OrderTags acceptance tests

*** Test Cases ***
No tags
    No Operation

Tags Upper Lower
    [Tags]    ba    Ab    Bb    Ca    Cb    aa
    My Keyword

One Tag
    [Tags]    one_tag
    One Tag Keyword

*** Keywords ***
My Keyword
    [Tags]    ba    Ab    Bb    Ca    Cb    aa
    No Operation

One Tag Keyword
    [Tags]    one_tag
    No Operation