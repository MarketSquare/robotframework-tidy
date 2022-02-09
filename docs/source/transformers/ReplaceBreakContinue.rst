.. _ReplaceBreakContinue:

ReplaceBreakContinue
================================
Replace Continue For Loop and Exit For Loop keyword variants with CONTINUE and BREAK statements.

ReplaceBreakContinue is included in default transformers but it can be also run separately with::

   robotidy --transform ReplaceBreakContinue src

It will replace ``Continue For Loop`` and ``Exit For Loop`` keywords with ``CONTINUE`` and ``BREAK`` respectively:


.. tabs::

    .. code-tab:: robotframework Before

        *** Test Cases ***
        Test
            WHILE    $flag
                Continue For Loop
            END
            FOR    ${var}    IN    abc
                Exit For Loop
            END

    .. code-tab:: robotframework After

        *** Test Cases ***
        Test
            WHILE    $flag
                CONTINUE
            END
            FOR    ${var}    IN    abc
                BREAK
            END

Conditional variants are also handled. Shorter IFs can be also formatted to inline ``IF`` with :ref:`InlineIf` transformer:

.. tabs::

    .. code-tab:: robotframework Before

        *** Test Cases ***
        Test
            WHILE    $flag
                Continue For Loop If    $condition
            END
            FOR    ${var}    IN    abc
                Exit For Loop If    $condition
            END

    .. code-tab:: robotframework After

        *** Test Cases ***
        Test
            WHILE    $flag
                IF    $condition
                    CONTINUE
                END
            END
            FOR    ${var}    IN    abc
                IF    $condition
                    BREAK
                END
            END

``Continue For Loop`` and ``Exit For Loop`` along with conditional variants outside of the loop are ignored.

Supports global formatting params: ``--startline`` and ``--endline``.