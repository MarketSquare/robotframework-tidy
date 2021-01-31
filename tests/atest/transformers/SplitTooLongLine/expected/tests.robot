*** Test Cases ***
Test
    Short Keyword
    This line is quite long and is going and going and going and going and going and going and going and going and going until max char length
    This line is quite long and is going and going  ${arguuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuument}    ${argsssssssssssssssssssssssssssssssssssss}
    ${ret}    ${ret2}    This line is quite long and is going and going  ${arguuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuument}    ${argsssssssssssssssssssssssssssssssssssss}
    This is short keyword but with long comment  ${arg}  # I am commmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmment
    This is short keyword but with long comment  ${arg}  # I am commmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmment
    This is long and multineeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee    ${arg}
    ...    ${arg2}
    Short Keyword With Long Second Line
    ...    ${argument}    ${argument}    ${argument}    ${argument}    ${argument}    ${argument}    ${argument}    ${argument}    ${argument}
    FOR  ${i}  IN RANGE  10
        Short Keyword
        Short Keyword With Long Second Line
            ...    ${argument}    ${argument}    ${argument}    ${argument}    ${argument}    ${argument}    ${argument}    ${argument}    ${argument}
    END
    IF    ${condition}
                               Over Indented But Not In Scope Of This Transformer
                               This is long and multine but we want to keep indentation as it isssssssssssssssssssssssssss    ${arg}
    ...    ${arg2}
    END
    # for loops, nested ifs etc