*** Test Cases ***
Test
    Click With Options    elem    button=right

Test in loop
    WHILE    ${var}
        Browser.Click With Options    elem    CONTROL    SHIFT
    END

Already replaced
    Click With Options    elem    button=right   clickCount=1

Different keyword
    Some Custom Keyword    elem

*** Keywords ***
Keyword
    Click With Options    elem    SHIFT    clickCount=2    delay=200ms
