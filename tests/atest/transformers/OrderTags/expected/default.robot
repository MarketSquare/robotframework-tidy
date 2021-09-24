*** Settings ***
Documentation       OrderTags acceptance tests
Force Tags          forced_tag_1    forced_tag_2    forced_tag_aa    forced_tag_Ab    forced_tag_ba    forced_tag_Bb
Default Tags        default_tag_1    default_tag_2    default_tag_aa    default_tag_Ab    default_tag_ba    default_tag_Bb

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