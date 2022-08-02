.. _NormalizeSectionHeaderName:

NormalizeSectionHeaderName
======================================

Normalize section headers names.

.. |TRANSFORMERNAME| replace:: NormalizeSectionHeaderName
.. include:: enabled_hint.txt

Robot Framework is quite flexible with the section header naming. Following lines are equal::

    *setting
    *** SETTINGS
    *** SettingS ***

This transformer normalize naming to follow ``*** SectionName ***`` format (with plurar variant)::

    *** Settings ***
    *** Keywords ***
    *** Test Cases ***
    *** Variables ***
    *** Comments ***

Optional data after section header (for example data driven column names) is preserved.
It is possible to upper case section header names by passing ``uppercase=True`` parameter::

    robotidy --configure NormalizeSectionHeaderName:uppercase=True src

.. tab-set::

    .. tab-item:: Before

        .. code:: robotframework

            * setting *

    .. tab-item:: After

        .. code:: robotframework

            *** SETTINGS ***
