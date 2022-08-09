.. _transformers:

Transformers
============

.. toctree::
    :hidden:
    :maxdepth: 1
    :glob:

    *

.. rubric:: List of transformers

To see list of all transformers currently implemented in `robotidy` run::

    robotidy --list

Transformers are sorted in the order they are run by default.
To see description of the transformer run::

    robotidy --desc TRANSFORMER_NAME

See :ref:`configuring-transformers` to learn how transformers can be configured (including disabling and enabling transformers).

.. rubric:: Order of transformers

By default all transformers run in the same order. Whether called with::

   robotidy src

or::

   robotidy --transform ReplaceRunKeywordIf --transform SplitTooLongLine src

or::

   robotidy --transform SplitTooLongLine --transform ReplaceRunKeywordIf src

It will transform files according to internal order (in this example ``ReplaceRunKeywordIf`` is before
``SplitTooLongLine``). To see order of the transformers run ``robotidy --list``.

If you want to transform files using different transformer order you need to run transformers separately::

   robotidy --transform SplitTooLongLine src
   robotidy --transform ReplaceRunKeywordIf src

You can also add ``--force-order`` flag to use order provided in cli::

   robotidy --force-order --transform SplitTooLongLine --transform ReplaceRunKeywordIf src

External transformers are used last. If you want to change this behaviour (for example run your custom transformer
before default ones) you need to use ``--force-order`` flag.

.. rubric:: Pipe handling

Not all transformers can handle pipe syntax. If you encounter any issues with pipe separators, run
``NormalizeSeparators`` transformer to replace pipes with spaces.
