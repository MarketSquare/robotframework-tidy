Align comments in AlignKeywordsSection and AlignTestCasesSection (#657)
-----------------------------------------------------------------------

It is now possible to align lines with comments in ``AlignKeywordsSection`` and ``AlignTestCasesSection``
transformers. Enable it by configuring ``align_comments`` parameter to ``True``.

It is especially useful if you want to use comments to name the aligned columns. For example::

    *** Test Cases ***
    Testing Random List
        [Template]    Validate Random List Selection
        # collection          nbr items
        ${SIMPLE LIST}        2             # first test
        ${MIXED LIST}         3             # second test
        ${NESTED LIST}        4             # third test
