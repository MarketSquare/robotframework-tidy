.. _ReplaceRunKeywordIf:

ReplaceRunKeywordIf
================================

Replace ``Run Keyword If`` keyword calls with IF expressions.

ReplaceRunKeywordIf is included in default transformers but it can be also
run separately with::

    robotidy --transform ReplaceRunKeywordIf src

.. tabs::

    .. code-tab:: robotframework Before

        Run Keyword If  ${condition}
        ...  Keyword  ${arg}
        ...  ELSE IF  ${condition2}  Keyword2
        ...  ELSE  Keyword3

    .. code-tab:: robotframework After

        IF    ${condition}
            Keyword    ${arg}
        ELSE IF    ${condition2}
            Keyword2
        ELSE
            Keyword3
        END

Any return value will be applied to every ELSE/ELSE IF branch.

.. tabs::

    .. code-tab:: robotframework Before

        ${var}  Run Keyword If  ${condition}  Keyword  ELSE  Keyword2

    .. code-tab:: robotframework After

        IF    ${condition}
            ${var}    Keyword
        ELSE
            ${var}    Keyword2
        END

Run Keywords inside Run Keyword If will be splitted into separate keywords.

.. tabs::

    .. code-tab:: robotframework Before

        Run Keyword If  ${condition}  Run Keywords  Keyword  ${arg}  AND  Keyword2

    .. code-tab:: robotframework After

        IF    ${condition}
            Keyword    ${arg}
            Keyword2
        END

Supports global formatting params: ``--spacecount``, ``--startline`` and ``--endline``.