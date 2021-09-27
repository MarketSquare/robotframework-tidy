.. _NormalizeTags:

NormalizeTags
================================

NormalizeTags is not included in default transformers, that's why you need to call it with ``--transform`` explicitly::

    robotidy --transform NormalizeTags src

Or configure `enable` parameter::

    robotidy --configure NormalizeTags:enabled=True


Supported cases: lowercase (default), uppercase, titlecase.
You can configure case using `case` parameter::

    robotidy --transform NormalizeTags:case=uppercase


You can remove duplicates without normalizing case by setting normalize_case parameter to False::

    robotidy --transform NormalizeTags:normalize_case=False

