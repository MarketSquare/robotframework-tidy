.. _NormalizeSectionHeaderName:

NormalizeSectionHeaderName
======================================

Normalize section headers names.

NormalizeSectionHeaderName is included in the default transformers but it can be also run separately with::

    robotidy --transform NormalizeSectionHeaderName src

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

.. tabs::

    .. code-tab:: robotframework Before

        * setting *

    .. code-tab:: robotframework After

        *** SETTINGS ***

Supports global formatting params: ``--startline`` and ``--endline``.