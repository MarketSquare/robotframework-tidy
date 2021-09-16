# Change Log

## Unreleased

### Transformers
- New non default transformer `RenameTestCases`. It capitalizes first letter of the test case name, removes trailing dot and can replace provided regex pattern with substitute string [#183](https://github.com/MarketSquare/robotframework-tidy/issues/183)
- Added `AlignTestCases` transformer for aligning templated test cases in column. Because it's in experimental mode it will be non default for now (see docs for information how to run it) [#185](https://github.com/MarketSquare/robotframework-tidy/issues/185)

### Features
- It is now possible to provide source paths in configuration file [#154](https://github.com/MarketSquare/robotframework-tidy/issues/154)
- Non default transformers can be enabled using ``enabled=True`` parameter [#182](https://github.com/MarketSquare/robotframework-tidy/issues/182)
- Semicolon in parameter value can now be escaped with `\:` [#190](https://github.com/MarketSquare/robotframework-tidy/issues/190)
- Default separator can be changed from space to tabular with new ``--separator`` option [#184](https://github.com/MarketSquare/robotframework-tidy/issues/184)

## 1.5.1

### Fixes
- Robotidy will now not crash on directory path [#177](https://github.com/MarketSquare/robotframework-tidy/issues/177)

## 1.5.0

### Features
- Ignore paths from .gitignore and ``--exclude`` option, allow to ignore paths through using ``--extend-exclude`` [#110](https://github.com/MarketSquare/robotframework-tidy/issues/110)
- Add extra indent for arguments in Suite Setup/Teardown, Test Setup/Teardown in AlignSettingsSection [#155](https://github.com/MarketSquare/robotframework-tidy/issues/155)
- OrderSettingsSection will now preserve order of imports. It can be configured to work as before and other settings order can be also preserved [#167](https://github.com/MarketSquare/robotframework-tidy/issues/167)
- When ordering imports with OrderSettingsSection, Remote library will not be grouped with other standard libs [#175](https://github.com/MarketSquare/robotframework-tidy/issues/175)
- Allow to disable selected transformers [#170](https://github.com/MarketSquare/robotframework-tidy/issues/170)

### Fixes
- Do not count documentation length when aligning all columns in settings section  [#156](https://github.com/MarketSquare/robotframework-tidy/issues/156)
- Acknowledge ``--lineseparator`` option [#163](https://github.com/MarketSquare/robotframework-tidy/issues/163)
- Do not print empty line for file without changes with ``--diff`` option [#160](https://github.com/MarketSquare/robotframework-tidy/issues/160)

## 1.4.0

### Features
- Allow to use spaces in pyproject.toml configuration file [#148](https://github.com/MarketSquare/robotframework-tidy/issues/148)

### Fixes
- Invalid option names in pyproject.toml file will now stop Robotidy (with optional hint message) [#150](https://github.com/MarketSquare/robotframework-tidy/issues/150)

## Other
- Fixed spelling issues in source code and docs [#146](https://github.com/MarketSquare/robotframework-tidy/issues/146)

## 1.3.0

### Transformers
- ``AssignmentNormalizer`` was renamed to ``NormalizeAssignment`` for consistent naming with other transformers [#115](https://github.com/MarketSquare/robotframework-tidy/issues/115)
- It is now possible to select what sections are normalized in ``NormalizeSeparators`` transformer with ``sections`` param [#116](https://github.com/MarketSquare/robotframework-tidy/issues/116)
- ``OrderSettings`` now puts settings before comments and empty lines at the end of keyword/test case body [#118](https://github.com/MarketSquare/robotframework-tidy/issues/118), [#125](https://github.com/MarketSquare/robotframework-tidy/issues/125)

### Features
- New option ``--output`` option for saving transformed file to provided path instead of overwriting source file [#108](https://github.com/MarketSquare/robotframework-tidy/issues/108)
- ``--desc`` now accepts ``all`` for printing out description of all transformers [#105](https://github.com/MarketSquare/robotframework-tidy/issues/105)
- Robotidy will now suggest similar names for invalid transformer names used with ``--transform`` or ``--desc`` options  [#107](https://github.com/MarketSquare/robotframework-tidy/issues/107)
- ``--list`` now prints transformers in alphabetical order [#141](https://github.com/MarketSquare/robotframework-tidy/issues/141)

### Fixes
- Renamed short version of ``--lineseparator`` to ``-ls`` to avoid collision with ``--list\-l``
- Description for disabled transformers can be now displayed & disabled transformers are in ``--list`` output [#114](https://github.com/MarketSquare/robotframework-tidy/issues/114)
- Robotidy should now correctly load configuration files from path when using ``--config`` [#138](https://github.com/MarketSquare/robotframework-tidy/issues/138)
- ReplaceRunKeywordIf will now set variable values to `None` if there is no ELSE branch [#140](https://github.com/MarketSquare/robotframework-tidy/issues/140)
- Transformers should always use the same order. If you need to use custom order, provide --force-order flag [#142](https://github.com/MarketSquare/robotframework-tidy/issues/142)

### Other
- Removed ``'--describe-transformer`` and ``--list-transformers`` aliases for ``--list`` and ``--desc``
- Added ``-h`` alias for ``--help`` command
- Warn user instead of doing nothing when invoking robotidy without any arguments [#106](https://github.com/MarketSquare/robotframework-tidy/issues/106)

## 1.2.0

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
- New OrderSettingsSection transformer for ordering settings, imports inside ``*** Settings ****`` section [#100](https://github.com/MarketSquare/robotframework-tidy/issues/100)

### Features
- New option ``--configure`` or ``-c`` for configuring transformer parameters. It works the same way configuring through ``--transform`` works. The benefit of using ``--configure`` is that you can configure selected transformers and still run all transformers [#96](https://github.com/MarketSquare/robotframework-tidy/issues/96)
- Transformers can now be disabled by default if you add ``ENABLED = False`` class attribute to your class. Those transformers will be only run when selected explicitly with ``--transform`` option [#10](https://github.com/MarketSquare/robotframework-tidy/issues/10)
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
- SplitTooLongLine - keywords with too long lines are split
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
