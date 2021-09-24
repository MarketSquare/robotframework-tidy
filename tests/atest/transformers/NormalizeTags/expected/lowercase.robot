*** Settings ***
Documentation       OrderTags acceptance tests
Force Tags              one_tag_various cases
Default Tags            one_tag_various cases

*** Test Cases ***
No tags
    Keyword no tags

Normalize case
    [Tags]    foo_bar_baz_a    foo_bar_baz_b    foo_bar_baz_c    foobarbazd    foobarbaze    foobarbazf    foo bar baz g    foo bar baz h    foo bar baz i
    Keyword normalize case

Deduplicate
    [Tags]    tag_a    tag_b    tag_c
    Keyword deduplicate

Deduplicate and normalize case
    [Tags]    foo_bar_baz_a    foo_bar_baz_b    foo_bar_baz_c    foobarbazd    foobarbaze    foobarbazf    foo bar baz g    foo bar baz h    foo bar baz i
    Keyword deduplicate and normalize case

One Tag
    [Tags]    one_tag_various cases
    One Tag Keyword

*** Keywords ***
Keyword no tags
    No Operation

Keyword normalize case
    [Tags]    foo_bar_baz_a    foo_bar_baz_b    foo_bar_baz_c    foobarbazd    foobarbaze    foobarbazf    foo bar baz g    foo bar baz h    foo bar baz i
    No Operation

Keyword deduplicate
    [Tags]    tag_a    tag_b    tag_c
    No Operation

Keyword deduplicate and normalize case
    [Tags]    foo_bar_baz_a    foo_bar_baz_b    foo_bar_baz_c    foobarbazd    foobarbaze    foobarbazf    foo bar baz g    foo bar baz h    foo bar baz i
    No Operation

One Tag Keyword
    [Tags]    one_tag_various cases
    No Operation