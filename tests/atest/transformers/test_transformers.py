import filecmp
from difflib import unified_diff
from pathlib import Path
from typing import List, Optional
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from robotidy.cli import cli
from robotidy.utils import decorate_diff_with_color


def save_tmp_model(self, model):
    """ Decorator that disables default robotidy save to file mechanism and replace with mocked one.
    That way we can save output to 'actual' directory for easy comparison with expected files.  """
    path = Path(Path(__file__).parent, 'actual', Path(model.source).name)
    print(path)
    model.save(output=path)


def run_tidy(
        transformer_name: str,
        args: List[str] = None,
        sources: List[str] = None,
        exit_code: int = 0
):
    runner = CliRunner()
    arguments = args if args is not None else []
    if sources is None:
        paths = [str(Path(Path(__file__).parent, transformer_name, 'source'))]
    else:
        paths = [str(Path(Path(__file__).parent, transformer_name, 'source', source)) for source in sources]
    cmd = arguments + paths
    result = runner.invoke(cli, cmd)
    if result.exit_code != exit_code:
        print(result.output)
        raise AssertionError(f'robotidy exit code: {result.exit_code} does not match expected: {exit_code}')
    return result


def compare_file(transformer_name: str, actual_name: str, expected_name: str = None):
    if expected_name is None:
        expected_name = actual_name
    expected = Path(Path(__file__).parent, transformer_name, 'expected', expected_name)
    actual = Path(Path(__file__).parent, 'actual', actual_name)
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


def run_tidy_and_compare(transformer_name: str, sources: List[str],
                         expected: Optional[List[str]] = None, config: str = ''):
    if expected is None:
        expected = sources
    run_tidy(
        transformer_name,
        args=f'--transform {transformer_name}{config}'.split(),
        sources=sources
    )
    for source_path, expected_path in zip(sources, expected):
        compare_file(transformer_name, source_path, expected_path)


@patch('robotidy.app.Robotidy.save_model', new=save_tmp_model)
class TestDiscardEmptySections:
    TRANSFORMER_NAME = 'DiscardEmptySections'

    def test_removes_empty_sections(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, sources=['removes_empty_sections.robot'])

    def test_removes_empty_sections_except_comments(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            sources=['removes_empty_sections.robot'],
            expected=['removes_empty_sections_except_comments.robot'],
            config=':allow_only_comments=True'
        )

    def test_remove_selected_empty_node(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            sources=['removes_empty_sections.robot'],
            expected=['removes_selected_empty_section.robot'],
            config=' --startline 17 --endline 18'
        )


@patch('robotidy.app.Robotidy.save_model', new=save_tmp_model)
class TestReplaceRunKeywordIf:
    TRANSFORMER_NAME = 'ReplaceRunKeywordIf'

    def test_run_keyword_if_replaced_selected(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            sources=['tests.robot'],
            expected=['tests_selected.robot'],
            config=' --startline 18 --endline 20'
        )

    def test_run_keyword_if_replaced(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, sources=['tests.robot'])

    def test_invalid_data(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, sources=['invalid_data.robot'])

    def test_golden_file(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, sources=['golden.robot'])


@patch('robotidy.app.Robotidy.save_model', new=save_tmp_model)
class TestAssignmentNormalizer:
    TRANSFORMER_NAME = 'AssignmentNormalizer'

    @pytest.mark.parametrize('filename', [
        'common_remove.robot',
        'common_equal_sign.robot',
        'common_space_and_equal_sign.robot'
    ])
    def test_autodetect(self, filename):
        run_tidy_and_compare(self.TRANSFORMER_NAME, sources=[filename])

    def test_remove(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            sources=['tests.robot'],
            expected=['remove.robot'],
            config=':equal_sign_type=remove'
        )

    def test_add_equal_sign(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            sources=['tests.robot'],
            expected=['equal_sign.robot'],
            config=':equal_sign_type=equal_sign'
        )

    def test_add_space_and_equal_sign(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            sources=['tests.robot'],
            expected=['space_and_equal_sign.robot'],
            config=':equal_sign_type=space_and_equal_sign'
        )

    def test_invalid_equal_sign_type(self):
        result = run_tidy(
            self.TRANSFORMER_NAME,
            args=f'--transform {self.TRANSFORMER_NAME}:equal_sign_type=='.split(),
            sources=['tests.robot'],
            exit_code=1
        )
        expected_output = "Importing 'robotidy.transformers.AssignmentNormalizer' failed: " \
                          "Creating instance failed: BadOptionUsage: Invalid configurable value: = " \
                          "for equal_sign_type for AssignmentNormalizer transformer. " \
                          "Possible values:\n    remove\n    equal_sign\n    space_and_equal_sign"
        assert expected_output in str(result.exception)


@patch('robotidy.app.Robotidy.save_model', new=save_tmp_model)
class TestExternalTransformer:
    def test_external_transformer_works(self):
        transformer_path = Path(Path(__file__).parent, 'ExternalTransformer', 'ExternalTransformer.py')
        run_tidy(
            'ExternalTransformer',
            args=f'--transform {transformer_path}:param=2'.split(),
            sources=['tests.robot']
        )
        compare_file('ExternalTransformer', 'tests.robot')


@patch('robotidy.app.Robotidy.save_model', new=save_tmp_model)
class TestNormalizeSettingName:
    TRANSFORMER_NAME = 'NormalizeSettingName'

    def test_normalize_setting_name(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, sources=['tests.robot'])

    def test_normalize_setting_name_selected(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            sources=['tests.robot'],
            expected=['selected.robot'],
            config=' --startline 12 --endline 15'
        )


@patch('robotidy.app.Robotidy.save_model', new=save_tmp_model)
class TestNormalizeSectionHeaderName:
    TRANSFORMER_NAME = 'NormalizeSectionHeaderName'

    def test_normalize_names(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, sources=['tests.robot'])

    def test_uppercase_names(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            sources=['tests.robot'],
            expected=['uppercase.robot'],
            config=':uppercase=True'
        )

    def test_normalize_names_selected(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            sources=['tests.robot'],
            expected=['selected.robot'],
            config=' --startline 5 --endline 6'
        )


@patch('robotidy.app.Robotidy.save_model', new=save_tmp_model)
class TestNormalizeNewLines:
    TRANSFORMER_NAME = 'NormalizeNewLines'

    def test_normalize_new_lines(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, sources=['tests.robot'])

    def test_normalize_new_lines_three_lines_after_section(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            sources=['tests.robot'],
            expected=['tests_three_lines_section.robot'],
            config=':section_lines=3'
        )

    def test_normalize_new_lines_two_lines_keywords(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            sources=['tests.robot'],
            expected=['tests_two_lines_keywords.robot'],
            config=':keyword_lines=2'
        )

    def test_templated_tests(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, sources=['templated_tests.robot'])

    def test_templated_tests_separated(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            sources=['templated_tests.robot'],
            expected=['templated_tests_with_1_line.robot'],
            config=':separate_templated_tests=True'
        )

    @pytest.mark.parametrize('lines_at_the_end', [0, 1])
    def test_test_case_last(self, lines_at_the_end):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            sources=[f'test_case_last_{lines_at_the_end}_lines.robot'],
            expected=['test_case_last.robot']
        )


@patch('robotidy.app.Robotidy.save_model', new=save_tmp_model)
class TestSplitTooLongLine:
    TRANSFORMER_NAME = 'SplitTooLongLine'

    def test_split_too_long_lines(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            sources=['tests.robot'],
            expected=['feed_until_line_length.robot'],
            config=':line_length=80:split_on_every_arg=False -s 4'
        )

    def test_split_too_long_lines_split_on_every_arg(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            sources=['tests.robot'],
            expected=['split_on_every_arg.robot'],
            config=':line_length=80:split_on_every_arg=True -s 4'
        )

    def test_split_lines_with_multiple_assignments(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            sources=['multiple_assignments.robot'],
            expected=['multiple_assignments_until_line_length.robot'],
            config=':line_length=80:split_on_every_arg=False -s 4'
        )

    def test_split_lines_with_multiple_assignments_on_every_arg(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            sources=['multiple_assignments.robot'],
            expected=['multiple_assignments_on_every_arg.robot'],
            config=':line_length=80:split_on_every_arg=True -s 4'
        )


@patch('robotidy.app.Robotidy.save_model', new=save_tmp_model)
class TestAlignVariablesSection:
    TRANSFORMER_NAME = 'AlignVariablesSection'

    def test_align_variables(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, sources=['tests.robot'])

    def test_align_with_optional_equal_signs(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, sources=['optional_equal_sign.robot'])

    def test_align_with_long_comment(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, sources=['long_comment.robot'])

    def test_align_selected_whole(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            sources=['align_selected.robot'],
            expected=['align_selected_whole.robot'],
            config=' --startline 5 --endline 17'
        )

    def test_align_selected_part(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            sources=['align_selected.robot'],
            expected=['align_selected_part.robot'],
            config=' --startline 10 --endline 12'
        )


@patch('robotidy.app.Robotidy.save_model', new=save_tmp_model)
class TestAlignSettingsSection:
    TRANSFORMER_NAME = 'AlignSettingsSection'

    def test_align_settings(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            sources=['test.robot'],
            expected=['all_columns.robot']
        )

    def test_align_two_columns(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            sources=['test.robot'],
            expected=['two_columns.robot'],
            config=':up_to_column=2'
        )

    def test_align_three_columns(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            sources=['test.robot'],
            expected=['three_columns.robot'],
            config=':up_to_column=3'
        )

    def test_align_selected_whole(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            sources=['test.robot'],
            expected=['selected_whole.robot'],
            config=' --startline 1 --endline 25'
        )

    def test_align_selected_part(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            sources=['test.robot'],
            expected=['selected_part.robot'],
            config=' --startline 9 --endline 14'
        )

    def test_empty_lines_inside_statement(self):
        # bug from #75
        run_tidy_and_compare(self.TRANSFORMER_NAME, sources=['empty_lines.robot'])


@patch('robotidy.app.Robotidy.save_model', new=save_tmp_model)
class TestSmartSortKeywords:
    TRANSFORMER_NAME = 'SmartSortKeywords'

    def test_ci_sort(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            sources=['sort_input.robot'],
            expected=['sort_ci.robot'],
            config=":ignore_other_underscore=False"
        )

    def test_ci_ilu(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            sources=['sort_input.robot'],
            expected=['sort_ci_ilu.robot'],
            config=":ignore_leading_underscore=True:ignore_other_underscore=False"
        )

    def test_ci_iou(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            sources=['sort_input.robot'],
            expected=['sort_ci_iou.robot']
        )

    def test_ci_ilu_iou(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            sources=['sort_input.robot'],
            expected=['sort_ci_ilu_iou.robot'],
            config=":ignore_leading_underscore=True"
        )

    def test_ilu_iou(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            sources=['sort_input.robot'],
            expected=['sort_ilu_iou.robot'],
            config=":case_insensitive=False:ignore_leading_underscore=True"
        )

    def test_iou(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            sources=['sort_input.robot'],
            expected=['sort_iou.robot'],
            config=":case_insensitive=False"
        )

    def test_ilu(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            sources=['sort_input.robot'],
            expected=['sort_ilu.robot'],
            config=":case_insensitive=False:ignore_leading_underscore=True:ignore_other_underscore=False"
        )

    def test_(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            sources=['sort_input.robot'],
            expected=['sort_.robot'],
            config=":case_insensitive=False:ignore_other_underscore=False"
        )

    def test_empty_section(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, sources=['empty_before_fist_keyword.robot'])

    def test_multiple_sections(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, sources=['multiple_sections.robot'])


@patch('robotidy.app.Robotidy.save_model', new=save_tmp_model)
class TestMergeAndOrderSections:
    TRANSFORMER_NAME = 'MergeAndOrderSections'

    def test_merging_and_ordering(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, sources=['tests.robot'])

    def test_both_test_and_task(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, sources=['both_test_and_task.robot'])

    def test_multiple_header_comments(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, sources=['multiple_header_comments.robot'])

    def test_nested_blocks(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, sources=['nested_blocks.robot'])

    def test_nested_block_for(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, sources=['nested_block_for.robot'])

    def test_empty_section(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, sources=['empty_section.robot'])

    def test_parsing_error(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, sources=['parsing_error.robot'])


@patch('robotidy.app.Robotidy.save_model', new=save_tmp_model)
class TestRemoveEmptySettings:
    TRANSFORMER_NAME = 'RemoveEmptySettings'

    def test_remove_empty_settings(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, sources=['test.robot'])
