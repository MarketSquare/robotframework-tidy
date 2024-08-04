Use variable_separator when converting variable from camelCase in RenameVariables (#705)
----------------------------------------------------------------------------------------

Previously ``variable_separator`` configuration was not respected when converting variable names from camelCase to
snake_case. In result variable names were converted with spaces as the separator::

    # from
    ${camelCase}
    # to
    ${camel case}

Now the setting will be take into account.
