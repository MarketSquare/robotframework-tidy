.. _DiscardEmptySections:

DiscardEmptySections
================================

Remove empty sections.
Sections are considered empty if there is no data or there are only comments inside (with the exception
for ``*** Comments ***`` section).
You can leave sections with only comments by setting ``allow_only_comments`` parameter to True::

    *** Variables ***
    # this section would be removed if not for ``alow_only_comments`` parameter

Supports global formatting params: ``--startline`` and ``--endline``.