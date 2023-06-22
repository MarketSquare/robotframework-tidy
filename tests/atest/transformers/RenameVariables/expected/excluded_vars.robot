*** Test Cases ***
Not important variable
    ${_}    ${local}    Keyword    ${GLOBAL_ARG}
    ...
    ...    ${PREV_EMPTY}
    FOR    ${_}    IN    @{LIST}
        Log    ${_}
    END
    Multiple Underscores    ${_}    ${_}    ${_}    ${_}

*** Keywords ***
Not important variable
    ${_}    ${local}    Keyword    ${GLOBAL_ARG}
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
    Log    %{ENV_VAR}
