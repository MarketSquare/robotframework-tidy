Transformers
============

.. toctree::
    :hidden:
    :maxdepth: 1
    :glob:

    *

Order of transformers
---------------------
By default all transformers run in the same order. Whether called with::

   robotidy src

or::

   robotidy --transform ReplaceRunKeywordIf --replace SplitTooLongLine src

or::

   robotidy --transform SplitTooLongLine --transform ReplaceRunKeywordIf src

It will transform files according to internal order (in this example ``ReplaceRunKeywordIf`` is before
``SplitTooLongLine``). If you want to transform files using different transformer order you need to run transformers separately::

   robotidy --transform SplitTooLongLine src
   robotidy --transform ReplaceRunKeywordIf src
