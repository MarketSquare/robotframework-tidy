Invalid variable case with extended syntax in RenameVariables (#551)
--------------------------------------------------------------------

Robotidy should now be able to recognize variables using extended variable syntax and set variable case accordingly::

    *** Test Cases ***
    Simple math operations
        ${i}    Set Variable    ${0}
        Log    ${i+1}  # i+1 instead of previous I+1
