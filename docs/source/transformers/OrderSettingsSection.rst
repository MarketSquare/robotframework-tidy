.. _OrderSettingsSection:

OrderSettingsSection
================================

Order settings inside ``*** Settings ***`` section.

Settings are grouped in following groups:
  - documentation (Documentation, Metadata),
  - imports (Library, Resource, Variables),
  - settings (Suite Setup and Teardown, Test Setup and Teardown, Test Timeout, Test Template),
  - tags (Force Tags, Default Tags)

Then ordered by groups (according to ``group_order = documentation,imports,settings,tags`` order). Every
group is separated by ``new_lines_between_groups = 1`` new lines.
Settings are grouped inside group. Default order can be modified through following parameters:
  - ``documentation_order = documentation,metadata``
  - ``imports_order = library,resource,variables``
  - ``settings_order = suite_setup,suite_teardown,test_setup,test_teardown,test_timeout,test_template``

Setting names omitted from custom order will be removed from the file. In following example we are missing metadata
therefore all metadata will be removed::

    robotidy --configure OrderSettingsSection:documentation_order=documentation

Libraries are grouped into built in libraries and custom libraries.
Parsing errors (such as Resources instead of Resource, duplicated settings) are moved to the end of section.