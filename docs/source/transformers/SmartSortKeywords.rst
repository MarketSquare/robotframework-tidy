.. _SmartSortKeywords:

SmartSortKeywords
================================

Sort keywords in ``*** Keywords ***`` section.

.. |TRANSFORMERNAME| replace:: SmartSortKeywords
.. include:: disabled_hint.txt

By default sorting is case insensitive, but keywords with leading underscore go to the bottom. Other underscores are
treated as spaces.
Empty lines (or lack of them) between keywords are preserved.

.. tabs::

    .. code-tab:: robotframework Before

        *** Keywords ***
        _my secrete keyword
            Kw2

        My Keyword
            Kw1


        my_another_cool_keyword
        my another keyword
            Kw3

    .. code-tab:: robotframework After

        *** Keywords ***
        my_another_cool_keyword

        my another keyword
            Kw3


        My Keyword
            Kw1
        _my secrete keyword
            Kw2

Default behaviour could be changed using following parameters: ``case_insensitive``, ``ignore_leading_underscore``
and ``ignore_other_underscore``.
