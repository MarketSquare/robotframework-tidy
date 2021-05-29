*** Keywords ***
Multiple Assignments
    ${first_assignment}    ${second_assignment}    My Keyword
    ${first_assignment}    ${second_assignment}    Some Lengthy Keyword So That This Line Is To Long          ${arg1}      ${arg2}
    ${multiline_first}
    ...    ${multiline_second}=    Some Lengthy Keyword So That This Line Is To Long
