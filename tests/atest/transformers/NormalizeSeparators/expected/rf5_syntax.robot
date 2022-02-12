*** Keywords ***
Inline IF
    IF    $cond    Keyword

    IF    $cond    Keyword    1    ELSE IF    Keyword2    ${arg}

    IF    ${variable} == 5
        IF    $cond    Keyword
    END

    ${var}    IF    $cond    Keyword
    ...    ${arg}

    FOR    ${var}    IN RANGE    10
        FOR    ${var2}    1    2
            IF    $cond    Keyword
        END
    END

WHILE
    WHILE    $cond
        Keyword With    ${arg}
        ...    ${arg2}
        IF    ${variable} == 5
            IF    $cond    Keyword
        END
    END

TRY EXCEPT
    TRY
        Some Keyword
    EXCEPT    Error message    # Try matching this first.
        Error Handler 1
    END

    TRY
        IF    $cond    Keyword
    EXCEPT    Error message    Another error    ${message}    # Match any of these.
        Error handler
    END
    Open Connection

    TRY
        Use Connection
    FINALLY
        Close Connection
    END
