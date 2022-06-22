.. _AlignTestCasesSection:

AlignTestCasesSection
================================
Short description.


.. |TRANSFORMERNAME| replace:: _AlignTestCasesSection
.. include:: enabled_hint.txt


Long description with code examples.

Split too long lines
---------------------
``AlignKeywordsSection`` will split the lines if the lines after alignment would exceed the limits set in
the :ref:`SplitTooLongLine` transformer.

.. note::
    Currently only ``--configure SplitTooLongLine:split_on_every_arg=True`` mode is supported.

Using this configuration (``SplitTooLongLine`` is enabled by default)::

    robotidy -c AlignTestCasesSection:enabled=True:widths=14,24 --line-length 80 src

Will result in the following transformation:

.. tabs::

    .. code-tab:: robotframework Before

        *** Test Cases ***
        Test case
            # fits now but it will not fit after the alignment
            Keyword    argument1    argument2    argument3    argument4

            # does not fit before alignment
            Longer Keyword Name That Could Happen    argument value with sentence that goes over

            # fits, will not be split
            Keyword    argument

    .. code-tab:: robotframework After

        *** Test Cases ***
        Test case
            # fits now but it will not fit after the alignment
            Keyword
            ...           argument1
            ...           argument2
            ...           argument3
            ...           argument4

            # does not fit before alignment
            Longer Keyword Name That Could Happen
            ...           argument value with sentence that goes over

            # fits, will be aligned but not split
            Keyword       argument


Skip formatting
----------------
It is possible to use the following arguments to skip formatting of the code:

- :ref:`skip documentation`
- :ref:`skip return values`
- :ref:`skip keyword call`
- :ref:`skip keyword call pattern`
