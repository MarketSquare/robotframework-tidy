*** Keywords ***
Single Argument
    [Documentation]
    ...
    ...    Arguments:
    ...        ${var}: 
    [Arguments]    ${var}

Two Arguments
    [Documentation]
    ...
    ...    Arguments:
    ...        ${var}: 
    ...        ${var2}: 
    [Arguments]    ${var}    ${var2}

No Arguments
    [Documentation]
    Log    ${EMPTY}

Empty Arguments
    [Documentation]
    [Arguments]

Return
    [Documentation]
    RETURN    ${var}

Return in block
    [Documentation]
    IF    $condition
        FOR    ${var}    IN RANGE    10
            IF    $var    RETURN    ${other_value}    ${multiple}
        END
    END

[Return]
    [Documentation]
    ...
    ...    Returns:
    ...        ${var}: 
     Step
     [Return]    ${var}

Double [Return]
    [Documentation]
    ...
    ...    Returns:
    ...        ${var}: 
     Step
     [Return]    ${var}
     [Return]    ${var}
     ...    $[var2}

Arguments And Return
    [Documentation]
    ...
    ...    Arguments:
    ...        ${var}: 
    ...        ${var2}: 
    [Arguments]    ${var}
    ...    ${var2}
    RETURN    ${var}

One Required And One With Default
    [Documentation]
    ...
    ...    Arguments:
    ...        ${required}: 
    ...        ${optional}: 
    [Arguments]    ${required}    ${optional}=default
    Log    Required: ${required}
    Log    Optional: ${optional}

Default Based On Earlier Argument
    [Documentation]
    ...
    ...    Arguments:
    ...        ${a}: 
    ...        ${b}: 
    ...        ${c}: 
    [Arguments]    ${a}    ${b}=${a}    ${c}=${a} and ${b}
    Should Be Equal    ${a}    ${b}
    Should Be Equal    ${c}    ${a} and ${b}

Existing documentation
    [Documentation]    Overwrite if needed.
    Step

Embedded ${var} variable
    [Documentation]
    ...
    ...    Arguments:
    ...        ${var}: 
    Step

Two ${embedded:pattern} variables ${embedded2}
    [Documentation]
    ...
    ...    Arguments:
    ...        ${embedded:pattern}: 
    ...        ${embedded2}: 
    Step
