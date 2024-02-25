Variables in tags are no longer renamed with NormalizeTags (#638)
-----------------------------------------------------------------

``NormalizeTags`` transformer incorrectly affected variables used in tags::

  *** Settings ***
  Test Tags    tag with ${var}

Such variables will be now ignored.
