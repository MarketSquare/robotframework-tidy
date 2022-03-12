.. _RenameKeywords:

RenameKeywords
================================

Enforce keyword naming. Title Case is applied to keyword name and underscores are replaced by spaces. It has only basic
support for keywords with embedded variables - use it on your own risk.

.. |TRANSFORMERNAME| replace:: RenameKeywords
.. include:: disabled_hint.txt

You can keep underscores if you set remove_underscores to False::

    robotidy --transform RenameKeywords -c RenameKeywords:remove_underscores=False .

Library name
------------
By default library name in keyword name is ignored. Anything before last dot in name is considered as library name.
Use `ignore_library = True` parameter to control if the library name part (Library.Keyword) of keyword call
should be renamed.

.. tabs::

    .. code-tab:: robotframework Before

        *** Keywords ***
        Keyword
            library_name.keyword

    .. code-tab:: robotframework After (default)

        *** Keywords ***
        Keyword
            library_name.Keyword

    .. code-tab:: robotframework After (``ignore_library=False``)

        *** Keywords ***
        Keyword
            Library Name.Keyword

Replace pattern
---------------
It is also possible to configure ``replace_pattern`` parameter to find and replace regex pattern. Use ``replace_to``
to set replacement value. This configuration (underscores are used instead of spaces)::

    robotidy --transform RenameKeywords -c RenameKeywords:replace_pattern=(?i)^rename\s?me$:replace_to=New_Shining_Name .

replaces all occurrences of name ``Rename Me``` (case insensitive thanks to ``(?i)`` flag) to ``New Shining Name``:

.. tabs::

    .. code-tab:: robotframework Before

        *** Keywords ***
        rename Me
           Keyword Call

    .. code-tab:: robotframework After

        *** Keywords ***
        New Shining Name
            Keyword Call

This feature makes this transformer convenient tool for renaming your keywords across Robot Framework project.

Supports global formatting params: ``--startline`` and ``--endline``.