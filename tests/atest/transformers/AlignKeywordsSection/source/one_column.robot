*** Keywords ***
Keyword
    Single column
      One column
    No args
    Args
    ...
    ...    In Last

For loop
    FOR    ${var}    IN RANGE    10
      Single column
       No args
    END

Misaligned
    Keyword
...    misaligned

Misaligned with empty
    Keyword
...    misaligned

...   arg
