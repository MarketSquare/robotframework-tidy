.. _AddMissingEnd:

AddMissingEnd
================================

Add missing ``END`` token to FOR loops and IF statements.

.. |TRANSFORMERNAME| replace:: AddMissingEnd
.. include:: enabled_hint.txt

.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

            *** Test Cases ***
            Test
                FOR    ${x}    IN    foo    bar
                    Log    ${x}
                IF    ${condition}
                    Log    ${x}
                    IF    ${condition}
                        Log    ${y}
                Keyword

    .. tab-item:: After

        .. code:: robotframework

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
