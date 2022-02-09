.. _OrderTags:

OrderTags
================================
Order tags in case-insensitive way in ascending order.

.. |TRANSFORMERNAME| replace:: OrderTags
.. include:: disabled_hint.txt

This relates to tags in Test Cases, Keywords, Force Tags and Default Tags.

.. tabs::

    .. code-tab:: robotframework Before

        *** Settings ***
        Documentation       OrderTags acceptance tests
        Force Tags      forced_tag_1    forced_tag_aa     forced_tag_2    forced_tag_Ab    forced_tag_Bb    forced_tag_ba
        Default Tags    default_tag_1    default_tag_aa    default_tag_2    default_tag_Ab    default_tag_Bb    default_tag_ba

        *** Test Cases ***
        Tags Upper Lower
            [Tags]    ba    Ab    Bb    Ca    Cb    aa
            My Keyword

        *** Keywords ***
        My Keyword
            [Tags]    ba    Ab    Bb    Ca    Cb    aa
            No Operation

    .. code-tab:: robotframework After

        *** Settings ***
        Documentation       OrderTags acceptance tests
        Force Tags          forced_tag_1    forced_tag_2    forced_tag_aa    forced_tag_Ab    forced_tag_ba    forced_tag_Bb
        Default Tags        default_tag_1    default_tag_2    default_tag_aa    default_tag_Ab    default_tag_ba    default_tag_Bb

        *** Test Cases ***
        Tags Upper Lower
            [Tags]    aa    Ab    ba    Bb    Ca    Cb
            My Keyword

        *** Keywords ***
        My Keyword
            [Tags]    aa    Ab    ba    Bb    Ca    Cb
            No Operation

Using the same example with ``reverse=True`` param we will get tags in descending order::

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

Force Tags and Default Tags ordering can be disabled like this::

    robotidy --transform OrderTags:default_tags=False:force_tags=False src

.. tabs::

    .. code-tab:: robotframework Before

        *** Settings ***
        Documentation       OrderTags acceptance tests
        Force Tags      forced_tag_1    forced_tag_aa     forced_tag_2    forced_tag_Ab    forced_tag_Bb    forced_tag_ba
        Default Tags    default_tag_1    default_tag_aa    default_tag_2    default_tag_Ab    default_tag_Bb    default_tag_ba

        *** Test Cases ***
        Tags Upper Lower
            [Tags]    ba    Ab    Bb    Ca    Cb    aa
            My Keyword

    .. code-tab:: robotframework After

        *** Settings ***
        Documentation       OrderTags acceptance tests
        Force Tags      forced_tag_1    forced_tag_aa     forced_tag_2    forced_tag_Ab    forced_tag_Bb    forced_tag_ba
        Default Tags    default_tag_1    default_tag_aa    default_tag_2    default_tag_Ab    default_tag_Bb    default_tag_ba

        *** Test Cases ***
        Tags Upper Lower
            [Tags]    aa    Ab    ba    Bb    Ca    Cb
            My Keyword
