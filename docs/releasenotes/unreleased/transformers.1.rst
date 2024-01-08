New VAR syntax support in RenameVariables
------------------------------------------

Robot Framework 7.0 introduces new syntax for creating variables: ``VAR``. It is now also supported in Robotidy in
``RenameVariables`` transformer:

Example renaming variables based on the scope. From:

```
*** Test Cases ***
    # Create a local variable `${local}` with a value `value`.
    VAR    ${local}    value

    # Create a variable that is available throughout the whole suite.
    # Supported scopes are GLOBAL, SUITE, TEST, TASK and LOCAL (default).
    VAR    ${suite}    value    scope=SUITE
    VAR    ${global}    value    scope=GLOBAL
    VAR    ${test}    value    scope=TEST
    VAR    ${task}    value    scope=TASK
    VAR    ${local_default}    value    scope=local

    # Validate created variables.
    Should Be Equal    ${local}    value
    Should Be Equal    ${suite}    value
    Should Be Equal    ${global}    value
    Should Be Equal    ${test}    value
    Should Be Equal    ${task}    value
```

To:

```
    # Create a local variable `${local}` with a value `value`.
    VAR    ${local}    value

    # Create a variable that is available throughout the whole suite.
    # Supported scopes are GLOBAL, SUITE, TEST, TASK and LOCAL (default).
    VAR    ${SUITE}    value    scope=SUITE
    VAR    ${GLOBAL}    value    scope=GLOBAL
    VAR    ${TEST}    value    scope=TEST
    VAR    ${TASK}    value    scope=TASK
    VAR    ${local_default}    value    scope=local

    # Validate created variables.
    Should Be Equal    ${local}    value
    Should Be Equal    ${SUITE}    value
    Should Be Equal    ${GLOBAL}    value
    Should Be Equal    ${TEST}    value
    Should Be Equal    ${TASK}    value
```
