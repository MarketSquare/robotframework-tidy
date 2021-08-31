.. _RenameTestCases:

RenameTestCases
================================

Enforce test case naming.

RenameTestCases is not included in default transformers, that's why you need to call it with ``--transform`` explicitly::

    robotidy --transform RenameTestCases src

Or configure `enable` parameter::

    robotidy --configure RenameTestCases:enabled=True

This transformer capitalizes first letter of test case name, removes trailing dot and strips leading/trailing whitespace.

It is also possible to configure `replace_pattern` parameter to find and replace regex pattern. Use `replace_to`
to set a replacement value. This configuration::

    robotidy --transform RenameTestCases -c RenameTestCases:replace_pattern=[A-Z]{3,}-\d{2,}:replace_to=foo

Replaces all occurrences of given pattern with string 'foo':

.. tabs::

    .. code-tab:: robotframework Before

        *** Test Cases ***
        test ABC-123
            No Operation

    .. code-tab:: robotframework After
        *** Test Cases ***
        Test foo
            No Operation

Supports global formatting params: ``--startline`` and ``--endline``.