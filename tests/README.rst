Robotidy tests
==============

There are two types of testing for robotidy: unit tests and acceptance testing. Both are implemented using ``pytest``.
Internal methods should have at least 90% coverage. Transformers should have 100% acceptance testing coverage.

.. contents::
   :local:

Coverage
--------
You can generate coverage html files locally by running in main directory::

    coverage run -m pytest
    coverage html

Unit tests
----------

Unit tests are located under utest/ directory. Test for particular file are located under test_<filename>.py.
Common methods are stored in utest/utils.py. For running the robotidy itself (through cli) we can use ``run_tidy``
method.

You can run tests by running::

    pytest tests\utest

Acceptance tests
----------------

Acceptance tests are located under atest/ directory. There is separate directory for each transformer. Tests for
transformers are defined in ``test_transformer.py`` file under each directory. In the same directory test data is stored.
Source files should go to ``source`` directory and expected files to ``expected`` directory.

You can add test methods and then run tidy against your source code using::

    run_tidy_and_compare(transformer_name: str, source: str, expected: Optional[str] = None, config: str = ''):

Transformer name and list of sources are mandatory. Here is minimal example::

    run_tidy_and_compare('MyTransformer', 'test.robot')

It will execute following:

   robotidy --transform MyTransformer MyTransformer/test.robot

If you did not provide expected filename it will use source name (meaning that for ``test.robot`` found in
``source`` expected file will be ``test.robot`` stored in ``expected``).

You can use the same source name with different transformer option and different expected files. For example::

    run_tidy_and_compare('MyTransformer', 'test.robot', 'option1.robot', config=':option1=True')
    run_tidy_and_compare('MyTransformer', 'test.robot', 'option2.robot', config=':option2=True')

It's equivalent of executing::

    robotidy --transform MyTransformer:option1=True MyTransformer/test.robot
    robotidy --transform MyTransformer:option2=True MyTransformer/test.robot

But in first case our output will be compared to ``option1.robot`` file and in second case to ``option2.robot``.
``config`` parameter is appended in command line right after ``--transformer <transformer_name>``.

For negative test scenarios you can use ``run_tidy`` method (also used by ``run_tidy_and_compare`` under hood) with
optional expected ``exit_code`` argument.