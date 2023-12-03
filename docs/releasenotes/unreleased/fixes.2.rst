Robot Framework 7.0 backward incompatible changes: ForceTags deprecation (#584)
--------------------------------------------------------------------------------

Our tag transformers imports ``Force Tags`` class from ``robot`` module. It was deprecated in Robot Framework 7
and caused ImportError when using Robotidy. It should be now fixed.
