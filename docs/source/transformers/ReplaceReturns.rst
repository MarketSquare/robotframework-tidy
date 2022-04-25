.. _ReplaceReturns:

ReplaceReturns
================================
Replace return statements (such as ``[Return]`` setting or ``Return From Keyword`` keyword) with new ``RETURN`` statement.

.. note::
    Required Robot Framework version: >=5.0

.. |TRANSFORMERNAME| replace:: ReplaceReturns
.. include:: enabled_hint.txt

This transformer replace ``[Return]`` statement with ``RETURN``:

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

Supports global formatting params: ``--startline`` and ``--endline``.
