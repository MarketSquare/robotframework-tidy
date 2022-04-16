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

You can disable formatting in Robot Framework statement or in span of lines using ``# robocop: off`` marker.

To skip formatting for one statement:

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


``# robotidy: on`` marker is used to enabled formatting again - but is not necessary. ``# robotidy: off`` will disable
formatting to the end of the current block:

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

It's possible to disable formatting in whole file by putting ``# robotidy: off`` in first line:

.. code-block:: robotframework

    # robotidy: off
    *** Settings ***
    Library    Collections

You can also disable formatting in whole section if you put ``# robotidy: off`` in section header:

.. code-block:: robotframework

    *** Test Cases ***
    Formatted
        Step

    *** Keywords ***  # robotidy: off
    Not Formatted
        Step
