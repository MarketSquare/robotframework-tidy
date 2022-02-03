.. _ReplaceReturns:

ReplaceReturns
================================
Replace return statements (such as [Return] setting or Return From Keyword keyword) with new RETURN statement.

ReplaceReturns is included in default transformers but it can be also run separately with::

   robotidy --transform ReplaceReturns src

This transformer replace ``[Return]`` statement to ``RETURN``:

.. tabs::

    .. code-tab:: robotframework Before

        *** Keywords ***
        Keyword
            Sub Keyword
            [Return]    ${value}

    .. code-tab:: robotframework After

        *** Keywords ***
        Keyword
            Sub Keyword
            RETURN    ${value}

It also does replace ``Return From Keyword`` and ``Return From Keyword If``:

.. tabs::

    .. code-tab:: robotframework Before

        *** Keywords ***
        Keyword
            Return From Keyword If    $condition    ${value}
            Sub Keyword
            Return From Keyword    ${other_value}

    .. code-tab:: robotframework After

        *** Keywords ***
        Keyword
            IF    $condition
                RETURN    ${value}
            END
            Sub Keyword
            RETURN    ${other_value}

Run and return keyword variants such as ``Run Keyword And Return`` and ``Run Keyword And Return If`` are also replaced:

.. tabs::

    .. code-tab:: robotframework Before

        *** Keywords ***
        Keyword
            WHILE    ${x} > 0
                Run Keyword And Return If    ${x} == 10    Keyword    ${arg}
            END
            Sub Keyword
            Run Keyword And Return    Keyword    {argument}

    .. code-tab:: robotframework After

        *** Keywords ***
        Keyword
            WHILE    ${x} > 0
                IF    ${x} == 10
                    RETURN    Keyword    ${arg}
                END
            END
            Sub Keyword
            RETURN    Keyword    {argument}

Supports global formatting params: ``--startline`` and ``--endline``.