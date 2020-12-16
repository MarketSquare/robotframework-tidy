*** Test Cases ***
Test
    IF    ${condition}
        ${var}    ${var}    Keyword
    ELSE IF    ${other_condition}
        ${var}    ${var}    Other Keyword    ${arg}
    ELSE
        ${var}    ${var}    Final Keyword
    END

    IF    condition
        Keyword
    ELSE IF  condition2
        Keyword2
    ELSE
        Keyword
    END
    IF    ${condition}
        Keyword
    ELSE IF    ${other_condition}
        Other Keyword
    ELSE
        Final Keyword
    END

    IF    "${var}"=="a"
        First Keyword
        Second Keyword    1    2
    ELSE IF    ${var}==1
        Single Keyword    ${argument}
    ELSE
        Normal Keyword    abc
    END
