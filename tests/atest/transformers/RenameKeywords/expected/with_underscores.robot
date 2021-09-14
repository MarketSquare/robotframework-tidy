*** Test Cases ***
test
    Keyword

Rename Me
    No Operation

*** Keywords ***
Rename Me
   Also Rename This

Rename Me 2
    No Operation

I Am Fine
    But I Am Not

Underscores_are_bad
    Looks_like_python

Keyword With Unicode And Non Latin
    Eäi Saa Peittää
    日本語
    _

Ignore ${var} Embedded
    Also Ignore ${variable}['key'] Syntax

Structures
    FOR  ${var}  IN  1  2  3
        IF  condition
            Keyword
        ELSE IF
            Keyword
        ELSE
            Keyword
        END
            Keyword
    END

Double__underscores
    No Operation
