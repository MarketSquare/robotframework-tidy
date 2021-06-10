from unittest.mock import patch
from pathlib import Path

from unittest.mock import MagicMock, Mock
import pytest
from click import FileError

from .utils import run_tidy, save_tmp_model
from robotidy.cli import (
    find_project_root,
    read_robotidy_config,
    read_pyproject_config,
    read_config
)
from robotidy.utils import node_within_lines
from robotidy.transformers import load_transformers
from robotidy.transformers.ReplaceRunKeywordIf import ReplaceRunKeywordIf
from robotidy.version import __version__


@patch('robotidy.app.Robotidy.save_model', new=save_tmp_model)
class TestCli:
    @pytest.mark.parametrize('src', [
        None,
        ['.']
    ])
    def test_nested_src(self, src):
        """ It should recursively search and find `testdata/test.robot` file """
        run_tidy(src)

    def test_not_existing_transformer(self):
        expected_output = "Importing 'NotExisting' failed: ModuleNotFoundError: No module named 'NotExisting'"
        args = '--transform NotExisting --transform MissingTransformer --transform DiscardEmptySections -'.split()
        result = run_tidy(args, exit_code=1)
        assert expected_output in str(result.exception)

    # TODO: raise exception if kwarg does not match
    # def test_not_existing_configurable(self):
    #     expected_output = "Usage: cli [OPTIONS] [PATH(S)]\n\n" \
    #                       "Error: Invalid configurable name: 'missing_configurable' for transformer: " \
    #                       "'DiscardEmptySections'\n"
    #
    #     args = '--transform DiscardEmptySections:allow_only_commentss=True'.split()
    #     result = run_tidy(args, exit_code=2)
    #     assert expected_output == result.output

    def test_invalid_configurable_usage(self):
        expected_output = "Importing 'DiscardEmptySections=allow_only_comments=False' failed: " \
                          "ModuleNotFoundError: No module named 'DiscardEmptySections=allow_only_comments=False'"
        args = '--transform DiscardEmptySections=allow_only_comments=False -'.split()
        result = run_tidy(args, exit_code=1)
        assert expected_output in str(result.exception)

    def test_too_many_arguments_for_transform(self):
        expected_output = "not enough values to unpack (expected 2, got 1)"
        args = '--transform DiscardEmptySections:allow_only_comments:False -'.split()
        result = run_tidy(args, exit_code=1)
        assert expected_output == str(result.exception)

    # def test_invalid_argument_type_for_transform(self):
    #     expected_output = "Importing 'robotidy.transformers.DiscardEmptySections' failed:  'DicardEmptySection'"
    #     args = '--transform DiscardEmptySections:allow_only_comments=true'.split()
    #     result = run_tidy(args, exit_code=1)
    #     assert expected_output == str(result.exception)

    def test_find_project_root_from_src(self):
        src = Path(Path(__file__).parent, 'testdata', 'nested', 'test.robot')
        path = find_project_root([src])
        assert path == Path(Path(__file__).parent, 'testdata')

    def test_read_robotidy_config(self):
        expected_config = {
            'overwrite': False,
            'diff': False,
            'spacecount': 4,
            'transform': [
                'DiscardEmptySections:allow_only_comments=True',
                'ReplaceRunKeywordIf'
            ]
        }
        config_path = str(Path(Path(__file__).parent, 'testdata', 'robotidy.toml'))
        config = read_robotidy_config(config_path)
        assert config == expected_config

    def test_read_pyproject_config(self):
        expected_parsed_config = {
            'overwrite': False,
            'diff': False,
            'startline': 10,
            'endline': 20,
            'transform': [
                'DiscardEmptySections:allow_only_comments=True',
                'SplitTooLongLine'
            ],
            'configure': [
                'DiscardEmptySections:allow_only_comments=False'
            ]
        }
        config_path = str(Path(Path(__file__).parent, 'testdata', 'only_pyproject', 'pyproject.toml'))
        config = read_pyproject_config(config_path)
        assert config == expected_parsed_config

    def test_read_pyproject_config_e2e(self):
        expected_parsed_config = {
            'overwrite': 'False',
            'diff': 'False',
            'startline': '10',
            'endline': '20',
            'transform': [
                'DiscardEmptySections:allow_only_comments=True',
                'SplitTooLongLine'
            ],
            'configure': [
                'DiscardEmptySections:allow_only_comments=False'
            ]
        }
        config_path = str(Path(Path(__file__).parent, 'testdata', 'only_pyproject'))
        ctx_mock = MagicMock()
        ctx_mock.params = {'src': [config_path]}
        param_mock = Mock()
        read_config(ctx_mock, param_mock, value=None)
        assert ctx_mock.default_map == expected_parsed_config

    def test_read_invalid_config(self):
        config_path = str(Path(Path(__file__).parent, 'testdata', 'invalid_pyproject', 'pyproject.toml'))
        with pytest.raises(FileError) as err:
            read_pyproject_config(config_path)
        assert 'Error reading configuration file: ' in str(err)

    def test_read_config_from_param(self):
        expected_parsed_config = {
            'overwrite': 'False',
            'diff': 'False',
            'spacecount': '4',
            'transform': [
                'DiscardEmptySections:allow_only_comments=True',
                'ReplaceRunKeywordIf'
            ]
        }
        config_path = str(Path(Path(__file__).parent, 'testdata', 'robotidy.toml'))
        ctx_mock = MagicMock()
        param_mock = Mock()
        read_config(ctx_mock, param_mock, config_path)
        assert ctx_mock.default_map == expected_parsed_config

    def test_read_config_without_param(self):
        expected_parsed_config = {
            'overwrite': 'False',
            'diff': 'False',
            'spacecount': '4',
            'transform': [
                'DiscardEmptySections:allow_only_comments=True',
                'ReplaceRunKeywordIf'
            ]
        }
        config_path = str(Path(Path(__file__).parent, 'testdata', 'robotidy.toml'))
        ctx_mock = MagicMock()
        ctx_mock.params = {'src': [config_path]}
        param_mock = Mock()
        read_config(ctx_mock, param_mock, value=None)
        assert ctx_mock.default_map == expected_parsed_config

    @pytest.mark.parametrize('node_start, node_end, start_line, end_line, expected', [
        (15, 30, 15, None, True),
        (15, 30, 15, 30, True),
        (14, 30, 15, 30, False),
        (15, 31, 15, 30, False),
        (15, 30, None, 30, True),
        (15, 30, None, None, True)
    ])
    def test_skip_node_start_end_line_setting(self, node_start, node_end, start_line, end_line, expected):
        assert node_within_lines(node_start, node_end, start_line, end_line) == expected

    def test_list_transformers(self):
        result = run_tidy(['--list-transformers'])
        assert 'Run --desc <transformer_name> to get more details. Transformers:' in result.output
        assert 'ReplaceRunKeywordIf\n' in result.output
        result = run_tidy(['--list'])
        assert 'Run --desc <transformer_name> to get more details. Transformers:' in result.output
        assert 'ReplaceRunKeywordIf\n' in result.output
        result = run_tidy(['-l'])
        assert 'Run --desc <transformer_name> to get more details. Transformers:' in result.output
        assert 'ReplaceRunKeywordIf\n' in result.output

    def test_describe_transformer(self):
        expected_doc = ReplaceRunKeywordIf.__doc__.replace('::', ':').replace("``", "'")
        result = run_tidy(['--describe-transformer', 'ReplaceRunKeywordIf'])
        assert expected_doc in result.output
        result = run_tidy(['--desc', 'ReplaceRunKeywordIf'])
        assert expected_doc in result.output
        result = run_tidy(['-d', 'ReplaceRunKeywordIf'])
        assert expected_doc in result.output

    def test_help(self):
        result = run_tidy(['--help'])
        assert f'Version: {__version__}' in result.output

    @pytest.mark.parametrize('source, return_status', [
        ('golden.robot', 0),
        ('not_golden.robot', 1)
    ])
    def test_check(self, source, return_status):
        source = Path(Path(__file__).parent, 'testdata', 'check', source)
        run_tidy(
            ['--check', '--overwrite', '--transform', 'NormalizeSectionHeaderName', str(source)],
            exit_code=return_status
        )

    def test_diff(self):
        source = Path(Path(__file__).parent, 'testdata', 'check', 'not_golden.robot')
        result = run_tidy(['--diff', '--no-overwrite', '--transform', 'NormalizeSectionHeaderName', str(source)])
        assert "*** settings ***" in result.output
        assert "*** Settings ***" in result.output

    def test_disabled_transformer(self):
        transformers = load_transformers(None, {})
        assert all(transformer.__class__.__name__ != 'SmartSortKeywords' for transformer in transformers)

    def test_enable_disable_transformer(self):
        transformers = load_transformers([('SmartSortKeywords', [])], {})
        assert transformers[0].__class__.__name__ == 'SmartSortKeywords'

    def test_configure_transformer(self):
        transformers = load_transformers(
            None,
            {'AlignVariablesSection': ['up_to_column=4']}
        )
        transformers_not_configured = load_transformers(None, {})
        assert len(transformers) == len(transformers_not_configured)
        for transformer in transformers:
            if transformer.__class__.__name__ == 'AlignVariablesSection':
                assert transformer.up_to_column + 1 == 4

    def test_configure_transformer_overwrite(self):
        transformers = load_transformers(
            [('AlignVariablesSection', ['up_to_column=3'])],
            {'AlignVariablesSection': ['up_to_column=4']}
        )
        assert transformers[0].up_to_column + 1 == 4
