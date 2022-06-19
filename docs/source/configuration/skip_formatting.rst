.. _skip_formatting:

Skip formatting
================
.. rubric:: Skip formatting

It is possible to skip formatting on code that matches given criteria.
Following transformers provide support for skip option:

- :ref:`AlignKeywordsSection`
- :ref:`AlignTestCasesSection`
- :ref:`NormalizeSeparators`

To see what types are possible to skip see ``Skip formatting`` sections in each transformer documentation.

.. _skip documentation:

Skip documentation
-------------------
Flag that disables formatting the documentation. Example usage::

    robotidy -c NormalizeSeparators:skip_documentation=True src

.. _skip return_values:

Skip return values
-------------------
Flag that disables formatting the return values (assignments). Example usage::

    robotidy -c AlignKeywordsSection:skip_return_values=True src

.. _skip keyword call:

Skip keyword call
------------------
Comma separated list of keyword call names that should not be formatted. Names will be
normalized before search (spaces and underscores removed, lowercase).

With this configuration::

    robotidy -c AlignTestCasesSection:skip_keyword_call=ExecuteJavascript,catenate

All instances of ``Execute Javascript`` and ``Catenate`` keywords will not be formatted.

.. _skip keyword call pattern:

Skip keyword call pattern
-------------------------
Comma separated list of keyword call name patterns that should not be formatted. The keyword names are not normalized.
If you're using different case for the same keyword ("Keyword" and "keyword") or using both spaces and underscores it is
recommended to use proper regex flags to match it properly.

With this configuration::

    robotidy -c AlignKeywordsSection:skip_keyword_call_pattern=^First,(i?)contains\s?words src

All instances of keywords that starts with "First" or contains "contains words" (case insensitive, space optional) will
not be formatted.

Note that list is comma separated - it is currently not possible to provide regex with ``,``.
