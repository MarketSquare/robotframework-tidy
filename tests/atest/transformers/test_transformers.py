import filecmp
from difflib import unified_diff
from pathlib import Path
from typing import List
from unittest.mock import patch

from click.testing import CliRunner

from robotidy.cli import cli
from robotidy.utils import decorate_diff_with_color


def save_tmp_model(self, model):
    path = Path('actual', Path(model.source).name)
    model.save(output=path)


def run_tidy(transformer_name: str, args: List[str] = None, sources: List[str] = None, exit_code: int = 0):
    runner = CliRunner()
    arguments = args if args is not None else []
    if sources is None:
        paths = [str(Path(transformer_name, 'source'))]
    else:
        paths = [str(Path(transformer_name, 'source', source)) for source in sources]
    cmd = arguments + paths
    result = runner.invoke(cli, cmd)
    assert result.exit_code == exit_code
    return result


def compare_file(transformer_name: str, actual_name: str, expected_name: str = None):
    if expected_name is None:
        expected_name = actual_name
    expected = Path(transformer_name, 'expected', expected_name)
    actual = Path('actual', actual_name)
    if not filecmp.cmp(expected, actual):
        display_file_diff(expected, actual)
        raise AssertionError(f'File {actual_name} is not same as expected')


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


@patch('robotidy.app.Robotidy.save_model', new=save_tmp_model)
class TestDiscardEmptySections:
    TRANSFORMER_NAME = 'DiscardEmptySections'

    def test_removes_empty_sections(self):
        run_tidy(
            self.TRANSFORMER_NAME,
            args='--transform DiscardEmptySections'.split(),
            sources=['removes_empty_sections.robot']
        )
        compare_file(self.TRANSFORMER_NAME, 'removes_empty_sections.robot')

    def test_removes_empty_sections_except_comments(self):
        run_tidy(
            self.TRANSFORMER_NAME,
            args='--transform DiscardEmptySections:allow_only_comments=True'.split(),
            sources=['removes_empty_sections.robot']
        )
        # we're using the same actual name (since we used the same source) but different expected
        # that's because our expected changed with modified transformation configuration
        compare_file(
            self.TRANSFORMER_NAME,
            'removes_empty_sections.robot',
            'removes_empty_sections_except_comments.robot'
        )
