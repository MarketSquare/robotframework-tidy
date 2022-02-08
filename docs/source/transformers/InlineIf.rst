.. _InlineIf:

InlineIf
================================
Replaces IF blocks with inline IF.

InlineIf is included in default transformers but it can be also run separately with::

   robotidy --transform InlineIf src

It will only replace IF block if it can fit in one line shorter than ``--line-length``.

Simple IF blocks that will be replaced by inline IF:

.. tabs::

    .. code-tab:: robotframework Before

        *** Keywords ***
        Keyword
            IF    $condition1
                Keyword    argument
            ELSE IF    $condition2
                Keyword    argument2
            END
            IF    $condition2
                RETURN
            END

    .. code-tab:: robotframework After

        *** Keywords ***
        Keyword
            IF    $condition1    Keyword    argument    ELSE IF    $condition2    Keyword    argument2
            IF    $condition2    RETURN

Assignments are also supported as long all ELSE and ELSE IF branches have matching return variables and there is ELSE
branch. ELSE branch is required because without it assignment variable would be overwritten with ``None`` without
your consent:

.. tabs::

    .. code-tab:: robotframework Before

        *** Keywords ***
        Keyword
        # assignment variable but missing ELSE
        IF    $condition
            ${var}    Keyword
        END
        # assignment variables and ELSE branch
        IF    $condition
            ${var}    ${var2}    Keyword
        ELSE
            ${var}    ${var2}    Keyword 2
        END
        # assignment variable and ELSE branch but variable name does not match
        IF    $condition
            ${var}    Keyword
        ELSE
            ${other_var}    Keyword 2
        END

    .. code-tab:: robotframework After

        *** Keywords ***
        Keyword
        # assignment variable but missing ELSE
        IF    $condition
            ${var}    Keyword
        END
        # assignment variables and ELSE branch
        ${var}    ${var2}    IF    $condition    Keyword    ELSE    Keyword 2
        # assignment variable and ELSE branch but variable name does not match
        IF    $condition
            ${var}    Keyword
        ELSE
            ${other_var}    Keyword 2
        END

Inline IF will be only used if resulting IF will be shorter than ``line_length`` parameter (default value is ``120``).
Multi statements IF blocks are also skipped:

.. tabs::

    .. code-tab:: robotframework Before

        *** Keywords ***
        Keyword
            FOR    ${var}    IN    @{array}
                # Infline IF would not fit under --line-length
                IF    $condition == "some value"
                    Longer Keyword That Will Not Fit In One Line    ${argument}    ${argument2}
                ELIF    $condition == "other value"
                    Longer Keyword That Will Not Fit In One Line    ${argument3}    ${argument4}
                END
            END
            # multi statements inside IF
            IF    $condition
                Keyword
                Other Keyword
            END

    .. code-tab:: robotframework After

        *** Keywords ***
        Keyword
            FOR    ${var}    IN    @{array}
                # Infline IF would not fit under --line-length
                IF    $condition == "some value"
                    Longer Keyword That Will Not Fit In One Line    ${argument}    ${argument2}
                ELIF    $condition == "other value"
                    Longer Keyword That Will Not Fit In One Line    ${argument3}    ${argument4}
                END
            END
            # multi statements inside IF
            IF    $condition
                Keyword
                Other Keyword
            END

Supports global formatting params: ``--startline`` and ``--endline``.