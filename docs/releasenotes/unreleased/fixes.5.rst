load_transformers not supported in the configuration file (#576)
-----------------------------------------------------------------

``--load-transformers`` (and ``load_transformers`` in the toml configuration file) was renamed before to
``--custom-transformers`` (``custom_transformers``). Old name remained due to backward compatibility. However it was
not handled properly and Robotidy cli only supported ``--load-transformers`` while configuration file only
``custom_transformers``. Now the approach should be unified and both cli and configuration file should support old
and new option name.
