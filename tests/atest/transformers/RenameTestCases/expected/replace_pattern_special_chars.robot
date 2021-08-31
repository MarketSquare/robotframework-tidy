*** Test Cases ***
Starting with small case
    log  1

Ending with dot
    No Operation

Ending with dot and containing variables    column name    another column
    No Operation

Containing replace pattern JIRA-1234
    [Tags]    tag
    No Operation

Remove special chars
    No Operation
