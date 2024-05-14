Ignoring additional variables in RenameVariables (#692)
-------------------------------------------------------

``RenameVariables`` will now ignore and do not transform following variables:

- ``${None}``
- ``${True}``
- ``${False}``
- numerical values such as ``${0x1A}`` or ``${0b01010}``
