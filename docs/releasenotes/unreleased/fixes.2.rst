``NormalizeSeparators`` with ``flatten_lines=True`` not handling Inline IFs (#548)
-----------------------------------------------------------------------------------

Robotidy should now correctly handles Inline IFs in ``NormalizeSeparators`` transformer with ``flatten_lines=True``.
Previously, spacing before `ELSE` and `ELSE IF` branches was set to 0::

    IF    ${value}>0    Do Thing    ELSE    Do Other Thing

it was transformed to::

    IF    ${value}>0    Do ThingELSE    Do Other Thing

Additionally, number of spaces before `ELSE` and `ELSE IF` in Inline IFs should now be calculated correctly
(based on the separator length and not indentation).
