.. _NormalizeAssignments:

NormalizeAssignments
================================

Normalize assignments. By default it detects most common assignment sign
and apply it to every assignment in given file.

NormalizeAssignments is included in default transformers but it can be also
run separately with::

    robotidy --transform NormalizeAssignments src

In this code most common is no equal sign at all. It should remove ``=`` signs from all lines:

.. tabs::

    .. code-tab:: robotframework Before

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

    .. code-tab:: robotframework After

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
(possible types are: ``autodetect`` (default), ``remove``, ``equal_sign`` ('='), ``space_and_equal_sign`` (' =')::

    robotidy --configure NormalizeAssignments:equal_sign_type=space_and_equal_sign src

.. tabs::

    .. code-tab:: robotframework Before

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

    .. code-tab:: robotframework After

        *** Variables ***
        ${var} =  ${1}
        @{list} =  a
        ...  b
        ...  c

        ${variable} =  10


        *** Keywords ***
        Keyword
            ${var} =  Keyword1
            ${var} =   Keyword2
            ${var} =    Keyword
