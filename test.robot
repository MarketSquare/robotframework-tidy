*** Keywords ***
Keyword
    ${returned_value_with_long_name_1}    ${returned_value_with_long_name_2}    ${returned_value_with_long_name_3}    ${returned_value_with_long_name_4}    ${returned_value_with_long_name_5}    ${returned_value_with_long_name_6}    Short
    ...    ${var}    ${var}
    ...    ${var}
    Keyword 2    ${arg}
    ...    ${arg2}

Keyword
    ${returned_value_with_long_name_1}
    ...    ${returned_value_with_long_name_2}
    ...    ${returned_value_with_long_name_3}
    ...    ${returned_value_with_long_name_4}
    ...    ${returned_value_with_long_name_5}
    ...    ${returned_value_with_long_name_6}
    ...    Short
    ...    ${var}    ${var}
    ...    ${var}    Keyword 2    ${arg}
    ...    ${arg2}

Keyword
    ${returned_value_with_long_name_1}    ${returned_value_with_long_name_2}    ${returned_value_with_long_name_3}
    ...    ${returned_value_with_long_name_4}    ${returned_value_with_long_name_5}
    ...    ${returned_value_with_long_name_6}
    ...    Short
