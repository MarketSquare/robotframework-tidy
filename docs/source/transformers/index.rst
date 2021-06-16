Transformers
============

Order of transformers
---------------------
By default all transformers run in the same order. Whether called with:

.. code-block:: console

   robotidy src

or

.. code-block:: console

   robotidy --transform ReplaceRunKeywordIf --replace SplitTooLongLine src

or

.. code-block:: console

   robotidy --transform SplitTooLongLine --transform ReplaceRunKeywordIf src

It will transform files according to internal order (in this example ``ReplaceRunKeywordIf`` is before
``SplitTooLongLine``). If you want to transform files using different transformer order you need to run transformers separately:

.. code-block:: console

   robotidy --transform SplitTooLongLine src
   robotidy --transform ReplaceRunKeywordIf src

.. toctree::
    :hidden:
    :maxdepth: 1
    :glob:

    *