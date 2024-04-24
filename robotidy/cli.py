import sys
from pathlib import Path
from typing import List, Optional, Pattern, Tuple, Union

try:
    import rich_click as click

    RICH_PRESENT = True
except ImportError:  # Fails on vendored-in LSP plugin
    import click

    RICH_PRESENT = False

from robotidy import app
from robotidy import config as config_module
from robotidy import decorators, exceptions, files, skip, version
from robotidy.config import RawConfig, csv_list_type, validate_target_version
from robotidy.rich_console import console
from robotidy.transformers import (
    TransformConfigMap,
    TransformConfigParameter,
    complete_transformer_name,
    load_transformers,
)
from robotidy.utils import misc

CLI_OPTIONS_LIST = [
    {
        "name": "Run only selected transformers",
        "options": ["--transform"],
    },
    {
        "name": "Load custom transformers",
        "options": ["--load-transformers"],
    },
    {
        "name": "Work modes",
        "options": ["--overwrite", "--diff", "--check", "--force-order"],
    },
    {
        "name": "Documentation",
        "options": ["--list", "--desc"],
    },
    {
        "name": "Configuration",
        "options": ["--ignore-git-dir", "--generate-config"],
    },
    {
        "name": "Global formatting settings",
        "options": [
            "--spacecount",
            "--indent",
            "--continuation-indent",
            "--line-length",
            "--lineseparator",
            "--separator",
            "--startline",
            "--endline",
        ],
    },
    {"name": "File exclusion", "options": ["--exclude", "--extend-exclude", "--skip-gitignore"]},
    skip.option_group,
    {
        "name": "Other",
        "options": [
            "--target-version",
            "--language",
            "--reruns",
            "--verbose",
            "--color",
            "--output",
            "--version",
            "--help",
        ],
    },
]

if RICH_PRESENT:
    click.rich_click.USE_RICH_MARKUP = True
    click.rich_click.USE_MARKDOWN = True
    click.rich_click.FORCE_TERMINAL = None  # workaround rich_click trying to force color in GitHub Actions
    click.rich_click.STYLE_OPTION = "bold sky_blue3"
    click.rich_click.STYLE_SWITCH = "bold sky_blue3"
    click.rich_click.STYLE_METAVAR = "bold white"
    click.rich_click.STYLE_OPTION_DEFAULT = "grey37"
    click.rich_click.STYLE_OPTIONS_PANEL_BORDER = "grey66"
    click.rich_click.STYLE_USAGE = "magenta"
    click.rich_click.OPTION_GROUPS = {
        "robotidy": CLI_OPTIONS_LIST,
        "python -m robotidy": CLI_OPTIONS_LIST,
    }


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


def complete_transformers(ctx, param, incomplete):
    transformers = load_transformers(TransformConfigMap([], [], []), allow_disabled=True, target_version=None)
    # TODO if name:config in incomplete, complete config? check parameters and args
    return [tr.name for tr in transformers if tr.name.startswith(incomplete)]


@click.version_option(version=version.__version__, prog_name="robotidy")
@click.pass_context
@decorators.catch_exceptions
def cli(ctx: click.Context, **kwargs):
    """
    Robotidy is a tool for formatting Robot Framework source code.
    Full documentation available at <https://robotidy.readthedocs.io> .
    """
    cli_config = RawConfig.from_cli(ctx=ctx, **kwargs)
    global_config = config_module.MainConfig(cli_config)
    global_config.validate_src_is_required()
    if global_config.default.list_transformers:
        print_transformers_list(global_config)
        sys.exit(0)
    if global_config.default.describe_transformer is not None:
        return_code = print_description(
            global_config.default.describe_transformer, global_config.default.target_version
        )
        sys.exit(return_code)
    if global_config.default.generate_config:
        generate_config(global_config)
        sys.exit(0)
    tidy = app.Robotidy(global_config)
    status = tidy.transform_files()
    sys.exit(status)
