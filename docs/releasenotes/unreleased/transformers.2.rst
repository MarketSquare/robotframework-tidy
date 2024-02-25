Split too long VARs (#626)
---------------------------

Too long ``VAR`` is now split with ``SplitTooLong`` transformer. Following code::

    VAR    ${long_variable_name_that_fills_up_half_of_available_space}    long string value that overflows over available space

will be formatted to::

    VAR    ${long_variable_name_that_fills_up_half_of_available_space}
    ...    long string value that overflows over available space
