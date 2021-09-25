.. _NormalizeSeparators:

NormalizeSeparators
================================

Normalize separators and indents.

NormalizeSeparators is included in the default transformers but it can be also run separately with::

    robotidy --transform NormalizeSeparators src

All separators (pipes included) are converted to fixed length of 4 spaces (configurable via global argument
``--spacecount``).

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

By configuring global option ``spacecount`` you can change the default separator length::

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