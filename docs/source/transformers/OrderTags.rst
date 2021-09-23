.. _OrderTags:

OrderTags
================================

OrderTags is not included in default transformers, that's why you need to call it with ``--transform`` explicitly::

    robotidy --transform OrderTags src

Or configure `enable` parameter::

    robotidy --configure OrderTags:enabled=True

