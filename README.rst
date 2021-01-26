.. Badges

|Unit tests| |Codecov| |License|


Robotidy
===============

.. contents::
   :local:

Introduction
------------
Robotidy is spiritual descendant of Robot Framework's ``robot.tidy`` package. Its main purpose is to format
Robot Framework code according to agreed code standards. You can run Robotidy without configuring anything but
you can also change how it behaves through CLI or configuration file.

Requirements
------------

Python 3.7+ and Robot Framework 4.0.0+.

Installation
------------

You can install Robotidy by running::

    pip install git+git://github.com/MarketSquare/robotframework-tidy

Usage
-----
When called without any arguments, robotidy will not do anything. It requires at least one argument: source to file/directory
with robot files::

    robotidy tests
    robotidy test.robot
    robotidy tests/resources  test.robot


Executing selected transformers
-------------------------------
You can run robotidy with selected transformers. Use ``--transform`` argument for this::

    robotidy --transform ReplaceRunKeywordIf src

Some transformers provide configurable parameters. You can modify them by adding `:` after transformer name::

    robotidy --transform DiscardEmptySections:allow_only_comments=True src

It is possible to develop your own transformers. You can use module name (if it is installed in your env) or path to
file with class::

    robotidy --transform MyTransformers.YourCustomTransformer --transform C:\transformers\YourCustomTransformer2.py src

Command line options
--------------------
You can list available options by running ``robotidy --help``::

   Usage: robotidy [OPTIONS] [PATH(S)]

   Options:
     --transform TRANSFORMER_NAME    Transform files from [PATH(S)] with given
                                     transformer

     --overwrite / --no-overwrite    Overwrite source files.
     --diff                          Output diff of each processed file.
     -s, --spacecount INTEGER        The number of spaces between cells in the
                                     plain text format. Default is 4.

     -l, --lineseparator [native|windows|unix]
                                     Line separator to use in outputs. The
                                     default is 'native'.
                                     native:  use operating system's native line separators
                                     windows: use Windows line separators (CRLF)
                                     unix:    use Unix line separators (LF)

     -p, --usepipes                  Use pipe ('|') as a column separator in the
                                     plain text format.

     -sl, --startline INTEGER        Limit robotidy only to selected area. If
                                     --endline is not provided, format text only
                                     at --startline. Line numbers start from 1.

     -el, --endline INTEGER          Limit robotidy only to selected area. Line
                                     numbers start from 1.

     -v, --verbose
     --config FILE                   Read configuration from FILE path.
     --list-transformers             List available transformers and exit.
     --describe-transformer TRANSFORMER_NAME
                                     Show documentation for selected transformer.
     --version                       Show the version and exit.
     --help                          Show this message and exit.


Configuration file
-------------------
Robotidy can read configuration from files with ``toml`` type. Options are loaded in following order:
 - auto-discovered configuration file (``robotidy.toml``)
 - configuration file passed with ``--config``
 - command line arguments

By default if ``--config`` argument is not used, robotidy look for configuration file named ``robotidy.toml``
in common directories for passed sources and execution directory.

It is possible to mix configuration between config file and command line, but if the same parameters are used
command line parameter value will be used instead (reference to loading order). It's important because
you cannot specify some of the transformers in config file and come in CLI - you need to list all required transformers
in one place.

Example configuration file::

    [main]
    overwrite = false
    diff = false
    spacecount = 4

    [transformers]
        [transformers.DiscardEmptySections]
            allow_only_comments = true
        [transformers.ReplaceRunKeywordIf]


.. Badges links

.. |Unit tests|
   image:: https://img.shields.io/github/workflow/status/MarketSquare/robotframework-tidy/Unit%20tests/main
   :alt: GitHub Workflow Unit Tests Status
   :target: https://github.com/MarketSquare/robotframework-tidy/actions?query=workflow%3A%22Unit+tests%22

.. |Codecov|
   image:: https://img.shields.io/codecov/c/github/MarketSquare/robotframework-tidy/main
   :alt: Code coverage on master branch

.. |License|
   image:: https://img.shields.io/pypi/l/robotframework-robocop
   :alt: PyPI - License
