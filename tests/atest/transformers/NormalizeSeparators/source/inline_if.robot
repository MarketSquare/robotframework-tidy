*** Test Cases ***
Simple IF
    IF    $condition1    Keyword    argument

Nested IF
    FOR    ${var}    IN RANGE    10
        IF    $condition1    Keyword    argument    # comment
    END
