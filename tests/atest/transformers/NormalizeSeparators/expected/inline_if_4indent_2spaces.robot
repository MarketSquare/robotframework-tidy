*** Test Cases ***
Simple IF
    IF  $condition1  Keyword  argument
    IF  $condition1  RETURN

Nested IF
    FOR  ${var}  IN RANGE  10
        IF  $condition1  Keyword  argument  # comment
    END
