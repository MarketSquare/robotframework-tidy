.. _OrderTags:

OrderTags
================================

OrderTags is not included in default transformers, that's why you need to call it with ``--transform`` explicitly::

    robotidy --transform OrderTags src

Or configure `enable` parameter::

    robotidy --configure OrderTags:enabled=True

By default tags are ordered in case-insensitive way in ascending order.

.. tabs::

    .. code-tab:: robotframework Before

        *** Test Cases ***
        No tags
            No Operation

        Tags Upper Lower
            [Tags]    ba    Ab    Bb    Ca    Cb    aa
            My Keyword

        One Tag
            [Tags]    one_tag
            One Tag Keyword

        *** Keywords ***
        My Keyword
            [Tags]    ba    Ab    Bb    Ca    Cb    aa
            No Operation

        One Tag Keyword
            [Tags]    one_tag
            No Operation

    .. code-tab:: robotframework After

        *** Test Cases ***
        No tags
            No Operation

        Tags Upper Lower
            [Tags]    aa    Ab    ba    Bb    Ca    Cb
            My Keyword

        One Tag
            [Tags]    one_tag
            One Tag Keyword

        *** Keywords ***
        My Keyword
            [Tags]    aa    Ab    ba    Bb    Ca    Cb
            No Operation

        One Tag Keyword
            [Tags]    one_tag
            No Operation

Using the same example with reverse=True param we will get tags in descending order::

    robotidy --transform OrderTags:reverse=True src


.. tabs::

    .. code-tab:: robotframework Before

        *** Test Cases ***
        Tags Upper Lower
            [Tags]    ba    Ab    Bb    Ca    Cb    aa
            My Keyword

    .. code-tab:: robotframework After

        *** Test Cases ***
        Tags Upper Lower
            [Tags]    Cb    Ca    Bb    ba    Ab    aa
            My Keyword


Tags can be also order in case-sensitive way::

    robotidy --transform OrderTags:case_sensitive=True:reverse=False src

.. tabs::

    .. code-tab:: robotframework Before

        *** Test Cases ***
        Tags Upper Lower
            [Tags]    ba    Ab    Bb    Ca    Cb    aa
            My Keyword

    .. code-tab:: robotframework After

        *** Test Cases ***
        Tags Upper Lower
            [Tags]    Ab    Bb    Ca    Cb    aa    ba
            My Keyword