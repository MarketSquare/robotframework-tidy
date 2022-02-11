.. _AddMissingEnd:

AddMissingEnd
================================

Add missing END token to FOR loops and IF statements.

.. |TRANSFORMERNAME| replace:: AddMissingEnd
.. include:: enabled_hint.txt

.. tabs::

    .. code-tab:: robotframework Before

        *** Test Cases ***
        Test
            FOR    ${x}    IN    foo    bar
                Log    ${x}
            IF    ${condition}
                Log    ${x}
                IF    ${condition}
                    Log    ${y}
            Keyword

    .. code-tab:: robotframework After

        *** Test Cases ***
        Test
            FOR    ${x}    IN    foo    bar
                Log    ${x}
            END
            IF    ${condition}
                Log    ${x}
                IF    ${condition}
                    Log    ${y}
                END
            END
            Keyword

AddMissingEnd transformer supports global formatting params: ``--startline`` and ``--endline``.
