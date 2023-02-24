.. _configuration:

Configuration
=============

.. toctree::
   :maxdepth: 1
   :hidden:

   config_file
   configuring_transformers
   skip_formatting

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

Note that both ``exclude`` and ``extend-exclude`` options accept regex patterns. Following configuration is not
array with single `Tests/` path but regex pattern that excludes paths containing any of the character from the `Tests/`
set::

    [tool.robotidy]
    exclude = ['Tests/']

To exclude files under `Tests` directory you need to use pattern `Tests/*`::

    [tool.robotidy]
    exclude = 'Tests/*'

To parse files listed in ``.gitignore`` use ``--skip-gitignore`` flag::

    robotidy --skip-gitignore .

.. rubric:: Target Version

Robotidy can automatically disable transformers that are not supported in target version of Robot Framework.
Typical usage is when your environment has Robot Framework >5.0 installed but your source code supports only previous
Robot Framework version::

    robotidy --target-version rf4 .

It will disable all transformers that require Robot Framework greater than <target-version> to run (even if you have Robot Framework greater than <target-version> installed).

.. _language_support:
.. rubric:: Language support

Robot Framework 6.0 added support for Robot settings and headers translation.
Robotidy recognizes language markers in the file but needs to be configured if you have translated file without language marker.
You can supply language code or name in the configuration using ``--language / --lang`` option::

    robotidy --lang fi

Support multiple languages by providing language code/name in comma separated list::

    robotidy --lang fi,pt

``pyproject.toml`` file accepts ``language`` array::

    [tool.robotidy]
    language = [
        "pt",
        "fi"
    ]

Language header in the file is supported by default::

    language: pl

    *** Zmienne ***
    ${VAR}   1


Custom language file is currently not supported.

.. _disablers:

.. rubric:: Disablers

You can disable formatting in Robot Framework statement or in span of lines using ``# robotidy: off`` marker.

To skip the formatting for one statement:

.. code-block:: robotframework

    Keyword That Is Longer Than Allowed Line Length  ${arg}  # robotidy: off

To skip multiple lines:

.. code-block:: robotframework

    *** Test Cases ***
    Test that will be formatted
        Step

    # robotidy: off
    Test that will not be formatted
        Step

    # robotidy: on
    Another test that will be formatted
        Step


``# robotidy: on`` marker is used to enable the formatting again - but is not required. ``# robotidy: off`` will disable
the formatting to the end of the current block:

.. code-block:: robotframework

    *** Keywords ***
    Keyword
        Keyword That Is Formatted
        IF    $condition
            Formatted
        ELSE
            Formatted
            # robotidy: off
            Not Formatted
            WHILE    $condition
                Not Formatted
            END
        END
        Formatted

It's possible to disable the formatting in whole file by putting ``# robotidy: off`` on first line:

.. code-block:: robotframework

    # robotidy: off
    *** Settings ***
    Library    Collections

You can also disable the formatting in the whole section if you put ``# robotidy: off`` in the section header:

.. code-block:: robotframework

    *** Test Cases ***
    Formatted
        Step

    *** Keywords ***  # robotidy: off
    Not Formatted
        Step
