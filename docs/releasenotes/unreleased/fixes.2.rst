RenameVariables adding _ to variables with equal sign in Variables section (#692)
---------------------------------------------------------------------------------

Following code::

    *** Variables ***
    ${random_seed} =    ${None}

was formatted incorrectly - ``_`` was added before ``=``.
