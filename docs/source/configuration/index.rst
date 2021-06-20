.. _configuration:

Configuration
=============

.. toctree::
   :maxdepth: 1
   :hidden:

   config_file
   configuring_transformers

Behaviour of robotidy can be changed through global options or by configuring specific transformer.
To read more about configuring transformer go to :ref:`configuring-transformers`. To see how to configure robotidy
using configuration files see :ref:`config-file`.

.. rubric:: Command line options

- ``--transform`` / ``-t``
  Used to select what transformers will be run (overwrites default transformers list)
- ``--configure`` / ``-c``
  Used to configure transformers. See more :ref:`configuring-transformers`
- ``--list`` / ``-l``
  List available transformers.
- ``--desc`` / ``-d`` TRANSFORMER_NAME
  Show documentation for selected transformer. Pass ``all`` as transformer name to show documentation for all transformers.
- ``--output`` / ``-o``
  Path to output file where source will be saved (by default the source file is overwritten).
- ``--config`` FILE
  Path to configuration file.
- ``--overwrite/--no-overwrite`` flag
  Flag to determine if changes should be written back to file (default: --overwrite).
- ``--diff`` flag
  If this flag is set Robotidy will output diff view of each processed file.
- ``--check`` flag
  Don't overwrite files and just return status.
- ``--spacecount`` / ``-s``
  The number of spaces between cells (used by some of the transformers, for example ``NormalizeSeparators``).
- ``--startline`` / ``-sl and ``--endline`` / ``-el``
  Used by some of the transformers to narrow down part of the file that is transformed. Line numbers start from 1.
- ``--verbose`` / ``-v``
  More verbose output.
- ``--version``
  Print Robotidy version.
- ``help``
  Prints robotidy help.