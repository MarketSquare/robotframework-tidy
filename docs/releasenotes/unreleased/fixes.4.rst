Minimal width of the column in AlignVariablesSection and AlignSettingsSection (#558)
------------------------------------------------------------------------------------

``AlignVariablesSection`` and ``AlignSettingsSection`` transformers use ``min_width`` parameter. Originally it didn't
work as ``min_width`` but more as ``fixed_width`` parameter. That's why we are now introducing new parameter
(``fixed_width``) that will work same as previous ``min_width``. ``min_width`` is now fixed and is used to configure
minimal width of the aligned column.

If you are relying on ``min_width`` to set fixed width of the column, rename it to ``fixed_width`` in your
configuration.
