Handle default default of environment variable in RenameVariables (#677)
------------------------------------------------------------------------

``RenameVariables`` did not handle default value of environment variable correctly. Now following code::

    Set Test Variable    ${local variable}    %{env variable=string message}
    Log    %{MY_ENV=${global}}
    Log    %{my env=${global} with extra}

should be transformed to::

    Set Test Variable    ${local_variable}    %{ENV_VARIABLE=string message}
    Log    %{MY_ENV=${GLOBAL}}
    Log    %{MY_ENV=${DEFAULT} with extra string}
