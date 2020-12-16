*** Test Cases ***
Test
    Keyword


*** Keywords ***
Keyword
    Log  ${stuff}
    IF  "${var}"=="onevalue" and ("${var2}"=="1" or "${var2}"=="2")
        Other Keyword
    END
    Run Keyword If    "${var}"=="onevalue" and ("${var2}"=="1" or "${var2}"=="2")
    ...               Dictionary Should Not Contain Key    ${dict}    first_condition
    Run Keyword If    "${var}"=="onevalue" and ("${var2}"=="1" or "${var2}"=="2")
    ...               Dictionary Should Not Contain Key    ${dict}    second_condition
    Run Keyword If    "${var}"=="onevalue" and ("${var2}"=="1" or "${var2}"=="2")
    ...               Dictionary Should Not Contain Key    ${dict}    third_condition
    Run Keyword If    "${var}"=="onevalue" and ("${var2}"=="3" or "${var2}"=="4")
    ...               Dictionary Should Not Contain Key    ${dict}    fourth_condition
    Run Keyword If    "${var}"=="onevalue" and ("${var2}"=="3" or "${var2}"=="4")
    ...               Dictionary Should Not Contain Key    ${dict}    fifth_condition
    Run Keyword If    "${var}"=="onevalue" and ("${var2}"=="3" or "${var2}"=="4")
    ...               Dictionary Should Not Contain Key    ${dict}    sixth_condition
    Run Keyword If    "${var}"=="twovalue"    Dictionary Should Contain Key  ${dict}    first_condition
    Run Keyword If    "${var}"=="twovalue"    Dictionary Should Contain Key  ${dict}    second_condition
    Run Keyword If    "${var}"=="twovalue"    Dictionary Should Contain Key  ${dict}    third_condition
    Run Keyword If    "${var}"=="twovalue"    Dictionary Should Contain Key  ${dict}    a
    Run Keyword If    "${var}"=="twovalue"    Dictionary Should Contain Key  ${dict}    b
    Another Keyword In The Middle Possibly Affecting Condition
    Run Keyword If    "${var}"=="twovalue"    Dictionary Should Contain Key  ${dict}    fourth_condition