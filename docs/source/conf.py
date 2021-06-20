# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import datetime
from robotidy.version import __version__



# -- Project information -----------------------------------------------------

project = 'Robotidy'
copyright = f'{datetime.datetime.now().year}, Bartlomiej Hirsz'
author = 'Bartłomiej Hirsz'

# The full version, including alpha/beta/rc tags
release = __version__
version = __version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx_tabs.tabs',
    'sphinx_copybutton'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

html_theme_options = {
    "description": "Robot Framework code formatter",
    "show_powered_by": False,
    "github_user": "MarketSquare",
    "github_repo": "robotframework-tidy",
    "github_banner": False,
    "github_button": True,
    "show_related": False,
    "note_bg": "#FFF59C",
    "github_type": "star"
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']