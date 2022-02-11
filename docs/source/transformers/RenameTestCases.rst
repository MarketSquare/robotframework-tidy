.. _RenameTestCases:

RenameTestCases
================================

Enforce test case naming. This transformer capitalizes first letter of test case name, removes trailing dot and
strips leading/trailing whitespaces.

.. |TRANSFORMERNAME| replace:: RenameTestCases
.. include:: disabled_hint.txt

It is also possible to configure ``replace_pattern`` parameter to find and replace regex pattern. Use ``replace_to``
to set a replacement value. This configuration::

    robotidy --transform RenameTestCases -c RenameTestCases:replace_pattern=[A-Z]{3,}-\d{2,}:replace_to=foo

replaces all occurrences of given pattern with string 'foo':

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