.. _OrderSettingsSection:

OrderSettingsSection
================================

Order settings inside ``*** Settings ***`` section.

OrderSettingsSection is included in the default transformers but it can be also run separately with::

    robotidy --transform OrderSettingsSection src

Settings are grouped in following groups:

- documentation (Documentation, Metadata),
- imports (Library, Resource, Variables),
- settings (Suite Setup and Teardown, Test Setup and Teardown, Test Timeout, Test Template),
- tags (Force Tags, Default Tags)

Then ordered by groups (according to ``group_order = documentation,imports,settings,tags`` order). Every
group is separated by ``new_lines_between_groups = 1`` new lines.
Settings are grouped inside group. Default order can be modified through following parameters:

- ``documentation_order = documentation,metadata``
- ``imports_order = preserved``
- ``settings_order = suite_setup,suite_teardown,test_setup,test_teardown,test_timeout,test_template``

.. tabs::

    .. code-tab:: robotframework Before

        *** Settings ***
        Metadata  value  param

        Force Tags  tag
        ...  tag

        Documentation  doc  # this is comment
        ...  another line
        Test Timeout  1min

        # I want to be keep together with Test Setup

        Test Setup  Keyword


        Suite Setup  Keyword
        Default Tags  1
        Suite Teardown  Keyword2

        Variables   variables.py
        Library  Stuff
        Library  Collections
        Resource    robot.resource
        Library  stuff.py  WITH NAME  alias

    .. code-tab:: robotframework After

        *** Settings ***
        Documentation  doc  # this is comment
        ...  another line
        Metadata  value  param

        Variables   variables.py
        Library  Stuff
        Library  Collections
        Resource    robot.resource
        Library  stuff.py  WITH NAME  alias

        Suite Setup  Keyword
        Suite Teardown  Keyword2
        # I want to be keep together with Test Setup
        Test Setup  Keyword
        Test Timeout  1min

        Force Tags  tag
        ...  tag
        Default Tags  1

Using the same example with non default group order we will move tags from end to beginning of section::

    robotidy --configure OrderSettingsSection:group_order=tags,documentation,imports,settings src

.. tabs::

    .. code-tab:: robotframework Before

        *** Settings ***
        Metadata  value  param

        Force Tags  tag
        ...  tag

        Documentation  doc  # this is comment
        ...  another line
        Test Timeout  1min

        # I want to be keep together with Test Setup

        Test Setup  Keyword


        Suite Setup  Keyword
        Default Tags  1
        Suite Teardown  Keyword2

    .. code-tab:: robotframework After

        *** Settings ***
        Force Tags  tag
        ...  tag
        Default Tags  1

        Documentation  doc  # this is comment
        ...  another line
        Metadata  value  param

        Suite Setup  Keyword
        Suite Teardown  Keyword2
        # I want to be keep together with Test Setup
        Test Setup  Keyword
        Test Timeout  1min

Order of setting inside common group can also be changed::

    robotidy --configure OrderSettingsSection:settings_order=suite_teardown,suite_setup,test_setup,test_teardown,test_timeout,test_template src

.. tabs::

    .. code-tab:: robotframework Default order

        Suite Setup    Suite Setup Keyword
        Suite Teardown    Suite Teardown Keyword
        Test Timeout    1min

    .. code-tab:: robotframework Configured order

        Suite Teardown    Suite Teardown Keyword
        Suite Setup    Suite Setup Keyword
        Test Timeout    1min

By default order of imports is preserved. You can overwrite this behaviour::

    robotidy --configure OrderSettingsSections:imports_order=library,resource,variables

You can also preserve order inside any group by passing ``preserved`` instead of setting names::

    robotidy --configure OrderSettingsSections:settings_order=preserved

Setting names omitted from custom order will be removed from the file. In following example we are missing metadata
therefore all metadata will be removed::

    robotidy --configure OrderSettingsSection:documentation_order=documentation

Group of settings are separated by ``new_lines_between_groups = 1`` new lines. It can be configured::

    robotidy --configure OrderSettingsSection:new_lines_between_groups=2 src

.. tabs::

    .. code-tab:: robotframework Before

        Library  Collections
        Default Tags    tag
        Documentation  doc  # this is comment
        ...  another line
        Metadata  value  param

    .. code-tab:: robotframework Default separator

        Documentation  doc  # this is comment
        ...  another line
        Metadata  value  param

        Library  Collections

        Default Tags    tag

    .. code-tab:: robotframework 0

        Documentation  doc  # this is comment
        ...  another line
        Metadata  value  param
        Library  Collections
        Default Tags    tag

    .. code-tab:: robotframework 2

        Documentation  doc  # this is comment
        ...  another line
        Metadata  value  param


        Library  Collections


        Default Tags    tag

If you're not preserving the default order of libraries they will be grouped into built in libraries and custom libraries.
Parsing errors (such as Resources instead of Resource, duplicated settings) are moved to the end of section.

.. tabs::

    .. code-tab:: robotframework Before

        Test Templating  Template  # parsing error
        Library  Stuff
        Resource    robot.resource
        Library  Dialogs  # built in library

    .. code-tab:: robotframework After

        Library  Dialogs  # built in library
        Library  Stuff
        Resource    robot.resource

        Test Templating  Template  # parsing error
