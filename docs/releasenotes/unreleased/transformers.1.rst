Ignore variable separator in RenameVariables (#682)
---------------------------------------------------

Added new ``ignore`` mode to ``variable_separator`` parameter. It allows to ignore variable separators when
formatting with ``RenameVariables``::

    *** Variables ***
    # following variables will have variable separators (spaces and underscores) untouched
    ${variable with space}  value
    ${mixed_variable and_space}  value
