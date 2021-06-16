.. _AlignVariablesSection:

AlignVariablesSection
==================================

Align variables in ``*** Variables ***`` section to columns.

Following code::

    *** Variables ***
    ${VAR}  1
    ${LONGER_NAME}  2
    &{MULTILINE}  a=b
    ...  b=c

will be transformed to::

    *** Variables ***
    ${VAR}          1
    ${LONGER_NAME}  2
    &{MULTILINE}    a=b
    ...             b=c

You can configure how many columns should be aligned to longest token in given column. The remaining columns
will use fixed length separator length ``--space_count``. By default only first two columns are aligned.
To align first three columns::

   robotidy --transform AlignVariablesSection:up_to_column=3

To align all columns set ``up_to_column`` to 0.

Supports global formatting params: ``--startline`` and ``--endline``.