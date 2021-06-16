.. _AlignSettingsSection:

AlignSettingsSection
================================

Align lines in ``*** Settings ***`` section to columns.

Following code::

    *** Settings ***
    Library      SeleniumLibrary
    Library   Mylibrary.py
    Variables  variables.py
    Test Timeout  1 min
        # this should be left aligned

will be transformed to::

    *** Settings ***
    Library         SeleniumLibrary
    Library         Mylibrary.py
    Variables       variables.py
    Test Timeout    1 min
    # this should be left aligned

You can configure how many columns should be aligned to longest token in given column. The remaining columns
will use fixed length separator length ``--space_count``. By default only first two columns are aligned.
To align first three columns::

   robotidy --transform AlignSettingsSection:up_to_column=3

To align all columns set ``up_to_column`` to 0.

Supports global formatting params: ``--startline``, ``--endline`` and ``--space_count``
(for columns with fixed length).