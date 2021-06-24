Introduction
------------
Robotidy is a tool for autoformatting Robot Framework code.

It is spiritual descendant of Robot Framework's internal robot.tidy package.

Documentation
-------------
Full documentation available Full documentation available `here <https://robotidy.readthedocs.io>`_.

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

Navigate to sections in the navigation menu such as :ref:`transformers` or :ref:`configuration` to read more.