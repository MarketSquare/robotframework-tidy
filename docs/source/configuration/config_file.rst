.. _config-file:

Configuration file
==================

Robotidy supports configuration files in TOML format. Any setting loaded from configuration file will be overwritten
if the same setting is supplied from the command line.

You can load configuration from the file using ``--config`` option::

    robotidy --config path/to/config.toml src

Robotidy will also look by default for ``pyproject.toml`` file starting from directory of the source(s)
passed on the command line and going up to parent directories. It stops when it finds the file or it finds root of the
project (determined by existence of ``.git`` directory) or root of the file system.

.. note::

    You can keep searching for configuration file in parent directories even if there is ``.git`` directory with
    ``--ignore_git_dir`` flag::

        > robotidy --ignore_git_dir src

``pyproject.toml`` contain separate sections for different tools. Robotidy uses ``tool.robotidy`` section. The option
names are the same as name of the options used on the command line.

Flag-like options like ``--diff``, ``--overwrite/no-overwrite``, ``--check`` require passing true/false boolean value.
``--transform`` and ``--configure`` require defining list of strings.

See example:

  .. code-block:: toml

    [tool.robotidy]
    overwrite = false
    diff = true
    spacecount = 2
    continuation-indent = 4
    startline = 10
    endline = 20
    transform = [
       "DiscardEmptySections:allow_only_comments=True",
       "SplitTooLongLine"
    ]
    configure = [
        "SplitTooLongLine:split_on_every_arg=False"
    ]

Source paths can be configured via ``src`` parameter. If the path does not exist it will be silently ignored:

  .. code-block:: toml

    [tool.robotidy]
    src = [
        "test.robot",
        "directory"
    ]

Multiline configuration
------------------------
Transformers with multiple parameters can be configured in one line (each param delimited by ``:``) or in separate lines:

  .. code-block:: toml

    [tool.robotidy]
    configure = [
        "OrderSettings:keyword_before=documentation,tags,timeout,arguments:keyword_after=return",
        "OrderSettingsSection:group_order=documentation,imports,settings,tags",
        "OrderSettingsSection:imports_order=library,resource,variables"
    ]

Multiline configuration is only possible with ``configure`` option. ``transform`` option overrides previous
configuration. In the following configuration only last ``OrderSettings`` configuration will be used:

  .. code-block:: toml

    [tool.robotidy]

    transform = [
        "OrderSettings:test_before=tags, setup,  teardown, documentation:test_after=", # will be ignored
        "OrderSettings:keyword_before=tags, teardown, documentation, arguments:keyword_after="
    ]

If you want to use ``transform`` and provide configuration for multiple parameters you can either chain
parameters with ``:`` or use ``configure``:

  .. code-block:: toml

    [tool.robotidy]

    transform = [
        "OrderSettings"
    ]
    configure = [
        "OrderSettings:test_before=tags, setup,  teardown, documentation:test_after=",
        "OrderSettings:keyword_before=tags, teardown, documentation, arguments:keyword_after="
    ]

Ignored whitespace
-------------------
Transformer configuration can contain spaces for better readability:

  .. code-block:: toml

    [tool.robotidy]
    configure = [
        "OrderSettingsSection: group_order = documentation,imports,settings,tags",
        "OrderSettingsSection: imports_order = library, resource, variables"
    ]
