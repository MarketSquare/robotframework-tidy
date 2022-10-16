import filecmp
from difflib import unified_diff
from pathlib import Path
from typing import List, Optional

import pytest
from click.testing import CliRunner
from packaging import version
from packaging.specifiers import SpecifierSet
from rich.console import Console
from robot.version import VERSION as RF_VERSION

from robotidy.cli import cli
from robotidy.utils import decorate_diff_with_color

VERSION_MATRIX = {
    "ReplaceReturns": 5,
    "InlineIf": 5,
    "ReplaceBreakContinue": 5,
}
ROBOT_VERSION = version.parse(RF_VERSION)


def display_file_diff(expected, actual):
    print("\nExpected file after transforming does not match actual")
    with open(expected) as f, open(actual) as f2:
        expected_lines = f.readlines()
        actual_lines = f2.readlines()
    lines = [
        line
        for line in unified_diff(
            expected_lines, actual_lines, fromfile=f"expected: {expected}\t", tofile=f"actual: {actual}\t"
        )
    ]
    colorized_output = decorate_diff_with_color(lines)
    console = Console(color_system="windows", width=400)
    for line in colorized_output:
        console.print(line, end="", highlight=False)


class TransformerAcceptanceTest:
    TRANSFORMER_NAME: str = "DUMMY"

    def compare(
        self,
        source: str,
        not_modified: bool = False,
        expected: Optional[str] = None,
        config: str = "",
        target_version: Optional[str] = None,
    ):
        """
        Compare actual (source) and expected files. If expected filename is not provided it's assumed to be the same
        as source.

        Use not_modified flag if the content of the file shouldn't be modified by transformer.
        """
        if not self.enabled_in_version(target_version):
            pytest.skip(f"Test enabled only for RF {target_version}")
        if expected is None:
            expected = source
        self.run_tidy(
            args=f"--transform {self.TRANSFORMER_NAME}{config}".split(), source=source, not_modified=not_modified
        )
        if not not_modified:
            self.compare_file(source, expected)

    def run_tidy(self, args: List[str] = None, source: str = None, exit_code: int = 0, not_modified: bool = False):
        runner = CliRunner()
        output_path = str(Path(Path(__file__).parent, "actual", source))
        arguments = ["--output", output_path]
        if not_modified:
            arguments.extend(["--check", "--overwrite"])
        if args is not None:
            arguments += args
        if source is None:
            source_path = str(Path(Path(__file__).parent, self.TRANSFORMER_NAME, "source"))
        else:
            source_path = str(Path(Path(__file__).parent, self.TRANSFORMER_NAME, "source", source))
        cmd = arguments + [source_path]
        result = runner.invoke(cli, cmd)
        if result.exit_code != exit_code:
            raise AssertionError(
                f"robotidy exit code: {result.exit_code} does not match expected: {exit_code}. "
                f"Exception description: {result.exception}"
            )
        return result

    def compare_file(self, actual_name: str, expected_name: str = None):
        if expected_name is None:
            expected_name = actual_name
        expected = Path(Path(__file__).parent, self.TRANSFORMER_NAME, "expected", expected_name)
        actual = Path(Path(__file__).parent, "actual", actual_name)
        if not filecmp.cmp(expected, actual):
            display_file_diff(expected, actual)
            pytest.fail(f"File {actual_name} is not same as expected")

    def enabled_in_version(self, target_version: Optional[str]) -> bool:
        if target_version and ROBOT_VERSION not in SpecifierSet(target_version, prereleases=True):
            return False
        if self.TRANSFORMER_NAME in VERSION_MATRIX:
            return ROBOT_VERSION.major >= VERSION_MATRIX[self.TRANSFORMER_NAME]
        return True
