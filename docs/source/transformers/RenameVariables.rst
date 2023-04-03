.. _RenameVariables:

RenameVariables
================
Rename and normalize variable names.

.. |TRANSFORMERNAME| replace:: RenameVariables
.. include:: disabled_hint.txt

Variable names in Settings, Variables, Test Cases and Keywords section are renamed. Variables in arguments are
also affected.

Following conventions are applied:

- variable case depends on the variable scope (lowercase for local variables and uppercase for global variables)
- leading and trailing whitespace is stripped
- more than 2 consecutive whitespace in name is replaced by 1
- whitespace is replaced by _
- camelCase is converted to snake_case

Conventions can be configured or switched off using parameters - read more in the following sections.

.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

            *** Settings ***
            Suite Setup    ${keyword}

            *** Variables ***
            ${global}    String with {other global}

            *** Test Cases ***
            Test
                ${local}    Set Variable    variable
                Log    ${local}
                Log    ${global}
                Log    ${local['item']}

            *** Keywords ***
            Keyword
                [Arguments]    ${ARG}
                Log    ${arg}

            Keyword With ${EMBEDDED}
                Log    ${emb   eded}

    .. tab-item:: After

        .. code:: robotframework

            *** Settings ***
            Suite Setup    ${KEYWORD}

            *** Variables ***
            ${GLOBAL}    String with {OTHER_GLOBAL}

            *** Test Cases ***
            Test
                ${local}    Set Variable    variable
                Log    ${local}
                Log    ${GLOBAL}
                Log    ${local['item']}

            *** Keywords ***
            Keyword
                [Arguments]    ${arg}
                Log    ${arg}

            Keyword With ${embedded}
                Log    ${emb_eded}

.. note::

    RenameVariables is still under development and is not considered feature complete. Following syntax is not yet supported:

      - variable evaluation with ``${variable * 2}`` (following will be replaced to ``${variable_*_2}``

    Robotidy can be locally disabled with # robotidy: off if you want to ignore specific cases.

Variable case in Settings section
---------------------------------

All variables in the the ``*** Settings ***`` section are formatted to be uppercase. This behaviour is configurable
using ``settings_section_case``::

    > robotidy -c RenameVariables:settings_section_case=upper src

Allowed values are:

- ``upper`` (default) to uppercase names
- ``lower`` to lowercase names
- ``ignore`` to leave existing case

Variable case in Variables section
----------------------------------

All variables in the the ``*** Variables ***`` section are formatted to be uppercase. This behaviour is configurable
using ``variables_section_case``::

    > robotidy -c RenameVariables:variables_section_case=upper src

Allowed values are:

- ``upper`` (default) to uppercase names
- ``lower`` to lowercase names
- ``ignore`` to leave existing case

Variable case in Keywords, Tasks and Test Cases sections
--------------------------------------------------------

Variable case in ``*** Keywords ***``, ``*** Tasks ***`` and ``*** Test Cases ***`` sections depends on the
variable scope. Local variables are lowercase and global variables are uppercase. Any unknown variable (not defined
in current keyword or test case) is considered as global. You can configure what happes with unknown variables using
``unknown_variables_case``::

    > robotidy -c RenameVariables:unknown_variables_case=upper src

Allowed values are:

- ``upper`` (default) to uppercase unknown names
- ``lower`` to lowercase unknown names
- ``ignore`` to leave existing case

.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

            *** Keywords ***
            Keyword
                [Arguments]    ${arg}  # ${arg} is known
                ${local}    Set Variable    value  # since we set it, ${local} is also known
                Keyword Call    ${arg}    ${local}    ${global}  # ${global} is unknown

    .. tab-item:: After (unknown_variables_case = upper)

        .. code:: robotframework

            *** Keywords ***
            Keyword
                [Arguments]    ${arg}  # ${arg} is known
                ${local}    Set Variable    value  # since we set it, ${local} is also known
                Keyword Call    ${arg}    ${local}    ${GLOBAL}  # ${global} is unknown

    .. tab-item:: After (unknown_variables_case = lower)

        .. code:: robotframework

            *** Keywords ***
            Keyword
                [Arguments]    ${arg}  # ${arg} is known
                ${local}    Set Variable    value  # since we set it, ${local} is also known
                Keyword Call    ${arg}    ${local}    ${global}  # ${global} is unknown

    .. tab-item:: After (unknown_variables_case = ignore)

        .. code:: robotframework

            *** Keywords ***
            Keyword
                [Arguments]    ${arg}  # ${arg} is known
                ${local}    Set Variable    value  # since we set it, ${local} is also known
                Keyword Call    ${arg}    ${local}    ${global}  # ${global} is unknown

Converting camelCase to snake_case
----------------------------------

Variable names written in camelCase are converted to snake_case. You can disable this behaviour by configuring
``convert_camel_case`` to ``False``::

    > robotidy -c RenameVariables:convert_camel_case=False

.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

            *** Variables ***
            ${camelCase}    value

            *** Keywords ***
            Keyword
                ${CamelCase_Name}    Set Variable    value
                Keyword Call    ${CamelCase_Name}

    .. tab-item:: After - default (convert_camel_case = True)

        .. code:: robotframework

            *** Variables ***
            ${camel_case}    value

            *** Keywords ***
            Keyword
                ${camel_case_name}    Set Variable    value
                Keyword Call    ${camel_case_name}

    .. tab-item:: After (convert_camel_case = False)

        .. code:: robotframework

            *** Variables ***
            ${CAMELCASE}    value

            *** Keywords ***
            Keyword
                ${camelcase_name}    Set Variable    value
                Keyword Call    ${camelcase_name}

Variable separator
-------------------

Separators inside variable name are converted to underscore (``_``). You can configure it using ``variable_separator``::

    > robotidy -c RenameVariables:variable_separator=underscore

Allowed values are:

- ``underscore`` (default)
- ``space``

.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

            *** Variables ***
            ${camelCase}    value

            *** Keywords ***
            Keyword
                ${variable_name}    Set Variable    value
                Keyword Call    ${variable name}

    .. tab-item:: After - default (variable_separator = underscore)

        .. code:: robotframework

            *** Variables ***
            ${CAMEL_CASE}    value

            *** Keywords ***
            Keyword
                ${variable_name}    Set Variable    value
                Keyword Call    ${variable_name}

    .. tab-item:: After (variable_separator = space)

        .. code:: robotframework

            *** Variables ***
            ${CAMEL CASE}    value

            *** Keywords ***
            Keyword
                ${variable name}    Set Variable    value
                Keyword Call    ${variable name}

Skip formatting
----------------

It is possible to use the following arguments to skip formatting of the code:

- :ref:`skip sections`

It is also possible to use disablers (:ref:`disablers`) but ``skip`` option
makes it easier to skip all instances of given type of the code.