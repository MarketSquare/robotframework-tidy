Deprecation notice
-------------------

Starting with Robocop 6.0, Robotidy is now integrated into Robocop.
The standalone version of Robotidy is deprecated and may not support the latest Robot Framework versions.

Please see https://robocop.readthedocs.io/en/stable/ for Robocop documentation.

Introduction
------------
Robotidy is a tool for autoformatting Robot Framework code.

It is spiritual descendant of Robot Framework's internal robot.tidy package.

Requirements
------------

Python 3.7+ and Robot Framework 4.0.0+.

Installation
------------

You can install Robotidy simply by running::

    pip install robotframework-tidy

Usage
-----
Call robotidy with path(s) to file/directory with robot files::

    robotidy tests
    robotidy test.robot
    robotidy tests/resources test.robot

All command line options can be displayed in help message by executing::

    robotidy --help

Start with :ref:`quickstart` to see how you can use the tool. You can also navigate to :ref:`transformers`
or :ref:`configuration` to read more.
