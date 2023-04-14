*** Settings ***
Force Tags    value    value
...    value    value


*** Variables ***
@{LIST}    1
...  2
...  3   4    5

*** Keywords ***
Keyword
    [Arguments]    ${argument1}
    ...    ${argument2}    ${argument3}
    Keyword Call    1    2
    ...    1
    ...    2    3
    FOR    ${var}    IN    1    2
    ...    1    2
        Keyword Call    1    2
        ...    1  # comment
        ...    2    3
    END
