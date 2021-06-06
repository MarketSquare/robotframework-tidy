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

    pip install robotframework-tidy

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

Some transformers provide configurable parameters. You can pass your own values using --config/-c TRANSFORMER_NAME:param=value syntax::

    robotidy --configure DiscardEmptySections:allow_only_comments=True src

It is also possible to supply parameters using ``--transform`` option. The main difference is that ``--transform`` works like
include option in Robot Framework while ``--configure`` allows you to configure selected transformers and still run all of them::

   robotidy --transform DiscardEmptySections:allow_only_comments=True src

It is possible to develop your own transformers. You can use module name (if it is installed in your env) or path to
file with class::

    robotidy --transform MyTransformers.YourCustomTransformer --transform C:\transformers\YourCustomTransformer2.py src

Command line options
--------------------
You can list available options by running ``robotidy --help``

Configuration file
-------------------
Robotidy can read configuration from files with ``toml`` type. Options are loaded in following order:
 - auto-discovered configuration file (``robotidy.toml`` or ``pyproject.toml`` inside ``[tool.robotidy]`` section)
 - configuration file passed with ``--config``
 - command line arguments

By default if ``--config`` argument is not used, robotidy look for configuration file in common directories
for passed sources and execution directory.

It is possible to mix configuration between config file and command line, but if the same parameters are used
command line parameter value will be used instead (reference to loading order). It's important because
you cannot specify some of the transformers in config file and come in CLI - you need to list all required transformers
in one place.

Example configuration file::

   overwrite = false
   diff = false
   spacecount = 4
   transform = [
       "DiscardEmptySections:allow_only_comments=True",
       "ReplaceRunKeywordIf"
   ]
   configure = [
       "DiscardEmptySections:allow_only_comments=False"
   ]

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
