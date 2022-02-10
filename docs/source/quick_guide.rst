Quickstart
===========
`Robotidy` is easy to use and you can do it just by running::

    robotidy path/to/file_or_directory.robot

Displaying the difference
--------------------------
If you want to see which lines are changed by tool add ``--diff`` flag::

    robotidy --diff test.robot
    --- test.robot before
    +++ test.robot after
    @@ -1,23 +1,15 @@
     *** Test Cases ***
    Simple IF
    -    IF    $condition1
    -        Keyword    argument
    -    END
    -    IF    $condition2
    -        RETURN
    -    END
    +    IF    $condition1    Keyword    argument
    +    IF    $condition2    RETURN

Do not overwrite files
-----------------------
Pass ``--no-overwrite`` flag to not modify the files when running the `Robotidy`. Combine it with ``--diff`` to run a preview
of how files will look after formatting::

    robotidy --no-overwrite test.robot

Status code
------------
By default `Robotidy` returns 0 exit code after successful run and 1 if there was an error. You can make `Robotidy` exit 1
if any file would be transformed by passing ``--check``. By default files will not be transformed (same as running with
``--no-overwrite``::

    robotidy --check golden.robot
    0
    robotidy --check ugly.robot
    1

If you want `Robotidy` to transform the files while using ``--check`` flag add ``--overwrite`::

    robotidy --check --overwrite file.robot

Configuration
--------------
See :ref:`configuration` for information how to configure `Robotidy`.

Listing transformers
---------------------
To see list of transformers included with `Robotidy` use ``--list``::

    robotidy --list
    To see detailed docs run --desc <transformer_name> or --desc all. Transformers with (disabled) tag
    are executed only when selected explicitly with --transform or configured with param `enabled=True`.
    Available transformers:

    AddMissingEnd
    AlignSettingsSection
    AlignTestCases (disabled)
    AlignVariablesSection
    DiscardEmptySections
    InlineIf
    MergeAndOrderSections
    NormalizeAssignments
    NormalizeNewLines
    NormalizeSectionHeaderName
    NormalizeSeparators
    NormalizeSettingName
    NormalizeTags
    OrderSettings
    OrderSettingsSection
    OrderTags (disabled)
    RemoveEmptySettings
    RenameKeywords (disabled)
    RenameTestCases (disabled)
    ReplaceBreakContinue
    ReplaceReturns
    ReplaceRunKeywordIf
    SmartSortKeywords (disabled)
    SplitTooLongLine

You can display short documentation on particular transformer with ``--desc``::

    robotidy --desc DiscardEmptySections
    Transformer DiscardEmptySections:

        Remove empty sections.
        Sections are considered empty if there are only empty lines inside.
        You can remove sections with only comments by setting 'allow_only_comments' parameter to False:

            *** Variables ***
            # this section will be removed with'alow_only_comments' parameter set to False

        Supports global formatting params: '--startline' and '--endline'.

        See https://robotidy.readthedocs.io/en/latest/transformers/DiscardEmptySections.html for more examples.

Transform selected lines
-------------------------
Most transformers support running `Robotidy` only on selected lines. Use ``--startline`` and ``--endline`` for this::

    robotidy --startline 5 --endline 10 file.robot

Transform code from standard input
-----------------------------------
Use ``-`` to load code from input::

    cat file.robot | robotidy -
