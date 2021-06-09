import filecmp
from difflib import unified_diff
from pathlib import Path
from typing import List, Optional

from click.testing import CliRunner
import pytest

from robotidy.cli import cli
from robotidy.utils import decorate_diff_with_color


def run_tidy(
        transformer_name: str,
        args: List[str] = None,
        source: str = None,
        exit_code: int = 0
):
    runner = CliRunner()
    output_path = str(Path(Path(__file__).parent, 'actual', source))
    arguments = ['--output', output_path]
    if args is not None:
        arguments += args
    if source is None:
        source_path = str(Path(Path(__file__).parent, transformer_name, 'source'))
    else:
        source_path = str(Path(Path(__file__).parent, transformer_name, 'source', source))
    cmd = arguments + [source_path]
    result = runner.invoke(cli, cmd)
    if result.exit_code != exit_code:
        raise AssertionError(f'robotidy exit code: {result.exit_code} does not match expected: {exit_code}. '
                             f'Exception description: {result.exception}')
    return result


def compare_file(transformer_name: str, actual_name: str, expected_name: str = None):
    if expected_name is None:
        expected_name = actual_name
    expected = Path(Path(__file__).parent, transformer_name, 'expected', expected_name)
    actual = Path(Path(__file__).parent, 'actual', actual_name)
    if not filecmp.cmp(expected, actual):
        display_file_diff(expected, actual)
        pytest.fail(f'File {actual_name} is not same as expected')


def display_file_diff(expected, actual):
    print('\nExpected file after transforming does not match actual')
    with open(expected) as f, open(actual) as f2:
        expected_lines = f.readlines()
        actual_lines = f2.readlines()
    lines = [line for line in unified_diff(expected_lines,
                                           actual_lines,
                                           fromfile=f'expected: {expected}\t', tofile=f'actual: {actual}\t')
             ]
    colorized_output = decorate_diff_with_color(lines)
    print(colorized_output)


def run_tidy_and_compare(transformer_name: str, source: str,
                         expected: Optional[str] = None, config: str = ''):
    if expected is None:
        expected = source
    run_tidy(
        transformer_name,
        args=f'--transform {transformer_name}{config}'.split(),
        source=source
    )
    compare_file(transformer_name, source, expected)
