import filecmp
import shutil
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
from robotidy.utils.misc import decorate_diff_with_color

VERSION_MATRIX = {"ReplaceReturns": 5, "InlineIf": 5, "ReplaceBreakContinue": 5, "Translate": 6, "ReplaceWithVAR": 7}
ROBOT_VERSION = version.parse(RF_VERSION)


def display_file_diff(expected, actual):
    print("\nExpected file after transforming does not match actual")
    with open(expected, encoding="utf-8") as f, open(actual, encoding="utf-8") as f2:
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
    TRANSFORMER_NAME: str = "PLACEHOLDER"
    TRANSFORMERS_DIR = Path(__file__).parent / "transformers"

    def compare(
        self,
        source: str,
        not_modified: bool = False,
        expected: Optional[str] = None,
        config: str = "",
        target_version: Optional[str] = None,
        run_all: bool = False,
    ):
        """
        Compare actual (source) and expected files. If expected filename is not provided it's assumed to be the same
        as source.

        Use not_modified flag if the content of the file shouldn't be modified by transformer.
        """
        if expected is None:
            expected = source
        if run_all:
            run_cmd = config
        else:
            run_cmd = f"--transform {self.TRANSFORMER_NAME}{config}"
        self.run_tidy(args=run_cmd.split(), source=source, not_modified=not_modified, target_version=target_version)
        if not not_modified:
            self.compare_file(source, expected)

    def run_tidy(
        self,
        args: List[str] = None,
        source: str = None,
        exit_code: int = 0,
        not_modified: bool = False,
        target_version: Optional[str] = None,
    ):
        if not self.enabled_in_version(target_version):
            pytest.skip(f"Test enabled only for RF {target_version}")
        runner = CliRunner()
        output_path = str(self.TRANSFORMERS_DIR / "actual" / source)
        arguments = ["--output", output_path]
        if not_modified:
            arguments.extend(["--check", "--overwrite"])
        if args is not None:
            arguments += args
        if source is None:
            source_path = str(self.TRANSFORMERS_DIR / self.TRANSFORMER_NAME / "source")
        else:
            source_path = str(self.TRANSFORMERS_DIR / self.TRANSFORMER_NAME / "source" / source)
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
        expected = self.TRANSFORMERS_DIR / self.TRANSFORMER_NAME / "expected" / expected_name
        actual = self.TRANSFORMERS_DIR / "actual" / actual_name
        if not filecmp.cmp(expected, actual):
            display_file_diff(expected, actual)
            pytest.fail(f"File {actual_name} is not same as expected")

    def enabled_in_version(self, target_version: Optional[str]) -> bool:
        if target_version and ROBOT_VERSION not in SpecifierSet(target_version, prereleases=True):
            return False
        if self.TRANSFORMER_NAME in VERSION_MATRIX:
            return ROBOT_VERSION.major >= VERSION_MATRIX[self.TRANSFORMER_NAME]
        return True


class MultipleConfigsTest:
    TEST_DIR: str = "PLACEHOLDER"
    ROOT_DIR = Path(__file__).parent / "configuration_files"

    def run_tidy(self, tmpdir, args: List[str] = None, exit_code: int = 0, not_modified: bool = False):
        runner = CliRunner()
        temporary_dir = tmpdir / self.TEST_DIR
        shutil.copytree(self.ROOT_DIR / self.TEST_DIR / "source", temporary_dir)
        arguments = []
        if not_modified:
            arguments.extend(["--check", "--overwrite"])
        if args is not None:
            arguments += args
        cmd = arguments + [str(temporary_dir)]
        result = runner.invoke(cli, cmd)
        if result.exit_code != exit_code:
            raise AssertionError(
                f"robotidy exit code: {result.exit_code} does not match expected: {exit_code}. "
                f"Exception description: {result.exception}"
            )

    def compare_files(self, tmpdir, expected_dir: str):
        expected = self.ROOT_DIR / self.TEST_DIR / expected_dir
        actual = Path(tmpdir / self.TEST_DIR)
        if compare_file_tree(expected, actual):
            pytest.fail(f"Files in expected file tree: {expected} and the actual are not the same.")


def compare_file_tree(actual_dir: Path, expected_dir: Path) -> bool:
    error = False
    actual_files = {x.name: x for x in actual_dir.iterdir()}
    expected_files = {x.name: x for x in expected_dir.iterdir()}
    for exp_file_name, exp_file in expected_files.items():
        if exp_file_name in actual_files:
            if exp_file.is_dir():
                error = compare_file_tree(actual_files[exp_file_name], exp_file) or error
            elif not filecmp.cmp(exp_file, actual_files[exp_file_name]):
                error = True
                display_file_diff(exp_file, actual_files[exp_file_name])
        else:
            error = True
            print(f"File {exp_file} not found in the actual files.")
    for actual_file_name, actual_file in actual_files.items():
        if actual_file_name not in expected_files:
            error = True
            print(f"Extra {actual_file} found in the actual files.")
    return error
