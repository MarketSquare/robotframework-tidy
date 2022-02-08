*** Test Cases ***
Inline IF
    IF    $condition1    Keyword    argument
    IF    $condition1    Keyword    ELSE IF    $condition2    Keyword2    ELSE    Keyword3
    ${var}    IF    $condition1    Keyword    argument

Simple IF
    IF    $condition1    Keyword    argument
    IF    $condition2    RETURN

Branched IF
    IF    $condition1
        Keyword    1
    ELSE
        Keyword    2
    END

Multi statements IF
    IF    $condition1
        Keyword
        Keyword 2
    END

    IF    $condition1
        Keyword
    ELSE IF  $condition2
        Keyword
        Keyword 2
    END

Nested IF
    IF    $condition1
        IF    $condition2    RETURN
        Keyword
    END

    IF  $condition1
        Keyword
    ELSE
        IF    $condition2    RETURN
    END

Assign vars IF
   IF    $condition1
       ${var}    Keyword
   END

   IF  $condition1
       ${var}    ${var2}    Keyword
   ELSE
       ${var}    ${var2}    Keyword2
   END

   IF  $condition1
       ${var}    Keyword
   ELSE IF  $condition2
       ${var}    Keyword2
   END

   IF  $condition1
       ${var}    Keyword
   ELSE
       ${var2}    Keyword2
   END

   IF  $condition1
       ${var}    Keyword
   ELSE
       Keyword2
   END

Long line IF
    IF    ($condition1 and $condition2) or ($condition3)
        This Keyword Does Some Thing And Have Quite Long Name For Some Reason    ${argument}
    END

For Loop IF
    IF    $condition1
        FOR    ${var}    IN RANGE  10
            Keyword
        END
    END

With Comments IF
    IF    $condition1
        Keyword
    ELSE
        # not sure if it's valid though
    END

Break Continue IF
    WHILE    $condition
        IF    $condition2    CONTINUE
        Keyword
        IF    $condition3    BREAK
    END

Multiline IF
    IF    $condition    Keyword    1    2    3

Return With Value IF
    IF    $condition    RETURN    ${a}    ${b}

Mixed Type Return IF
    IF    $condition
        ${var}    Keyword
    ELSE
        RETURN
    END

Invalid IF
    IF    $condition
    END

    IF    $cond    Keyword
        Keyword
    END
