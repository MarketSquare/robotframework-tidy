.. _AlignSettingsSection:

AlignSettingsSection
================================

Align statements in ``*** Settings ***`` section to columns.

.. |TRANSFORMERNAME| replace:: AlignSettingsSection
.. include:: enabled_hint.txt

.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

            *** Settings ***
            Library      SeleniumLibrary
            Library   Mylibrary.py
            Variables  variables.py
            Test Timeout  1 min
              # this should be left aligned

    .. tab-item:: After

        .. code:: robotframework

            *** Settings ***
            Library         SeleniumLibrary
            Library         Mylibrary.py
            Variables       variables.py
            Test Timeout    1 min
            # this should be left aligned

Align up to columns
-------------------
You can configure how many columns should be aligned to the longest token in given column. The remaining columns
will use fixed length separator length ``--spacecount``. By default only first two columns are aligned.

Example of how AlignSettingsSection transformer behaves with default configuration and multiple columns:

.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

            *** Settings ***
            Library    CustomLibrary   WITH NAME  name
            Library    ArgsedLibrary   ${1}  ${2}  ${3}

            Documentation     Example using the space separated format.
            ...  and this documentation is multiline
            ...  where this line should go I wonder?

    .. tab-item:: After

        .. code:: robotframework

            *** Settings ***
            Library             CustomLibrary    WITH NAME    name
            Library             ArgsedLibrary    ${1}    ${2}    ${3}

            Documentation       Example using the space separated format.
            ...                 and this documentation is multiline
            ...                 where this line should go I wonder?

You can configure it to align three columns::

    robotidy --configure AlignSettingsSection:up_to_column=3 src

.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

            *** Settings ***
            Library    CustomLibrary   WITH NAME  name
            Library    ArgsedLibrary   ${1}  ${2}  ${3}

            Documentation     Example using the space separated format.
            ...  and this documentation is multiline
            ...  where this line should go I wonder?

    .. tab-item:: After

        .. code:: robotframework

            *** Settings ***
            Library             CustomLibrary    WITH NAME    name
            Library             ArgsedLibrary    ${1}         ${2}     ${3}

            Documentation       Example using the space separated format.
            ...                 and this documentation is multiline
            ...                 where this line should go I wonder?

To align all columns set ``up_to_column`` to 0.

Extra indent for keyword arguments
-----------------------------------
Arguments in multiline settings are indented by additional ``argument_indent`` (default ``4``) spaces.
You can configure the indent or disable it by setting ``argument_indent`` to 0.

.. tab-set::

    .. tab-item:: argument_indent=4 (default)

        .. code:: robotframework

            *** Settings ***
            Suite Setup         Start Session
            ...                     host=${IPADDRESS}
            ...                     user=${USERNAME}
            ...                     password=${PASSWORD}
            Suite Teardown      Close Session

    .. tab-item:: argument_indent=2

        .. code:: robotframework

            *** Settings ***
            Suite Setup         Start Session
            ...                   host=${IPADDRESS}
            ...                   user=${USERNAME}
            ...                   password=${PASSWORD}
            Suite Teardown      Close Session

    .. tab-item:: argument_indent=0

        .. code:: robotframework

            *** Settings ***
            Suite Setup         Start Session
            ...                 host=${IPADDRESS}
            ...                 user=${USERNAME}
            ...                 password=${PASSWORD}
            Suite Teardown      Close Session

``WITH NAME`` arguments are not indented:

.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

            *** Settings ***
            Library             SeleniumLibrary
            ...                 timeout=${TIMEOUT}
            ...                 implicit_wait=${TIMEOUT}
            ...                 run_on_failure=Capture Page Screenshot
            ...                 WITH NAME    Selenium

    .. tab-item:: After

        .. code:: robotframework

            Library             SeleniumLibrary
            ...                     timeout=${TIMEOUT}
            ...                     implicit_wait=${TIMEOUT}
            ...                     run_on_failure=Capture Page Screenshot
            ...                 WITH NAME    Selenium

Fixed width of column
-------------------------
It's possible to set fixed minimal width of column. To configure it use ``min_width`` parameter::

    robotidy --configure AlignSettingsSection:min_width=30 src

This configuration respects ``up_to_column`` parameter but ignores ``argument_indent``.

.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

            *** Settings ***
            Library    CustomLibrary   WITH NAME  name
            Library    ArgsedLibrary   ${1}  ${2}  ${3}

            Documentation     Example using the space separated format.
            ...  and this documentation is multiline
            ...  where this line should go I wonder?

    .. tab-item:: After

        .. code:: robotframework

            *** Settings ***
            Library                      CustomLibrary   WITH NAME  name
            Library                      ArgsedLibrary   ${1}  ${2}  ${3}

            Documentation                Example using the space separated format.
            ...                          and this documentation is multiline
            ...                          where this line should go I wonder?

Select lines to transform
-------------------------
AlignSettingsSection does also support global formatting params ``startline`` and ``endline``::

    robotidy --startline 2 --endline 3 --configure AlignSettingsSection:up_to_column=3 src


.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

            *** Settings ***
            Metadata  Version  2.0  # this should be not aligned
            Metadata      More Info  For more information about *Robot Framework* see http://robotframework.org
            Metadata     Executed At  {HOST}

    .. tab-item:: After

        .. code:: robotframework

            *** Settings ***
            Metadata  Version  2.0  # this should be not aligned
            Metadata    More Info       For more information about *Robot Framework* see http://robotframework.org
            Metadata    Executed At     {HOST}
