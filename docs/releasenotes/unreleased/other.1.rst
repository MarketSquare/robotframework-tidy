Generate configuration file (#563)
-----------------------------------

New option to generate configuration file with most important options and their default values::

    robotidy --generate-config

It is only enabled after installing optional ``generate_config`` profile::

    pip install robotidy[generate_config]

Generated configuration contains all transformers with their enabled status. Example of the file::

    [tool.robotidy]
    diff = false
    overwrite = true
    verbose = false
    separator = "space"
    spacecount = 4
    line_length = 120
    lineseparator = "native"
    skip_gitignore = false
    ignore_git_dir = false
    configure = [
        "AddMissingEnd:enabled=True",
        "NormalizeSeparators:enabled=True",
        "DiscardEmptySections:enabled=True",
        "MergeAndOrderSections:enabled=True",
        "RemoveEmptySettings:enabled=True",
        "ReplaceEmptyValues:enabled=True",
        "NormalizeAssignments:enabled=True",
        "GenerateDocumentation:enabled=False",
        "OrderSettings:enabled=True",
        "OrderSettingsSection:enabled=True",
        "NormalizeTags:enabled=True",
        "OrderTags:enabled=False",
        "RenameVariables:enabled=False",
        "IndentNestedKeywords:enabled=False",
        "AlignSettingsSection:enabled=True",
        "AlignVariablesSection:enabled=True",
        "AlignTemplatedTestCases:enabled=False",
        "AlignTestCasesSection:enabled=False",
        "AlignKeywordsSection:enabled=False",
        "NormalizeNewLines:enabled=True",
        "NormalizeSectionHeaderName:enabled=True",
        "NormalizeSettingName:enabled=True",
        "ReplaceRunKeywordIf:enabled=True",
        "SplitTooLongLine:enabled=True",
        "SmartSortKeywords:enabled=False",
        "RenameTestCases:enabled=False",
        "RenameKeywords:enabled=False",
        "ReplaceReturns:enabled=True",
        "ReplaceBreakContinue:enabled=True",
        "InlineIf:enabled=True",
        "Translate:enabled=False",
        "NormalizeComments:enabled=True",
    ]
