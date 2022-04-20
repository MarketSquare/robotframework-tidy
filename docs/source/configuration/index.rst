.. _configuration:

Configuration
=============

.. toctree::
   :maxdepth: 1
   :hidden:

   config_file
   configuring_transformers

Behaviour of *robotidy* can be changed through global options or by configuring specific transformer.
To read more about configuring transformer go to :ref:`configuring-transformers`. To see how to configure robotidy
using configuration files see :ref:`config-file`.

.. rubric:: Command line options

To list *robotidy* command line options run::

    robotidy --help

.. rubric:: Ignored paths

Robotidy reads and ignores paths from ``.gitignore`` and ``--exclude``. You can overwrite default excludes by using
``--exclude`` option. If you want to exclude additional paths on top of those from ``--exclude`` and ``.gitignore`` use
``--extend-exclude`` with pattern::

    robotidy --extend-exclude skip_me.robot|some_dir/* .

.. rubric:: Target Version

Robotidy can automatically disable transformers that are not supported in target version of Robot Framework.
Typical usage is when your environment have Robot Framework >5.0 installed but your source code supports only previous
Robot Framework version::

    robotidy --target-version -rf4 .

It will disable all transformers that require Robot Framework >4.0 to run (even if you have Robot Framework >4.0 installed).
