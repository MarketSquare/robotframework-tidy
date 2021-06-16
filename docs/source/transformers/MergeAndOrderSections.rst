.. _MergeAndOrderSections:

MergeAndOrderSections
==================================

Merge duplicated sections and order them.

Default order is: Comments > Settings > Variables > Test Cases > Keywords.

You can change sorting order by configuring ``order`` parameter with comma separated list of section names (without
spaces)::

    robotidy --transform MergeAndOrderSections:order=settings,keywords,variables,testcases,comments

Because merging and changing the order of sections can shuffle your empty lines it's greatly advised to always
run ``NormalizeNewLines`` transformer after this one.

If both ``*** Test Cases ***`` and ``*** Tasks ***`` are defined in one file they will be merged into one (header
name will be taken from first encountered section).

Any data before first section is treated as comment in Robot Framework. This transformer add ``*** Comments ***``
section for such lines::

    i am comment
    # robocop: disable
    *** Settings ***

To::

    *** Comments ***
    i am comment
    # robocop: disable
    *** Settings ***

You can disable this behaviour by setting ``create_comment_section`` to False.