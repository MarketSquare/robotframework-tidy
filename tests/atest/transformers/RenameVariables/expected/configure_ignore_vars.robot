*** Test Cases ***
Not important variable
    ${_}    ${local}    Keyword    ${global_arg}
    ...
    ...    ${PREV_EMPTY}
    FOR    ${_}    IN    @{LIST}
        Log    ${_}
    END
    Multiple Underscores    ${_}    ${_}    ${_}    ${_}

*** Keywords ***
Not important variable
    ${_}    ${local}    Keyword    ${global_arg}
    ...
    ...    ${PREV_EMPTY}
    FOR    ${_}    IN    @{LIST}
        Log    ${_}
    END
    Multiple Underscores    ${_}    ${_}    ${_}    ${_}

Path and line separators
    Load From Path    C${:}/tests${/}file.csv
    Catenate    ${\n}
    ...    sentence
    ...    sentence2

Environment variable
    Log    %{APPLICATION_PORT=8080}
    Log    %{env_var}

True and False
    IF    $True
        Log    The truth.
    ELIF    ${False}
        Log    The lie.
    END
