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

.. rubric:: Disablers

It's possible to skip formatting using ``# robotidy: off`` comment. It supports both inline and block disabling.

To skip one statement::

    Keyword Call That Should Not Be Formatted  ${arg}  # robotidy: off


To skip multiple lines use ``# robotidy: off`` at beginning of line. You can enable formatting again with
``robotidy: on``. If ``# robotidy: off`` is used inside block (Keyword, Test, IF, FOR, WHOLE etc.) only content of the block will be skipped::

    *** Test Cases ***
    Test that will be formatted
        Step

    # robotidy: off
    Test that will not be formatted
        Step

    # robotidy: on

    Mixed blocks test
        Formatted
        IF   $condition
            Formatted
            # robotidy: off
            Not formatted
        END
        Formatted

Transformers can be also disabled by adding ``robotidy: off`` in section header::

    *** Settings ***  # robotidy: off
    # it will not be formatted
    Force Tags    tag
    Library    Collections

    *** Variables ***
    # it will be formatted
    ${VAR}    4
