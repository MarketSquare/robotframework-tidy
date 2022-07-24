.. _Translate:

Translate
================================

Translate Robot Framework source files from one or many languages to different one.

.. note::
    Required Robot Framework version: >=6.0

.. |TRANSFORMERNAME| replace:: Translate
.. include:: disabled_hint.txt


Example of Robot Framework markers translation:

.. tab-set::

    .. tab-item:: Before (default English)

        .. code:: robotframework

            *** Settings ***
            Documentation    Dokumentacja zestawu

            Library    Collections
            Variables    vars.py

            *** Test Cases ***
            Pierwszy test
                [Setup]    Setup Keyword
                Step 1

    .. tab-item:: After (translated to Polish)

        .. code:: robotframework


            *** Ustawienia ***
            Documentation    Dokumentacja zestawu

            Biblioteka    Collections
            Zmienne    vars.py

            *** Przypadki Testowe ***
            Pierwszy test
                [Inicjalizacja]    Setup Keyword
                Step 1

The language can be configured using ``language`` parameter with the language code (default ``en`` - English)::

    robotidy --configure Translate:enabled=True:language=se

Since the translation is from one or many languages to one, only one language can be configured.

Source language
----------------

Robotidy will translate only markers that can be recognized. If your source file is written in different language
you need to configure Robotidy to recognize given language. See :ref:`language_support` for more details.
Following example configure Robotidy to read English, Polish and German languages and translate Robot Framework
markers to Ukrainian::

    robotidy --configure Translate:enabled=True:language:uk --language pl,de source_in_pl_and_de.robot

BDD keywords
-------------

BDD keywords are not translated by default. Set ``translate_bdd`` parameter to ``True`` to enable it::

    robotidy --configure Translate:enabled=True:translate_bdd=True files/

.. tab-set::

    .. tab-item:: Before (default English)

        .. code:: robotframework

            *** Test Cases ***
            Test with BDD keywords
                Given login page is open
                When valid username and password are inserted
                And credentials are submitted
                Then welcome page should be open

    .. tab-item:: After (translated BDD keywords to German)

        .. code:: robotframework

            *** Testfälle ***
            Test with BDD keywords
                Angenommen login page is open
                Wenn valid username and password are inserted
                Und credentials are submitted
                Dann welcome page should be open

Some language have more than one alternative to BDD keyword. For example Polish can use "Kiedy" or "Gdy" when
translating "When" keyword. In this situation Robotidy will chose the first one (sorted alphabetically). It can
be overwritten using  ``<bdd_keyword>_alternative`` parameters::

    robotidy --configure Translate:enabled=True:language=pl:translate_bdd=True:when_alternative=Gdy files/

Language headers
-----------------

Robotidy can add or replace existing language header in the files. For example, if you're translating file
written in German to Swedish, the language header will change from ``language: de`` to ``language: se``.
Translation to English will remove language header since it's not necessary.
To do this configure ``add_language_header`` parameter to ``True``::

    robotidy --configure Translate:enabled=True:add_language_header=True files/

.. tab-set::

    .. tab-item:: Before (default German)

        .. code:: robotframework

            # language: de

            *** Testfälle ***
            Test
                Step

    .. tab-item:: Translated to Swedish

        .. code:: robotframework

            # language: se

            *** Testfall ***
            Test
                Step

    .. tab-item:: Translated to English

        .. code:: robotframework

            *** Test Cases ***
            Test
                Step
