.. _NormalizeAssignments:

NormalizeAssignments
================================

Normalize assignments. By default it detects most common assignment sign
and apply it to every assignment in given file.

In this code most common is no equal sign at all. We should remove ``=`` signs from the all lines::

    *** Variables ***
    ${var} =  ${1}
    @{list}  a
    ...  b
    ...  c

    ${variable}=  10


    *** Keywords ***
    Keyword
        ${var}  Keyword1
        ${var}   Keyword2
        ${var}=    Keyword

To::

    *** Variables ***
    ${var}  ${1}
    @{list}  a
    ...  b
    ...  c

    ${variable}  10


    *** Keywords ***
    Keyword
        ${var}  Keyword1
        ${var}   Keyword2
        ${var}    Keyword

You can configure that behaviour to automatically add desired equal sign with ``equal_sign_type`` parameter
(possible types are: ``autodetect`` (default), ``remove``, ``equal_sign`` ('='), ``space_and_equal_sign`` (' =').