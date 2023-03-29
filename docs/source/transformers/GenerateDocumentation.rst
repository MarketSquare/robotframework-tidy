.. _GenerateDocumentation:

GenerateDocumentation
================================
Generate keyword documentation with the documentation template.

.. |TRANSFORMERNAME| replace:: GenerateDocumentation
.. include:: disabled_hint.txt


By default, GenerateDocumentation uses Google documentation template.

.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

            *** Keywords ***
            Keyword
                [Arguments]    ${arg}
                ${var}   ${var2}    Step
                RETURN    ${var}    ${var2}

    .. tab-item:: After

        .. code:: robotframework

            *** Keywords ***
            Keyword
                [Documentation]
                ...
                ...    Arguments:
                ...        ${arg}:
                ...
                ...    Returns:
                ...        ${var}
                ...        ${var2}
                [Arguments]    ${arg}
                ${var}   ${var2}    Step
                RETURN    ${var}    ${var2}

Overwriting documentation
--------------------------

The documentation will not be added if it's already present in the keyword. You can configure it
by using ``overwrite`` parameter:

.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

            *** Keywords ***
            Keyword With Documentation
                [Documentation]    Short description.
                [Arguments]    ${arg}
                Step

    .. tab-item:: After (overwrite = False)

        .. code:: robotframework

            *** Keywords ***
            Keyword With Documentation
                [Documentation]    Short description.
                [Arguments]    ${arg}
                Step

    .. tab-item:: After (overwrite = True)

        .. code:: robotframework

            *** Keywords ***
            Keyword With Documentation
                [Documentation]
                ...    Arguments:
                ...        ${arg}:
                [Arguments]    ${arg}
                Step

Custom template
----------------

Custom templates can be loaded from the file using ``doc_template`` parameter. If you pass
``google`` string it will use default template::

    > robotidy --configure GenerateDocumentation:doc_template=google src

Templates support Jinja templating engines and we are providing several variables based on the
keyword data. Below there is default template::

    {% if keyword.arguments|length > 0 %}
    {{ formatting.cont_indent }}Arguments:
    {%- for arg in keyword.arguments %}
    {{ formatting.cont_indent }}{{ formatting.cont_indent }}{{ arg.name }}: {% endfor %}
    {% endif -%}
    {% if keyword.returns|length > 0 %}
    {{ formatting.cont_indent }}Returns:
    {%- for value in keyword.returns %}
    {{ formatting.cont_indent }}{{ formatting.cont_indent }}{{ value }}: {% endfor %}
    {% endif -%}

You can use it as reference to create your own template. Following subsections explains possible
features in detail.

Path to template can be absolute or relative (to working directory or configuration file directory)::

    > robotidy --configure GenerateDocumentation:doc_template="C:/doc_templates/template.jinja" src
    > robotidy --configure GenerateDocumentation:doc_template="template.jinja" src

.. dropdown:: First line of the documentation

    First line of the template is also first line of the documentation - right after the ``[Documentation]`` setting.

    .. tab-set::

        .. tab-item:: Template

            .. code:: text

                    First line of template
                    Second line of example
                  Third line.

        .. tab-item:: Generated example

            .. code:: robotframework

                *** Keywords ***
                Keyword
                    [Documentation]    First line of template
                    ...    Second line of example
                    ...  Third line.
                    Step

.. dropdown:: Whitespace can be static or dynamic

Any whitespace in the template will apply to the documentation. For example you can put 4 spaces after every argument
and before `->` sign:

    .. tab-set::

        .. tab-item:: Template

            .. code:: text

                Args:
                {%- for arg in keyword.arguments %}
                        {{ arg.name }}    ->{% endfor %}
                {% endif -%}

        .. tab-item:: Code

            .. code:: robotframework

                *** Keywords ***
                Keyword
                    [Arguments]    ${arguments}    ${arg}    ${arg2}
                    Step

        .. tab-item:: Generated example

            .. code:: robotframework

                *** Keywords ***
                Keyword
                    [Documentation]
                    ...    Arguments:
                    ...        ${arguments}    ->
                    ...        ${arg    ->
                    ...        ${arg2}    ->
                    [Arguments]    ${arguments}    ${arg}    ${arg2}
                    Step
