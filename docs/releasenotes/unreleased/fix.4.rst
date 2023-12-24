Set Local Variable not supported in RenameVariables (#593)
----------------------------------------------------------

``Set Local Variable`` keyword is now supported and scope of the variable is properly preserved:

```
${variable}    Set Variable    value
Set Global Variable    ${VARIABLE}
Log    ${VARIABLE}
Set Local Variable    ${variable}
Log    ${variable}
```
