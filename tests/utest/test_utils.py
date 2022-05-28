import os
from pathlib import Path

import pytest

from robotidy.app import Robotidy
from robotidy.utils import (
    decorate_diff_with_color,
    split_args_from_name_or_path,
    GlobalFormattingConfig,
    ROBOT_VERSION,
)


@pytest.fixture
def app():
    formatting_config = GlobalFormattingConfig(
        space_count=4, indent=4, line_sep="auto", start_line=None, separator="space", end_line=None, line_length=120
    )
    return Robotidy(
        transformers=[],
        transformers_config=[],
        src=(".",),
        exclude=None,
        extend_exclude=None,
        ignore_gitignore=False,
        overwrite=False,
        show_diff=False,
        formatting_config=formatting_config,
        verbose=False,
        check=False,
        output=None,
        force_order=False,
        target_version=ROBOT_VERSION.major,
        color=True,
    )


class TestUtils:
    def test_not_changed_lines_not_colorized(self):
        lines = ["this is one line\n", "and another\n"]
        output = decorate_diff_with_color(lines)
        assert output == "".join(lines)

    def test_diff_lines_colorized(self):
        lines = [
            "+++ color category\n",
            "--- color category\n",
            "+ new line\n",
            "- removed line\n",
            "@@ line numbers\n",
            "no diff line\n",
            "signs + in the - middle @@ +++ ---\n",
        ]
        expected_lines = [
            "\033[1m+++ color category\n\033[0m",
            "\033[1m--- color category\n\033[0m",
            "\033[32m+ new line\n\033[0m",
            "\033[31m- removed line\n\033[0m",
            "\033[36m@@ line numbers\n\033[0m",
            "no diff line\n",
            "signs + in the - middle @@ +++ ---\n",
        ]
        output = decorate_diff_with_color(lines)
        assert output == "".join(expected_lines)

    @pytest.mark.parametrize(
        "name_or_path, expected_name, expected_args",
        [
            ("DiscardEmptySections", "DiscardEmptySections", []),
            ("DiscardEmptySections:allow_only_comments=True", "DiscardEmptySections", ["allow_only_comments=True"]),
            ("DiscardEmptySections;allow_only_comments=True", "DiscardEmptySections", ["allow_only_comments=True"]),
            (
                "DiscardEmptySections;allow_only_comments=True:my_var=1",
                "DiscardEmptySections",
                ["allow_only_comments=True:my_var=1"],
            ),
            (r"C:\path\to\module\transformer:my_variable=1", r"C:\path\to\module\transformer", ["my_variable=1"]),
            (__file__, __file__, []),
        ],
    )
    def test_split_args_from_name_or_path(self, name_or_path, expected_name, expected_args):
        name, args = split_args_from_name_or_path(name_or_path)
        assert name == expected_name
        assert args == expected_args

    @pytest.mark.parametrize(
        "line_sep, source_file, expected",
        [
            ("auto", "lf.robot", "\n"),
            ("auto", "crlf.robot", "\r\n"),
            ("auto", "cr.robot", "\r"),
            ("auto", "crlf_mixed.robot", "\n"),
            ("auto", "empty.robot", os.linesep),
            ("native", "lf.robot", os.linesep),
            ("native", "crlf.robot", os.linesep),
            ("windows", "lf.robot", "\r\n"),
            ("windows", "crlf.robot", "\r\n"),
            ("unix", "lf.robot", "\n"),
            ("unix", "crlf.robot", "\n"),
        ],
    )
    def test_get_line_ending(self, line_sep, source_file, expected, app):
        source = str(Path(__file__).parent / "testdata" / "auto_line_sep" / source_file)
        app.formatting_config = GlobalFormattingConfig(
            space_count=4,
            indent=4,
            line_sep=line_sep,
            start_line=None,
            separator="space",
            end_line=None,
            line_length=120,
        )
        assert app.get_line_ending(source) == expected
