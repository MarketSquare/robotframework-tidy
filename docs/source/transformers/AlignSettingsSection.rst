.. _AlignSettingsSection:

AlignSettingsSection
================================

Align statements in ``*** Settings ***`` section to columns.

AlignSettingsSection is included in default transformers but it can be also
run separately with::

   robotidy --transform AlignSettingsSection src

.. tabs::

   .. code-tab:: robotframework Before

      *** Settings ***
      Library      SeleniumLibrary
      Library   Mylibrary.py
      Variables  variables.py
      Test Timeout  1 min
          # this should be left aligned

   .. code-tab:: robotframework After

      *** Settings ***
      Library         SeleniumLibrary
      Library         Mylibrary.py
      Variables       variables.py
      Test Timeout    1 min
      # this should be left aligned

Align up to columns
-------------------
You can configure how many columns should be aligned to longest token in given column. The remaining columns
will use fixed length separator length ``--space_count``. By default only first two columns are aligned.

Example of how AlignSettingsSection transformer behaves with default configuration and multiple columns:

.. tabs::

   .. code-tab:: robotframework Before

      *** Settings ***
      Library    CustomLibrary   WITH NAME  name
      Library    ArgsedLibrary   ${1}  ${2}  ${3}

      Documentation     Example using the space separated format.
      ...  and this documentation is multiline
      ...  where this line should go I wonder?

   .. code-tab:: robotframework After

      *** Settings ***
      Library             CustomLibrary    WITH NAME    name
      Library             ArgsedLibrary    ${1}    ${2}    ${3}

      Documentation       Example using the space separated format.
      ...                 and this documentation is multiline
      ...                 where this line should go I wonder?

You can configure it to align three columns::

    robotidy --configure AlignSettingsSection:up_to_column=3 src

.. tabs::

   .. code-tab:: robotframework Before

      *** Settings ***
      Library    CustomLibrary   WITH NAME  name
      Library    ArgsedLibrary   ${1}  ${2}  ${3}

      Documentation     Example using the space separated format.
      ...  and this documentation is multiline
      ...  where this line should go I wonder?

   .. code-tab:: robotframework After

      *** Settings ***
      Library             CustomLibrary    WITH NAME    name
      Library             ArgsedLibrary    ${1}         ${2}     ${3}

      Documentation       Example using the space separated format.
      ...                 and this documentation is multiline
      ...                 where this line should go I wonder?

To align all columns set ``up_to_column`` to 0.

Extra indent for keyword arguments
-----------------------------------
Arguments inside keywords in Suite Setup, Suite Teardown, Test Setup and Test Teardown are indented by additional
``argument_indent`` (default ``4``) spaces. You can configure the indent or disable it by setting ``argument_indent``
to 0.

.. tabs::

   .. code-tab:: robotframework argument_indent=4 (default)

        *** Settings ***
        Suite Setup         Start Session
        ...                     host=${IPADDRESS}
        ...                     user=${USERNAME}
        ...                     password=${PASSWORD}
        Suite Teardown      Close Session

   .. code-tab:: robotframework argument_indent=2

        *** Settings ***
        Suite Setup         Start Session
        ...                   host=${IPADDRESS}
        ...                   user=${USERNAME}
        ...                   password=${PASSWORD}
        Suite Teardown      Close Session

   .. code-tab:: robotframework argument_indent=0

        *** Settings ***
        Suite Setup         Start Session
        ...                 host=${IPADDRESS}
        ...                 user=${USERNAME}
        ...                 password=${PASSWORD}
        Suite Teardown      Close Session

Select lines to transform
-------------------------
AlignSettingsSection does also support global formatting params ``startline`` and ``endline``::

    robotidy --startline 2 --endline 3 --configure AlignSettingsSection:up_to_column=3 src


.. tabs::

   .. code-tab:: robotframework Before

      *** Settings ***
      Metadata  Version  2.0  # this should be not aligned
      Metadata      More Info  For more information about *Robot Framework* see http://robotframework.org
      Metadata     Executed At  {HOST}

   .. code-tab:: robotframework After

      *** Settings ***
      Metadata  Version  2.0  # this should be not aligned
      Metadata    More Info       For more information about *Robot Framework* see http://robotframework.org
      Metadata    Executed At     {HOST}
