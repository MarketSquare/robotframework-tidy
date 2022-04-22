*** Settings ***
Test Template    Template
Tags    tag
...   tag2
# robotidy: off
Suite Setup Keyword
Documentation    Suite documentation

*** Test Cases ***
Test
    No Operation

# robotidy: off


*** Keywords ***
Keyword
    Other Keyword

# robotidy: off

Other Keyword ${embed}
    RETURN    ${embed}
