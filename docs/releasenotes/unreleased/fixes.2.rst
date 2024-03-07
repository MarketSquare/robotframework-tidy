ReplaceWithVAR Create Dictionary does not support passing key and values separately (#652)
------------------------------------------------------------------------------------------

Fixed missing support for ``Create Dictionary`` keyword with key and values in a list. Following code::

    ${dict}    Create Dictionary    key    value
    ${dict}    Create Dictionary    key=value  # already handled

should now be transformed to::

    VAR    &{dict}    key=value
    VAR    &{dict}    key=value  # already handled
