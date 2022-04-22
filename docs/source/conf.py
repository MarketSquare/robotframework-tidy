import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))
import datetime

from robotidy.version import __version__

project = "Robotidy"
copyright = f"{datetime.datetime.now().year}, Bartlomiej Hirsz"
author = "Bartłomiej Hirsz"

release = __version__
version = __version__
master_doc = "index"

extensions = ["sphinx_tabs.tabs", "sphinx_copybutton"]

templates_path = ["_templates"]

exclude_patterns = []

html_theme = "alabaster"

html_theme_options = {
    "description": "Robot Framework code formatter",
    "logo": "robotidy_logo_small.png",
    "logo_name": True,
    "logo_text_align": "center",
    "show_powered_by": False,
    "github_user": "MarketSquare",
    "github_repo": "robotframework-tidy",
    "github_banner": False,
    "github_button": True,
    "show_related": False,
    "note_bg": "#FFF59C",
    "github_type": "star",
}


html_static_path = ["_static"]
html_favicon = "_static/robotidy.ico"
