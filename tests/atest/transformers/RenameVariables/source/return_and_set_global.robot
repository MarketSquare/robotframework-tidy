*** Keywords ***
[Return]
    ${local}    Set Variable    value
    [Return]    ${local}    ${global}

RETURN
    ${local}    Set Variable    value
    RETURN    ${local}    ${global}
