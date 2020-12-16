*** Test Cases ***
Test
    ${var}  ${var}  Run Keyword If  ${condition}    Keyword
    ...  ELSE IF  ${other_condition}    Other Keyword  ${arg}
    ...  ELSE  Final Keyword

    IF    condition
        Keyword
    ELSE IF  condition2
        Keyword2
    ELSE
        Keyword
    END
    Run Keyword If  ${condition}    Keyword
    ...  ELSE IF  ${other_condition}    Other Keyword
    ...  ELSE  Final Keyword

    Run Keyword If  "${var}"=="a"    Run Keywords  First Keyword  AND  Second Keyword  1  2
    ...  ELSE IF  ${var}==1  Run Keywords  Single Keyword  ${argument}
    ...  ELSE  Normal Keyword  abc
