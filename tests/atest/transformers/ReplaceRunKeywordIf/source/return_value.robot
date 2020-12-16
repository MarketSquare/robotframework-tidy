*** Test Cases ***
Single Return Value
    ${var}  Run Keyword If  ${condition}  Keyword With ${var}  ${arg}

Multiple Return Values
    ${var}  ${var2}  Run Keyword If  ${condition}  Keyword With ${var}  ${arg}

Common Condition And Return Values
   ${var}  Run Keyword If  ${condition}  Keyword
   @{variable}  Run Keyword If  ${condition}  Another Keyword  ${arg}  5
   Run Keyword If  ${condition2}  Other Keyword

Nested Structure
   TO DO later

ELSE IF Branches
    TO DO later
