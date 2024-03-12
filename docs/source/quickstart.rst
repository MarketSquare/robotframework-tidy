.. _quickstart:

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
``--no-overwrite``)::

    robotidy --check golden.robot
    0
    robotidy --check ugly.robot
    1

If you want `Robotidy` to transform the files while using ``--check`` flag add ``--overwrite``::

    robotidy --check --overwrite file.robot

Configuration
--------------
See :ref:`configuration` for information how to configure `Robotidy`.

Listing transformers
---------------------
To see list of transformers included with `Robotidy` use ``--list``::

    > robotidy --list
                  Transformers
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┓
    ┃ Name                       ┃ Enabled ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━┩
    │ AddMissingEnd              │ Yes     │
    │ NormalizeSeparators        │ Yes     │
    │ DiscardEmptySections       │ Yes     │
    │ MergeAndOrderSections      │ Yes     │
    │ RemoveEmptySettings        │ Yes     │
    │ NormalizeAssignments       │ Yes     │
    │ OrderSettings              │ Yes     │
    │ OrderSettingsSection       │ Yes     │
    │ NormalizeTags              │ Yes     │
    │ OrderTags                  │ No      │
    │ IndentNestedKeywords       │ No      │
    │ AlignSettingsSection       │ Yes     │
    │ AlignVariablesSection      │ Yes     │
    │ AlignTemplatedTestCases    │ No      │
    │ AlignTestCasesSection      │ No      │
    │ AlignKeywordsSection       │ No      │
    │ NormalizeNewLines          │ Yes     │
    │ NormalizeSectionHeaderName │ Yes     │
    │ NormalizeSettingName       │ Yes     │
    │ ReplaceRunKeywordIf        │ Yes     │
    │ SplitTooLongLine           │ Yes     │
    │ SmartSortKeywords          │ No      │
    │ RenameTestCases            │ No      │
    │ RenameKeywords             │ No      │
    │ ReplaceReturns             │ Yes     │
    │ ReplaceBreakContinue       │ Yes     │
    │ InlineIf                   │ Yes     │
    │ Translate                  │ No      │
    └────────────────────────────┴─────────┘
    Transformers are listed in the order they are run by default. The status of the transformer will be displayed in different color if it is changed by the configuration.
    To see detailed docs run:
        robotidy --desc transformer_name
    or
        robotidy --desc all

    Non-default transformers needs to be selected explicitly with --transform or configured with param `enabled=True`.

Pass optional value ``enabled`` or ``disabled`` to filter out output by the status of the transformer::

    > robotidy --list disabled
                    Transformers
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┓
    ┃ Name                    ┃ Enabled ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━┩
    │ OrderTags               │ No      │
    │ IndentNestedKeywords    │ No      │
    │ AlignTemplatedTestCases │ No      │
    │ AlignTestCasesSection   │ No      │
    │ AlignKeywordsSection    │ No      │
    │ SmartSortKeywords       │ No      │
    │ RenameTestCases         │ No      │
    │ RenameKeywords          │ No      │
    │ Translate               │ No      │
    └─────────────────────────┴─────────┘
    (...)

The configuration is reflected in the output. For example combining ``--transform`` (which only runs selected
transformers) and ``enabled`` gives us::

    > robotidy --transform DiscardEmptySections --list enabled
               Transformers
    ┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┓
    ┃ Name                 ┃ Enabled ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━┩
    │ DiscardEmptySections │ Yes     │
    └──────────────────────┴─────────┘
    (...)

You can display short documentation on particular transformer with ``--desc``::

    > robotidy --desc DiscardEmptySections
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

If you want to disable formatting in particular files see disablers section in :ref:`configuration`.

Transform code from standard input
-----------------------------------
Use ``-`` to load code from input::

    cat file.robot | robotidy -

Line endings
----------------

When working on multiple platforms the file can contain different line endings (``CRLF``, ``LF``). By default
Robotidy will replace all line endings with system native line ending. It may be problematic if you're using
different platforms. You can force specific line ending or autodetect line ending used in the file and use it by
configuring ``lineseparator`` option:

- native:  use operating system's native line endings (default)
- windows: use Windows line endings (CRLF)
- unix:    use Unix line endings (LF)
- auto:    maintain existing line endings (uses what's used in the first line of the file)

Rerun the transformation in place
----------------------------------

Because of high independence of each transformer, Robotidy runs them in specific order to obtain predictable results.
But sometimes the subsequent transformer modifies the file to the point that it requires another run of Robotidy.
Good example would be one transformer that replaces the deprecated syntax - but new syntax is inserted using standard
whitespace. If there is transformer that aligns this whitespace according to special rules
(like ``AlignKeywordsSection``) we need to run Robotidy again to format this whitespace.

This could be inconvenient in some cases where user had to rerun Robotidy without knowing why. That's why Robotidy
now has option ``reruns`` that allows to define limit of how many extra reruns Robotidy can perform if the
file keeps changing after the transformation. The default is ``0``. Recommended value is ``3``
although in vast majority of cases one extra run should suffice (and only in cases described above).

Example usage::

    > robotidy --reruns 3 --diff test.robot

Note that if you enable it, it can double the execution time of Robotidy (if the file was modified, it will be
transformed again to check if next transformation does not further modify the file).
