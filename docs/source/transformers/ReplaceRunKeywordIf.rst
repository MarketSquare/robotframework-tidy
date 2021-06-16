.. _ReplaceRunKeywordIf:

ReplaceRunKeywordIf
================================

Replace ``Run Keyword If`` keyword calls with IF END blocks.
Supports global formatting params: ``--spacecount``, ``--startline`` and ``--endline``.

Following code::

    Run Keyword If  ${condition}
    ...  Keyword  ${arg}
    ...  ELSE IF  ${condition2}  Keyword2
    ...  ELSE  Keyword3

Will be transformed to::

    IF    ${condition}
        Keyword    ${arg}
    ELSE IF    ${condition2}
        Keyword2
    ELSE
        Keyword3
    END

Any return value will be applied to every ELSE/ELSE IF branch::

    ${var}  Run Keyword If  ${condition}  Keyword  ELSE  Keyword2

Output::

    IF    ${condition}
        ${var}    Keyword
    ELSE
        ${var}    Keyword2
    END

Run Keywords inside Run Keyword If will be splitted into separate keywords::

   Run Keyword If  ${condition}  Run Keywords  Keyword  ${arg}  AND  Keyword2

Output::

    IF    ${condition}
        Keyword    ${arg}
        Keyword2
    END
