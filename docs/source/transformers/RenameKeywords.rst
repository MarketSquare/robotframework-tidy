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
By default library name in keyword name is ignored. Anything before the last dot in the name is considered as a library name.
Use `ignore_library = True` parameter to control if the library name part (Library.Keyword) of keyword call
should be renamed.

.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

            *** Keywords ***
            Keyword
                library_name.keyword

    .. tab-item:: ignore_library = True

        .. code:: robotframework

            *** Keywords ***
            Keyword
                library_name.Keyword

    .. tab-item:: ignore_library = False

        .. code:: robotframework

            *** Keywords ***
            Keyword
                Library Name.Keyword

Replace pattern
---------------
It is also possible to configure ``replace_pattern`` parameter to find and replace regex pattern. Use ``replace_to``
to set replacement value. This configuration (underscores are used instead of spaces)::

    robotidy --transform RenameKeywords -c RenameKeywords:replace_pattern=(?i)^rename\s?me$:replace_to=New_Shining_Name .

replaces all occurrences of name ``Rename Me``` (case insensitive thanks to ``(?i)`` flag) to ``New Shining Name``:

.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

            *** Keywords ***
            rename Me
               Keyword Call

    .. tab-item:: After

        .. code:: robotframework

            *** Keywords ***
            New Shining Name
                Keyword Call

This feature makes this transformer convenient tool for renaming your keywords across Robot Framework project.
