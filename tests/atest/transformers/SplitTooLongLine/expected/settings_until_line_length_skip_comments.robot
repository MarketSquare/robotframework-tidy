*** Settings ***
Force Tags    PS_CSMON_15838    PR_PPD    PR_B450    PR_B650    PR_B850    PR_CS1000    PR_CS1000L    PAR_ECG
...    PAR_IP_1    PAR_SPO2
Default Tags    PS_CSMON_15838    PR_PPD    PR_B450    PR_B650    PR_B850    PR_CS1000    PR_CS1000L    PAR_ECG
...    PAR_IP_1    PAR_SPO2
# comment


*** Test Cases ***
Test with lots of tags
    [Tags]    PS_CSMON_15838    PR_PPD    PR_B450    PR_B650    PR_B850    PR_CS1000    PR_CS1000L    PAR_ECG
    ...    PAR_IP_1    PAR_SPO2
    Prepare
    Run
    Assert

Test with comments in settings
    [Tags]    tag    tag    PS_CSMON_15838    PR_PPD    PR_B450    PR_B650    PR_B850    PR_CS1000    PR_CS1000L
    ...    PAR_ECG    PAR_IP_1    PAR_SPO2
    # comment1
    # comment2
    # comment3


*** Keywords ***
Arguments
    [Arguments]    ${short}    ${veryLongAndJavaLikeArgumentThatWillGoOverAllowedLength}
    ...    ${veryLongAndJavaLikeArgumentThatWillGoOverAllowedLength}
    Step

Arguments multiline
    [Arguments]    ${short}    ${veryLongAndJavaLikeArgumentThatWillGoOverAllowedLength}
    ...    ${veryLongAndJavaLikeArgumentThatWillGoOverAllowedLength}
    Step

Arguments single line over limit
    [Arguments]    ${short}
    ...    ${veryLongAndJavaLikeArgumentThatWillGoOverAllowedLengthveryLongAndJavaLikeArgumentThatWillGoOverAllowedLength}
    ...    ${veryLongAndJavaLikeArgumentThatWillGoOverAllowedLength}
    Step

Comment that goes over the allowed length
    [Arguments]    ${short}    ${veryLongAndJavaLikeArgumentThatWillGoOverAllowedLength}  # this is long comment and it should be ignored with --skip-comments
    Step
