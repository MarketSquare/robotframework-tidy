ReplaceWithVAR does detect empty separator as default separator (space) (#651)
------------------------------------------------------------------------------

Catenate with empty separator was incorrectly recognized as ${SPACE}. Following code::

    Catenate     SEPARATOR=    value

will now be transformed to::

    VAR    value    separator=${EMPTY}
