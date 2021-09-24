*** Settings ***
Documentation       OrderTags acceptance tests

*** Test Cases ***
No tags
    No Operation

Tags Upper Lower
    [Tags]    ba    aa    Cb    Ca    Bb    Ab
    My Keyword

One Tag
    [Tags]    one_tag
    One Tag Keyword

*** Keywords ***
My Keyword
    [Tags]    ba    aa    Cb    Ca    Bb    Ab
    No Operation

One Tag Keyword
    [Tags]    one_tag
    No Operation