Welcome to robotidy's documentation!
====================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

.. toctree::
   :maxdepth: 2
   :hidden:

   transformers/index.rst
   configuration
   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. tabs::

   .. code-tab:: robotframework Before

      *** Settings ***
      # whole line comment that should be ignored
      Resource  ..${/}resources${/}resource.robot
      Library      SeleniumLibrary
      Library   Mylibrary.py
      Variables  variables.py
      Test Timeout  1 min

   .. code-tab:: robotframework After

      *** Settings ***
      # whole line comment that should be ignored
      Resource            ..${/}resources${/}resource.robot
      Library             SeleniumLibrary
      Library             Mylibrary.py
      Variables           variables.py
      Test Timeout        1 min
