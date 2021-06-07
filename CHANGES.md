# Change Log

## Unreleased

### Transformers

- AlignVariablesSection now supports ``--startline`` and ``--endline`` options for aligning only part of ``*** Variables ***`` section [#62](https://github.com/MarketSquare/robotframework-tidy/issues/62)
- AlignVariablesSection now supports ``up_to_column`` parameter so it is possible to chose how much column are width aligned
- AlignVariablesSection and AlignSettingsSection change ``up_to_column`` default value from 0 (meaning all columns) to 2 (only first two columns are width aligned, rest use fixed length) #
- New AlignSettingsSection for aligning ``*** Settings ***`` section into columns [#60](https://github.com/MarketSquare/robotframework-tidy/issues/60)
- New NormalizeSeparators for normalizing all separators and indents to fixed length (according to global ``--spacecount`` option) [#32](https://github.com/MarketSquare/robotframework-tidy/issues/32)
- New RemoveEmptySettings transformer for removing empty settings such like `Suite Setup` or `[Arguments]`. Settings that are overwriting suite settings (like empty `[Tags]` overwriting `Default Tags`) are preserved. See the docs for config options [#78](https://github.com/MarketSquare/robotframework-tidy/issues/78)
- New SmartSortKeywords transformer (disabled by default) for sorting out keywords inside ``*** Keywords ***`` section [#52](https://github.com/MarketSquare/robotframework-tidy/issues/52)
- New MergeAndOrderSections transformer for merging duplicated sections and ordering them (order is configurable) [#70](https://github.com/MarketSquare/robotframework-tidy/issues/70)
- New OrderSettings transformer for ordering settings like [Arguments], [Setup], [Return] inside Keywords and Test Cases [#59](https://github.com/MarketSquare/robotframework-tidy/issues/59)

### Features
- New option ``--configure`` or ``-c`` for configuring transformer parameters. It works the same way configuring through ``--transform`` works. The benefit of using ``--configure`` is that you can configure selected transformers and still run all transformers [#96](https://github.com/MarketSquare/robotframework-tidy/issues/96)
- Transformers can now be disabled by default if you add ``ENABLED = False`` class attribute to your class. Those transformers will be only run when selected explictly with ``--transform`` option [#10](https://github.com/MarketSquare/robotframework-tidy/issues/10)
- Support for ``pyproject.toml`` configuration files. Because of the required changes there are backward incompatible changes done to ``robotidy.toml`` syntax. See example from [README](https://github.com/MarketSquare/robotframework-tidy/blob/main/README.rst#configuration-file) [#66](https://github.com/MarketSquare/robotframework-tidy/issues/66)
- ``--list-transformers`` output is now ordered. Also transformers themselves will always run in the same predefined order [#69](https://github.com/MarketSquare/robotframework-tidy/issues/69)
- ``--describe-transformer`` output is now pre-formatted (removed rst formatting) [#83](https://github.com/MarketSquare/robotframework-tidy/issues/83)
- Several options have now abbreviations: [#92](https://github.com/MarketSquare/robotframework-tidy/issues/92)
  - ``--transform`` can be also used with ``-t``
  - ``--list-transformers`` can be also used with ``--list`` or ``-l``
  - ``--describe-transformer`` can be also used with ``--desc`` or ``-d`` 

### Fixes
- SplitTooLongLine will now parse multiple assignment values correctly [#68](https://github.com/MarketSquare/robotframework-tidy/issues/68)
- AlignSettingsSection is now parsing empty lines in multi lines correctly (those lines are removed) [#75](https://github.com/MarketSquare/robotframework-tidy/issues/75)
- Fix ``--diff`` option not displaying colours on Windows [#86](https://github.com/MarketSquare/robotframework-tidy/issues/86)
- Fix issue where variable was not left aligned if name was prefixed with space (`` {variable} 4``) [#88](https://github.com/MarketSquare/robotframework-tidy/issues/88)

### Other
- Support for pipes is now removed. All pipes will be converted to spaces by NormalizeSeparators transformer. It can be restored if people that use pipe syntax request for it
- Files with invalid encoding will now not stop robotidy execution - warning will be printed instead

## 1.1.1

### Fixes

- AlignVariablesSection should ignore lines with only comments

## 1.1.0

### Transformers

- Added alignVariablesSection for aligning variables and their values in column like appearance [#50](https://github.com/MarketSquare/robotframework-tidy/issues/50)

### Fixes

- Robotidy should not add new (extra) line at the end of file [#47](https://github.com/MarketSquare/robotframework-tidy/issues/47)
- BuiltIn.Run Keyword If should now work with ReplaceRunKeywordIf transformer [#53](https://github.com/MarketSquare/robotframework-tidy/issues/53)

## 1.0.0

### Transformers

- DiscardEmptySections - empty sections are removed
- SplitTooLongLine - keywords with too long lines are splitted
- NormalizeSettingName - ensure that setting names are Title Case - Test Template, Library
- AssignmentNormalizer - use only one type of assignment
- NormalizeNewLines - ensure proper number of empty lines between keywords, test cases and sections
- NormalizeSectionHeaderName - ensure that sections are in ``*** Section ***`` or ``*** SECTION ***`` format
- ReplaceRunKeywordIf - replace RunKeywordIf with IF blocks

### Features

- configurable transformers
- selectable transformers (chose how you want to transform your code)
- robotidy configuration can be supplied from cli and config file (which can be pointed to or autodetected in directory if the name is 'robotidy.toml'
- option ``--no-overview`` to disable writing to files
- option ``--diff`` to display file diff with the changes done by robotidy
- option ``--check`` to return status depending on if any file was modified by robotidy
- options ``--spacecount`` and ``--lineseparator`` for defining global formatting rules
- ``--startline`` and ``--endline`` arguments for narrowing down what robotidy is supposed to transform in file
- ```--list-transformers``` and ``--describe-transformer`` for displaying information about existing transformers
