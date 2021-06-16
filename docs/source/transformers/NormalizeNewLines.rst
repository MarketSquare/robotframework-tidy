.. _NormalizeNewLines:

NormalizeNewLines
================================

Normalize new lines.

Ensure that there is exactly:
* ``section_lines = 1`` empty lines between sections,
* ``test_case_lines = 1`` empty lines between test cases,
* ``keyword_lines = test_case_lines`` empty lines between keywords.

Removes empty lines after section (and before any data) and appends 1 empty line at the end of file.

Consecutive empty lines inside settings, variables, keywords and test cases are also removed
(configurable via ``consecutive_lines = 1``). If set to 0 all empty lines will be removed.

If the suite contains Test Template tests will not be separated by empty lines unless ``separate_templated_tests``
is set to True.
