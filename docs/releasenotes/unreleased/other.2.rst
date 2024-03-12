Disable selected transformers (#653)
------------------------------------

Robotidy disablers now supports not only disabling all transformers but selected ones::

    *** Test Cases ***
    Test with mixed variables
        Keyword call  ${global}  # robotidy: off = RenameVariables

