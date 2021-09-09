.. _RenameKeywords:

RenameKeywords
================================

Enforce keyword naming. Title Case is applied to keyword name and underscores are replaced by spaces. It have only basic
support for keywords with embedded variables - use it on your own risk.

RenameKeywords is not included in default transformers, that's why you need to call it with ``--transform`` explicitly::

    robotidy --transform RenameKeywords src

Or configure `enable` parameter::

    robotidy --configure RenameKeywords:enabled=True

You can keep underscores if you set remove_underscores to False::

    robotidy --transform RenameKeywords -c RenameKeywords:remove_underscores=False .

It is also possible to configure `replace_pattern` parameter to find and replace regex pattern. Use `replace_to`
to set replacement value. This configuration (underscores are used instead of spaces)::

    robotidy --transform RenameKeywords -c RenameKeywords:replace_pattern=(?i)^rename\s?me$:replace_to=New_Shining_Name .

replaces all occurrences of name `Rename Me` (case insensitive thanks to `(?i)` flag) to `New Shining Name`:

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