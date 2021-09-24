*** Settings ***
Documentation       OrderTags acceptance tests
Force Tags              ONE_TAG_VARIOUS CASES
Default Tags            ONE_TAG_VARIOUS CASES

*** Test Cases ***
No tags
    Keyword no tags

Normalize case
    [Tags]    FOO_BAR_BAZ_A    FOO_BAR_BAZ_B    FOO_BAR_BAZ_C    FOOBARBAZD    FOOBARBAZE    FOOBARBAZF    FOO BAR BAZ G    FOO BAR BAZ H    FOO BAR BAZ I
    Keyword normalize case

Deduplicate
    [Tags]    TAG_A    TAG_B    TAG_C
    Keyword deduplicate

Deduplicate and normalize case
    [Tags]    FOO_BAR_BAZ_A    FOO_BAR_BAZ_B    FOO_BAR_BAZ_C    FOOBARBAZD    FOOBARBAZE    FOOBARBAZF    FOO BAR BAZ G    FOO BAR BAZ H    FOO BAR BAZ I
    Keyword deduplicate and normalize case

One Tag
    [Tags]    ONE_TAG_VARIOUS CASES
    One Tag Keyword

*** Keywords ***
Keyword no tags
    No Operation

Keyword normalize case
    [Tags]    FOO_BAR_BAZ_A    FOO_BAR_BAZ_B    FOO_BAR_BAZ_C    FOOBARBAZD    FOOBARBAZE    FOOBARBAZF    FOO BAR BAZ G    FOO BAR BAZ H    FOO BAR BAZ I
    No Operation

Keyword deduplicate
    [Tags]    TAG_A    TAG_B    TAG_C
    No Operation

Keyword deduplicate and normalize case
    [Tags]    FOO_BAR_BAZ_A    FOO_BAR_BAZ_B    FOO_BAR_BAZ_C    FOOBARBAZD    FOOBARBAZE    FOOBARBAZF    FOO BAR BAZ G    FOO BAR BAZ H    FOO BAR BAZ I
    No Operation

One Tag Keyword
    [Tags]    ONE_TAG_VARIOUS CASES
    No Operation