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

*** Keywords ***
# robotidy: off
Keyword
    [Arguments]    ${arg}
    # robotidy: on
    Step
    # robotidy: off
    Step  1
    ...  2

Keyword 2
    No Operation

# robotidy: on

Keyword 3
    [Tags]    tag
    ...   tag2    # robotidy: off
    WHILE    $condition
        FOR    ${var}   IN  1  2
            IF    $var
                Step
                # robotidy: off
                Step 2
                # robotidy: on
                IF    $var
                    ${return}    Step 3    a    b
                END
            ELSE IF
                TRY
                    Step
                EXCEPT
                    Step
                    # robotidy: off
                    Step 2
                ELSE
                    Step
                FINALLY
                    Step
                END
            END
        END

    FOR    ${var}    IN    a  b  # robotidy: off
        Keyword    ${var}
    END
