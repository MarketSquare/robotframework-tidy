.. _NormalizeTags:

NormalizeTags
================================
Normalize tag names by normalizing case and removing duplicates.

.. |TRANSFORMERNAME| replace:: NormalizeTags
.. include:: enabled_hint.txt

Supported cases: lowercase (default), uppercase, title case.
You can configure case using ``case`` parameter::

    robotidy --transform NormalizeTags:case=uppercase


You can remove duplicates without normalizing case by setting ``normalize_case`` parameter to False::

    robotidy --transform NormalizeTags:normalize_case=False

