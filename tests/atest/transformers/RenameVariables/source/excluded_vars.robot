*** Test Cases ***
Not important variable
    ${_}    ${local}    Keyword    ${global_arg}
    ...
    ...    ${prev_empty}
    FOR    ${_}    IN    @{LIST}
        Log    ${_}
    END
    Multiple Underscores    ${___}    ${ _}    ${_ }    ${ }

*** Keywords ***
Not important variable
    ${_}    ${local}    Keyword    ${global_arg}
    ...
    ...    ${prev_empty}
    FOR    ${_}    IN    @{LIST}
        Log    ${_}
    END
    Multiple Underscores    ${___}    ${ _}    ${_ }    ${ }

Path and line separators
    Load From Path    C${:}/tests${/}file.csv
    Catenate    ${\n}
    ...    sentence
    ...    sentence2

Environment variable
    Log    %{application_port=8080}
    Log    %{env_var}
