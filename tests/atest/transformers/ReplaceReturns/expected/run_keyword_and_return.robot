*** Test Cases ***
For and Ifs
    FOR    ${var}  IN  1  2
        IF    $var == 2
            RETURN    Keyword   ${arg}
        END
    END

*** Keywords ***
Testing
    RETURN    Keyword   ${arg}
    ...  ${arg2}
