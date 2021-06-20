.. _config-file:

Configuration file
==================

Robotidy supports configuration files in TOML format. Any setting loaded from configuration file will be overwritten
if the same setting is supplied from command line.

You can load configuration from the file using ``--config`` option::

    robotidy --config path/to/config.toml src

Robotidy will also  look by default for ``pyproject.toml`` file starting from directory of source(s)
passed on the command line and going up to parent directories. It stops when it finds the file or it finds root of the
project (determined by existence of ``.git`` directory) or root of the file system.

``pyproject.toml`` contain separate sections for different tools. Robotidy uses ``tool.robotidy`` section. The option
names are the same as name of the options used on the command line.

Flag-like options like ``--diff``, ``--overwrite/no-overwrite``, ``--check`` require passing true/false boolean value.
``--transform`` and ``--configure`` require defining list of strings.

See example:
  .. code-block:: toml

    [tool.robotidy]
    overwrite = false
    diff = true
    startline = 10
    endline = 20
    transform = [
       "DiscardEmptySections:allow_only_comments=True",
       "SplitTooLongLine"
    ]
    configure = [
        "SplitTooLongLine:split_on_every_arg=False"
    ]