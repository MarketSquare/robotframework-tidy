Robot Framework 7.0 backward incompatible changes: VariableIterator refactor
----------------------------------------------------------------------------

Robotidy variables handling relied upon ``VariableIterator`` class imported from Robot Framework package.
It caused ImportError which should be now fixed.
