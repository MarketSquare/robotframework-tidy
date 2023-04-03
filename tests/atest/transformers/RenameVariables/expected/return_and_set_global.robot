*** Keywords ***
[Return]
    ${local}    Set Variable    value
    [Return]    ${local}    ${GLOBAL}

RETURN
    ${local}    Set Variable    value
    RETURN    ${local}    ${GLOBAL}
