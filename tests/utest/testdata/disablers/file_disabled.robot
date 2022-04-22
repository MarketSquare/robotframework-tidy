# robotidy: off
*** Settings ***
Library  SeleniumLibrary

Metadata    Key    Value

*** Test Cases ***
Test
    [Documentation]     This is doc
    Step
    FOR    ${var}    IN RANGE    10
        IF    $condition
            WHILE    ${arg}
                ${return}    Keyword    ${value}
                ...    ${other_value}    # robotidy: off
            END
        ELSE IF
            Step    ${arg}
            ...    value
            Step 2
            #  comment
        END
    END
