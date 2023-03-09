*** Test Cases ***
Test
    Click    elem    right    1

Test in loop
    WHILE    ${var}
        Browser.click   elem   left   1   None   None   None   False   False    CONTROL   SHIFT
    END

Already replaced
    Click With Options    elem    button=right   clickCount=1

Different keyword
    Some Custom Keyword    elem

*** Keywords ***
Keyword
    Click   elem   left   2   200ms   None   None   False   False   SHIFT
