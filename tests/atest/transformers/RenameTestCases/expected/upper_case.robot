*** Test Cases ***
Starting With Small Case
    log  1

Ending With Dot
    No Operation

Ending With Dot And Containing Variables    column name    another column
    No Operation

Containing Replace Pattern JIRA-1234
    [Tags]    tag
    No Operation

Remove Special Chars: ?$@
    No Operation
