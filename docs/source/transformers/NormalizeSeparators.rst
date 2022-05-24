.. _NormalizeSeparators:

NormalizeSeparators
================================

Normalize separators and indents.

.. |TRANSFORMERNAME| replace:: NormalizeSeparators
.. include:: enabled_hint.txt

All separators (pipes included) are converted to fixed length of 4 spaces (configurable via global option
``--spacecount``). To separately configure the indentation, use ``--indent`` global option.

.. note::
    There are transformers that also affect separator lengths - for example ``AlignSettingsSection``. ``NormalizeSeparators``
    is used as a base and then potentially overwritten by behaviours of other transformers. If you only want to have fixed
    separator lengths (without aligning) then only run this transformer without running the others.

.. tabs::

    .. code-tab:: robotframework Before

        *** Settings ***
        Library  library.py  WITH NAME          alias

        Force Tags           tag
        ...   tag

        Documentation  doc
        ...      multi
        ...  line

        *** Test Cases ***
        Test case
          [Setup]  Keyword
           Keyword  with  arg
           ...  and  multi  lines
             [Teardown]          Keyword

        Test case with structures
            FOR  ${variable}  IN  1  2
            Keyword
             IF  ${condition}
               Log  ${stuff}  console=True
          END
           END

    .. code-tab:: robotframework After

        *** Settings ***
        Library    library.py    WITH NAME    alias

        Force Tags    tag
        ...    tag

        Documentation    doc
        ...    multi
        ...    line

        *** Test Cases ***
        Test case
            [Setup]    Keyword
            Keyword    with    arg
            ...    and    multi    lines
            [Teardown]    Keyword

        Test case with structures
            FOR    ${variable}    IN    1    2
                Keyword
                IF    ${condition}
                    Log    ${stuff}    console=True
                END
            END

Configure separator
--------------------

By configuring a global option ``spacecount``, you can change the default separator length::

    robotidy --spacecount 8 src

.. tabs::

    .. code-tab:: robotframework Before

        *** Settings ***
        Library  library.py  WITH NAME          alias

        Force Tags           tag
        ...   tag

    .. code-tab:: robotframework After

        *** Settings ***
        Library        library.py        WITH NAME        alias

        Force Tags        tag
        ...        tag

Indentation
-------

By default, indentation is the same as ``spacecount`` value (default ``4`` spaces). To configure it, use ``--indent``::

    robotidy --indent 4 src

Combine it with ``spacecount`` to set whitespace separately for indent and separators::

    robotidy --indent 4 --spacecount 2 src

.. tabs::

    .. code-tab:: robotframework Before

        *** Keywords ***
        Keyword
          FOR     ${var}  IN RANGE     10
            Keyword With  ${var}
          END

    .. code-tab:: robotframework After

        *** Keywords ***
        Keyword
            FOR  ${var}  IN RANGE  10
                Keyword With  ${var}
            END

Ignored sections
---------------

You can decide which sections should be transformed by configuring
``sections = comments,settings,variables,keywords,testcases`` param::

    robotidy --configure NormalizeSeparators:section=variables src

.. tabs::

    .. code-tab:: robotframework Before

        *** Settings ***
        Library  library.py  WITH NAME          alias

        Force Tags           tag
        ...   tag

        *** Variables ***
        ${var}  1  # only this section will be transformed

    .. code-tab:: robotframework After

        *** Settings ***
        Library  library.py  WITH NAME          alias

        Force Tags           tag
        ...   tag

        *** Variables ***
        ${var}    1    # only this section will be transformed

Supports global formatting params: ``--startline`` and ``--endline``.