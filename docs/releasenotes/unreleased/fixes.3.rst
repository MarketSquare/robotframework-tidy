[Return] setting deprecated
----------------------------

``[Return]`` setting is now visibly deprecated. The model also changed and several Robotidy transformers stopped
transforming ``[Return]``. We should now be able to handle both ``[Return]`` and ``RETURN``.

Note that Robotidy replaces ``[Return]`` with ``RETURN`` since Robot Framework 5.0 thanks to ``ReplaceReturns``
transformer. If you're not using default configuration you should remember to include it.
