from unittest.mock import patch
from pathlib import Path

from unittest.mock import MagicMock, Mock
import pytest
from click import FileError, NoSuchOption

from .utils import run_tidy, save_tmp_model
from robotidy.cli import (
    find_project_root,
    read_pyproject_config,
    read_config
)
from robotidy.utils import node_within_lines
from robotidy.transformers import load_transformers
from robotidy.transformers.AlignSettingsSection import AlignSettingsSection
from robotidy.transformers.ReplaceRunKeywordIf import ReplaceRunKeywordIf
from robotidy.transformers.SmartSortKeywords import SmartSortKeywords
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

    @pytest.mark.parametrize('name, similar', [
        ('NotExisting', ''),
        ('AlignSettings', ' Did you mean:\n    AlignSettingsSection'),
        ('align', ' Did you mean:\n    AlignSettingsSection\n    AlignVariablesSection'),
        ('splittoolongline', ' Did you mean:\n    SplitTooLongLine'),
        ('AssignmentNormalizer', ' Did you mean:\n    NormalizeAssignments')
    ])
    def test_not_existing_transformer(self, name, similar):
        expected_output = f"Importing transformer '{name}' failed. " \
                          f"Verify if correct name or configuration was provided.{similar}"
        args = f'--transform {name} --transform MissingTransformer --transform DiscardEmptySections -'.split()
        result = run_tidy(args, exit_code=1)
        assert expected_output in str(result.exception)

    def test_transformer_order(self):
        order_1 = ['NormalizeSeparators', 'OrderSettings']
        order_2 = ['OrderSettings', 'NormalizeSeparators']
        transformers_1 = load_transformers([(transf, []) for transf in order_1], {})
        transformers_2 = load_transformers([(transf, []) for transf in order_2], {})
        assert all(t1.__class__.__name__ == t2.__class__.__name__ for t1, t2 in zip(transformers_1, transformers_2))

    def test_transformer_force_order(self):
        # default_order = ['NormalizeSeparators', 'OrderSettings']
        custom_order = ['OrderSettings', 'NormalizeSeparators']
        transformers = load_transformers([(transf, []) for transf in custom_order], {}, force_order=True)
        assert all(t1.__class__.__name__ == t2 for t1, t2 in zip(transformers, custom_order))

    # TODO: raise exception if kwarg does not match
    # def test_not_existing_configurable(self):
    #     expected_output = "Usage: cli [OPTIONS] [PATH(S)]\n\n" \
    #                       "Error: Invalid configurable name: 'missing_configurable' for transformer: " \
    #                       "'DiscardEmptySections'\n"
    #
    #     args = '--transform DiscardEmptySections:allow_only_commentss=True -'.split()
    #     result = run_tidy(args, exit_code=2)
    #     assert expected_output == result.output

    def test_invalid_configurable_usage(self):
        expected_output = "Importing transformer 'DiscardEmptySections=allow_only_comments=False' failed. " \
                          "Verify if correct name or configuration was provided"
        args = '--transform DiscardEmptySections=allow_only_comments=False -'.split()
        result = run_tidy(args, exit_code=1)
        assert expected_output in str(result.exception)

    def test_too_many_arguments_for_transform(self):
        expected_output = "not enough values to unpack (expected 2, got 1)"
        args = '--transform DiscardEmptySections:allow_only_comments:False -'.split()
        result = run_tidy(args, exit_code=1)
        assert str(result.exception) == expected_output

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
        """ robotidy.toml follows the same format as pyproject starting from 1.2.0 """
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
        config = read_pyproject_config(config_path)
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
                'DiscardEmptySections:allow_only_comments=False',
                'OrderSettings: keyword_before = documentation,tags,timeout,arguments'
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
                'DiscardEmptySections:allow_only_comments=False',
                'OrderSettings: keyword_before = documentation,tags,timeout,arguments'
            ]
        }
        config_path = str(Path(Path(__file__).parent, 'testdata', 'only_pyproject'))
        ctx_mock = MagicMock()
        ctx_mock.params = {'src': [config_path]}
        ctx_mock.command.params = None
        param_mock = Mock()
        read_config(ctx_mock, param_mock, value=None)
        assert ctx_mock.default_map == expected_parsed_config

    def test_read_invalid_config(self):
        config_path = str(Path(Path(__file__).parent, 'testdata', 'invalid_pyproject', 'pyproject.toml'))
        with pytest.raises(FileError) as err:
            read_pyproject_config(config_path)
        assert 'Error reading configuration file: ' in str(err)

    @pytest.mark.parametrize('option, correct', [
        ('confgure', 'configure'),
        ('idontexist', None)
    ])
    def test_read_invalid_option_config(self, option, correct):
        config_path = str(Path(Path(__file__).parent, 'testdata', 'invalid_options_config', f'pyproject_{option}.toml'))
        ctx_mock = MagicMock()
        param_mock = MagicMock()
        with pytest.raises(NoSuchOption) as err:
            read_config(ctx_mock, param_mock, config_path)
        similar = '' if correct is None else f' Did you mean {correct}'
        assert f'no such option: {option}{similar}'

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
        ctx_mock.command.params = None
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
        ctx_mock.command.params = None
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

    @pytest.mark.parametrize('flag', ['--list', '-l'])
    def test_list_transformers(self, flag):
        result = run_tidy([flag])
        assert 'To see detailed docs run --desc <transformer_name> or --desc all. Transformers with (disabled) tag \n' \
               'are executed only when selected explicitly with --transform. Available transformers:\n'\
               in result.output
        assert 'ReplaceRunKeywordIf\n' in result.output
        assert 'SmartSortKeywords (disabled)\n' in result.output  # this transformer is disabled by default
        assert 'Available transformers:\n\nAlignSettingsSection\n' in result.output  # assert order

    @pytest.mark.parametrize('flag', ['--desc', '-d'])
    @pytest.mark.parametrize('name, expected_doc', [
        ('ReplaceRunKeywordIf', ReplaceRunKeywordIf.__doc__.replace('::', ':').replace("``", "'")),
        ('SmartSortKeywords', SmartSortKeywords.__doc__.replace('::', ':').replace("``", "'"))
    ])
    def test_describe_transformer(self, flag, name, expected_doc):
        not_expected_doc = AlignSettingsSection.__doc__.replace('::', ':').replace("``", "'")
        result = run_tidy([flag, name])
        assert expected_doc in result.output
        assert not_expected_doc not in result.output

    def test_describe_transformer_all(self):
        expected_doc = ReplaceRunKeywordIf.__doc__.replace('::', ':').replace("``", "'")
        expected_doc2 = AlignSettingsSection.__doc__.replace('::', ':').replace("``", "'")
        result = run_tidy(['--desc', 'all'])
        assert expected_doc in result.output
        assert expected_doc2 in result.output

    @pytest.mark.parametrize('name, similar', [
        ('NotExisting', ''),
        ('AlignSettings', ' Did you mean:\n    AlignSettingsSection'),
        ('align', ' Did you mean:\n    AlignSettingsSection\n    AlignVariablesSection'),
        ('splittoolongline', ' Did you mean:\n    SplitTooLongLine'),
        ('AssignmentNormalizer', ' Did you mean:\n    NormalizeAssignments')
    ])
    def test_describe_invalid_transformer(self, name, similar):
        expected_output = f"Transformer with the name '{name}' does not exist.{similar}"
        args = f'--desc {name} -'.split()
        result = run_tidy(args, exit_code=1)
        assert expected_output in str(result.output)

    @pytest.mark.parametrize('flag', ['--help', '-h'])
    def test_help(self, flag):
        result = run_tidy([flag])
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
