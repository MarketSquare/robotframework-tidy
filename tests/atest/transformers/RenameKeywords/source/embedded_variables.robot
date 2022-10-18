*** Keywords ***
Embedded ${variables} That should Be ${ignored.and.dots}
    Login With '{user.uid}'_and '${user.password}' to Check_Validation

Variable With Square Brackets
    normalize_this${variable['test']}
    normalize_this${variable}['test']

Invalid Syntax
    Not Closed ${var
