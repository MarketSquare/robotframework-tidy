Ignore comments in IndentNestedKeywords transformer (#702)
----------------------------------------------------------

``IndentNestedKeywords`` moves comments before transformation. This is required in order to properly format different
types of the source code (especially when expanding single line to multiple lines). However as side affect
``IndentNestedKeywords`` moved the comments even if the code didn't require formatting::

    *** Test Cases ***
    Keyword with commented out single line
        Run Keywords
        ...    No Operation
        # ...    No Operation
        ...    No Operation

In such case the code is already formatted and does not require moving the comments. After this release such
comments will be left alone in a case where the code is already formatted.
