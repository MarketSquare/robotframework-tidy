Robotidy tests
==============

There are two types of testing for robotidy: unit tests and acceptance testing. Both are implemented using ``pytest``.
Internal methods should have at least 90% coverage. Transformers should have 100% acceptance testing coverage.

.. contents::
   :local:

Coverage
--------
You can generate coverage html files locally by running in main directory::

    nox -s coverage

Unit tests
----------

Unit tests are located under utest/ directory. Test for particular file are located under test_<filename>.py.
Common methods are stored in utest/utils.py. For running the robotidy itself (through cli) we can use ``run_tidy``
method.

You can run tests by running::

    pytest tests\utest

You can also use nox for running our tests in different environments::

    nox -s unit

Acceptance tests
----------------

Acceptance tests are located under atest/ directory. There is separate directory for each transformer. Tests for
transformers are defined in ``test_transformer.py`` file under each directory. In the same directory test data is stored.
Source files should go to ``source`` directory and expected files to ``expected`` directory.

If you generated transformer using invoke script (See ``invoke list`` too check possible commands) you should have get
prepared test stub::

    from tests.atest import TransformerAcceptanceTest

    class TestMyTransformer(TransformerAcceptanceTest):
        TRANSFORMER_NAME = 'MyTransformer'

        def test_transformer(self):
            self.compare(source='test.robot', expected='test.robot')

All acceptance test classes inherit from TransformerAcceptanceTest class. It provides you ``compare`` method for comparing
output after transforming source file with given ``TRANSFORMER_NAME`` transformer. Above example is equivalent of executing::

   robotidy --transform MyTransformer MyTransformer/test.robot

You can use the same source name with different transformer option and different expected files. For example::

    self.compare('test.robot', 'option1.robot', config=':option1=True')
    self.compare('test.robot', 'option2.robot', config=':option2=True')

It's equivalent of executing::

    robotidy --transform MyTransformer:option1=True MyTransformer/test.robot
    robotidy --transform MyTransformer:option2=True MyTransformer/test.robot

But in first case our output will be compared to ``option1.robot`` file and in second case to ``option2.robot``.
``config`` parameter is appended in command line right after ``--transformer <transformer_name>``.

For negative test scenarios you can use ``run_tidy`` method (also used by ``compare`` under hood) with
optional expected ``exit_code`` argument.

End to end tests
-----------------
E2E tests focus on verifying the stability of the Robotidy output. It includes:

  - ensuring that code will not be modified after several reruns of the tool
  - AST model modified by one transformer can be safely parsed by another transformer

E2E tests are defined in ``tests/e2e`` directory. They are skipped by default - since they take
longer time to finish. To enable them add ``--e2e`` flag to pytest command.

Due to the amount of the work needed to also define end to end tests our tests reuse the same
sources as acceptance tests. You can define additional tests by creating robot files that will be
transformed in the ``tests/e2e/test_data`` directory.

Every test data file is used to generate two tests:

  - transform with all default transformers (excluding disabled by default)
  - transform with all transformers (including disabled by default)

If the test data file is invalid (and cannot be used in E2E tests) you can add it to ``SKIP_TESTS`` dictionary.
Otherwise if the test data require more than default 1 rerun of the tool you can set amount of reruns needed in
``RERUN_NEEDED`` dictionary.
