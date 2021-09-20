.. _NormalizeAssignments:

NormalizeAssignments
================================

Normalize assignments.

It can change all assignment signs to either the most commonly used in a given file or a configured one.
Default behaviour is autodetect for assignments from Keyword Calls and removing assignment signs in
``*** Variables ***`` section. It can be freely configured.

NormalizeAssignments is included in the default transformers but it can be also run separately with::

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

You can configure that behaviour to automatically add desired equal sign with `equal_sign_type`
(default `autodetect`) and `equal_sign_type_variables` (default `remove`) parameters.
(possible types are: `autodetect`, `remove`, `equal_sign` ('='), `space_and_equal_sign` (' =')::

    robotidy -c NormalizeAssignments:equal_sign_type=space_and_equal_sign -c NormalizeAssignments:equal_sign_type_variables=autodetect src

.. tabs::

    .. code-tab:: robotframework Before

        *** Variables ***
        ${var}=  ${1}
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
        ${var}=  ${1}
        @{list}=  a
        ...  b
        ...  c

        ${variable}=  10


        *** Keywords ***
        Keyword
            ${var} =  Keyword1
            ${var} =   Keyword2
            ${var} =    Keyword
