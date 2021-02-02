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
method. To stop robotidy from overwriting the source file we need to add to our test class monkey patch method for
saving output::

    @patch('robotidy.app.Robotidy.save_model', new=save_tmp_model)

You can run tests by running::

    pytest tests\utest

Acceptance tests
----------------

Acceptance tests are located under atest/ directory. Tests for transformers are defined in ``test_transformers.py``
file. You can add tests for transformer by creating test class and prefixing it with::

    @patch('robotidy.app.Robotidy.save_model', new=save_tmp_model)

It will monkey patch the robotidy method for saving the output. In that way our source files will not be overwritten
and output will be written to actual/ directory instead. Test data should be stored in directory with the same name as
transformation (ie. ``DiscardEmptySections\``). Source files should go to ``source`` directory and expected files to
``expected`` directory.

You can add test methods and then run tidy against your source code using::

    run_tidy_and_compare(transformer_name: str, sources: List[str],
                         expected: Optional[List[str]] = None, config: str = ''):

Transformer name and list of sources are mandatory. Here is minimal example::

    run_tidy_and_compare('MyTransformer', ['test.robot'])

It will execute following:

   robotidy --transform MyTransformer MyTransformer/test.robot

If you did not provide expected filenames list it will use source list (meaning that for ``test.robot`` found in
``source`` expected file will be ``test.robot`` stored in ``expected``).

You can use the same source name with different transformer option and different expected files. For example::

    run_tidy_and_compare('MyTransformer', ['test.robot'], ['option1.robot'], config=':option1=True')
    run_tidy_and_compare('MyTransformer', ['test.robot'], ['option2.robot'], config=':option2=True')

It's equivalent of executing::

    robotidy --transform MyTransformer:option1=True MyTransformer/test.robot
    robotidy --transform MyTransformer:option2=True MyTransformer/test.robot

But in first case our output will be compared to ``option1.robot`` file and in second case to ``option2.robot``.
``config`` parameter is appended in command line right after ``--transformer <transformer_name>``.

For negative test scenarios you can use ``run_tidy`` method (also used by ``run_tidy_and_compare`` under hood) with
optional expected ``exit_code`` argument.