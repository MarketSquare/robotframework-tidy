.. _IndentRunKeywords:

IndentRunKeywords
================================
Format indentation inside run keywords variants such as ``Run Keywords`` or ``Run Keyword And Continue On Failure``.

.. |TRANSFORMERNAME| replace:: IndentRunKeywords
.. include:: disabled_hint.txt

Keywords inside run keywords variants are detected and whitespace is formatted to outline them. This code:

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

    robotidy -c IndentRunKeywords:indent_and=True src

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
