*** Keywords ***
First
    ${var}    Set Variable    1
    FOR    ${variable}  IN  1  2
        IF    ${var}==2
            RETURN  Keyword 2    ${var}
        END
        Log    ${variable}
    END

With IF
    ${var}    Set Variable    1
    IF    ${var}>0
        IF    $var
            RETURN    Some Keyword    ${var}
              ...  1
        END
    END
