.. _config-file:

Configuration file
==================

Robotidy supports configuration files in TOML format. Any setting loaded from configuration file will be overwritten
if the same setting is supplied from the command line.

You can load configuration from the file using ``--config`` option::

    robotidy --config path/to/config.toml src

Robotidy will also look by default for ``pyproject.toml`` or ``.robotidy`` file starting from directory of the source(s)
passed on the command line and going up to parent directories. It stops when it finds the file or it finds root of the
project (determined by existence of ``.git`` directory) or root of the file system.

Multiple configuration files are allowed. Robotidy will use a configuration file that is closer to the source file. You can
create several configuration files in a file tree. For example, with the following file structure::

    root/
      pyproject.toml
      source/
        test.robot
        nested/
            pyproject.toml
            test2.robot

The ``test.robot`` file will use ``root/pyproject.toml`` configuration file and ``test2.robot`` will use
``root/source/nested/pyproject.toml``.

.. note::

    You can let Robotidy keep searching for configuration file in the parent directories even if it detects ``.git`` 
    directory on the way. Turn it on using ``--ignore_git_dir`` flag::

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

If you don't provide source paths in the cli, they will be taken from the closest configuration file. In a setup with
multiple configuration files, the source paths from other configurations than the closest will be ignored.

``.robotidy`` file uses the same toml syntax as ``pyproject.toml`` file but allows to skip ``tool.robotidy`` section:

  .. code-block:: toml

     spacecount = 8
     transform = [
        "DiscardEmptySections",
        "NormalizeSeparators"
     ]

Generate configuration file
---------------------------

It is possible to generate configuration files that contains most important options with their default values.
First install ``robotidy`` with ``generate_config`` that contains module for writing TOML files::

    pip install robotidy[generate_config]

You can generate configuration now::

    robotidy --generate-config

.. dropdown:: Example of generated configuration file

   .. code-block:: toml

    [tool.robotidy]
    diff = false
    overwrite = true
    verbose = false
    separator = "space"
    spacecount = 4
    line_length = 120
    lineseparator = "native"
    skip_gitignore = false
    ignore_git_dir = false
    configure = [
        "AddMissingEnd:enabled=True",
        "NormalizeSeparators:enabled=True",
        "DiscardEmptySections:enabled=True",
        "MergeAndOrderSections:enabled=True",
        "RemoveEmptySettings:enabled=True",
        "ReplaceEmptyValues:enabled=True",
        "NormalizeAssignments:enabled=True",
        "GenerateDocumentation:enabled=False",
        "OrderSettings:enabled=True",
        "OrderSettingsSection:enabled=True",
        "NormalizeTags:enabled=True",
        "OrderTags:enabled=False",
        "RenameVariables:enabled=False",
        "IndentNestedKeywords:enabled=False",
        "AlignSettingsSection:enabled=True",
        "AlignVariablesSection:enabled=True",
        "AlignTemplatedTestCases:enabled=False",
        "AlignTestCasesSection:enabled=False",
        "AlignKeywordsSection:enabled=False",
        "NormalizeNewLines:enabled=True",
        "NormalizeSectionHeaderName:enabled=True",
        "NormalizeSettingName:enabled=True",
        "ReplaceRunKeywordIf:enabled=True",
        "SplitTooLongLine:enabled=True",
        "SmartSortKeywords:enabled=False",
        "RenameTestCases:enabled=False",
        "RenameKeywords:enabled=False",
        "ReplaceReturns:enabled=True",
        "ReplaceBreakContinue:enabled=True",
        "InlineIf:enabled=True",
        "Translate:enabled=False",
        "NormalizeComments:enabled=True",
    ]

By default configuration file will be save in the current working directory as ``pyproject.toml`` file. Default
filename can be configured::

    robotidy --generate-config your_name.txt

Configuration is based on default values and configuration from the cli::

    robotidy --transform ReplaceReturns --diff --generate-config

.. dropdown:: Generated file

   .. code-block:: toml

    [tool.robotidy]
    diff = true
    overwrite = true
    verbose = false
    separator = "space"
    spacecount = 4
    line_length = 120
    lineseparator = "native"
    skip_gitignore = false
    ignore_git_dir = false
    configure = [
        "AddMissingEnd:enabled=False",
        "NormalizeSeparators:enabled=False",
        "DiscardEmptySections:enabled=False",
        "MergeAndOrderSections:enabled=False",
        "RemoveEmptySettings:enabled=False",
        "ReplaceEmptyValues:enabled=False",
        "NormalizeAssignments:enabled=False",
        "GenerateDocumentation:enabled=False",
        "OrderSettings:enabled=False",
        "OrderSettingsSection:enabled=False",
        "NormalizeTags:enabled=False",
        "OrderTags:enabled=False",
        "RenameVariables:enabled=False",
        "IndentNestedKeywords:enabled=False",
        "AlignSettingsSection:enabled=False",
        "AlignVariablesSection:enabled=False",
        "AlignTemplatedTestCases:enabled=False",
        "AlignTestCasesSection:enabled=False",
        "AlignKeywordsSection:enabled=False",
        "NormalizeNewLines:enabled=False",
        "NormalizeSectionHeaderName:enabled=False",
        "NormalizeSettingName:enabled=False",
        "ReplaceRunKeywordIf:enabled=False",
        "SplitTooLongLine:enabled=False",
        "SmartSortKeywords:enabled=False",
        "RenameTestCases:enabled=False",
        "RenameKeywords:enabled=False",
        "ReplaceReturns:enabled=True",
        "ReplaceBreakContinue:enabled=False",
        "InlineIf:enabled=False",
        "Translate:enabled=False",
        "NormalizeComments:enabled=False",
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
