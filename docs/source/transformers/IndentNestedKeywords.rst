.. _IndentNestedKeywords:

IndentNestedKeywords
================================
Format indentation inside run keywords variants such as ``Run Keywords`` or ``Run Keyword And Continue On Failure``.

.. |TRANSFORMERNAME| replace:: IndentNestedKeywords
.. include:: disabled_hint.txt

Keywords inside run keywords variants are detected and whitespace is formatted to outline them.

.. tabs::

    .. code-tab:: robotframework Before

        *** Test Cases ***
        Test
            Run Keyword    Run Keyword If    ${True}    Run keywords   Log    foo    AND    Log    bar    ELSE    Log    baz

    .. code-tab:: robotframework After

        *** Test Cases ***
        Test
            Run Keyword
            ...    Run Keyword If    ${True}
            ...        Run keywords
            ...            Log    foo
            ...            AND
            ...            Log    bar
            ...    ELSE
            ...        Log    baz


It is possible to provide extra indentation for keywords using ``AND`` separators by configuring ``indent_and`` to
``True``::

    robotidy -c IndentNestedKeywords:indent_and=True src

.. tabs::

    .. code-tab:: robotframework indent_and=False (default)

        *** Test Cases ***
        Test
            Run keywords
            ...    Log    foo
            ...    AND
            ...    Log    bar

    .. code-tab:: robotframework indent_and=True

        *** Test Cases ***
        Test
            Run keywords
            ...        Log    foo
            ...    AND
            ...        Log    bar


Skip formatting settings
-------------------------
To skip formatting run keywords inside settings (such as ``Suite Setup``, ``[Setup]``, ``[Teardown]`` etc.) set
``skip_settings`` to ``True``::

    robotidy -c IndentNestedKeywords:skip_settings:True .

