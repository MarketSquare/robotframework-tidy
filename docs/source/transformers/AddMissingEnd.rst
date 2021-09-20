.. _AddMissingEnd:

AddMissingEnd
================================

Add missing END token to FOR loops and IF statements.

AddMissingEnd is included in default transformers but it can be also
run separately with::

   robotidy --transform AddMissingEnd src

.. tabs::

    .. code-tab:: robotframework Before

        FOR    ${x}    IN    foo    bar
            Log    ${x}
        IF    ${condition}
            Log    ${x}
            IF    ${condition}
                Log    ${y}
        Keyword

   .. code-tab:: robotframework After

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
