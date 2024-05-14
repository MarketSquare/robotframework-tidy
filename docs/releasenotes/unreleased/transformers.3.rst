[Timeout] and [Setup] order for keywords in OrderSettings (#690)
-----------------------------------------------------------------

Default order of keyword settings in ``OrderSettings`` transformer was modified. Robot Framework 7.0 added ``[Setup]``
to keywords (which wasn't supported by Robotidy until now). ``[Timeout]`` order was also changed.

Old default order was ``documentation,tags,timeout,arguments`` and new order is
``documentation,tags,arguments,timeout,setup``.

``[Timeout]`` order was changed to follow Robot Framework Style Guide recommendation.

If you are using ``OrderSettings`` with custom order, this change requires to add ``setup`` to your order.

Note that if you're using ``[Setup]`` with keywords in your code (supported in RF from 7.0) but run Robotidy with older
version (pre 7.0) it will order ``[Setup]`` like a keyword call - essentially ignoring its order.
