from unittest.mock import patch
from pathlib import Path

from unittest.mock import MagicMock, Mock
import pytest

from .utils import run_tidy, save_tmp_model
from robotidy.cli import (
    find_project_root,
    find_config,
    parse_config,
    read_config
)
from robotidy.utils import node_within_lines


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
        expected_output = 'Usage: cli [OPTIONS] [PATH(S)]\n\n' \
                          'Error: Failed to load all requested transformers. Make sure you provided correct name. ' \
                          'Missing:\nMissingTransformer\nNotExisting\n'
        args = '--transform NotExisting --transform MissingTransformer --transform DiscardEmptySections'.split()
        result = run_tidy(args, exit_code=2)
        assert expected_output == result.output

    def test_not_existing_configurable(self):
        expected_output = "Usage: cli [OPTIONS] [PATH(S)]\n\n" \
                          "Error: Invalid configurable name: 'missing_configurable' for transformer: " \
                          "'DiscardEmptySections'\n"

        args = '--transform DiscardEmptySections:missing_configurable=5'.split()
        result = run_tidy(args, exit_code=2)
        assert expected_output == result.output

    @pytest.mark.parametrize('configurable', [
        ':allow_only_comments',
        ':allow_only_comments:False',
        '=allow_only_comments=False'
    ])
    def test_invalid_configurable_usage(self, configurable):
        name = 'DiscardEmptySections' + configurable.split(':')[0]
        expected_output = f'Invalid {name} transformer configuration. ' \
                          f'Parameters should be provided in format name=value, delimited by :'
        args = ('--transform DiscardEmptySections' + configurable).split()
        result = run_tidy(args, exit_code=1)
        assert expected_output == str(result.exception)

    def test_find_project_root_from_src(self):
        src = Path(Path(__file__).parent, 'testdata', 'nested', 'test.robot')
        path = find_project_root([src])
        assert path == Path(Path(__file__).parent, 'testdata')

    def test_find_config_toml_from_src(self):
        src = Path(Path(__file__).parent, 'testdata', 'nested', 'test.robot')
        path = find_config([src])
        assert path == str(Path(Path(__file__).parent, 'testdata', 'robotidy.toml'))

    def test_parse_config(self):
        expected_config = {
            'main': {
                'overwrite': False,
                'diff': False,
                'spacecount': 4
            },
            'transformers': {
                'DiscardEmptySections': {
                    'allow_only_comments': True
                },
                'ReplaceRunKeywordIf': {}
            }
        }
        config_path = str(Path(Path(__file__).parent, 'testdata', 'robotidy.toml'))
        config = parse_config(config_path)
        assert config == expected_config

    def test_read_config_from_param(self):
        expected_parsed_config = {
            'overwrite': False,
            'diff': False,
            'spacecount': 4,
            'transform': [
                'DiscardEmptySections:allow_only_comments=True',
                'ReplaceRunKeywordIf'
            ]
        }
        config_path = str(Path(Path(__file__).parent, 'testdata', 'robotidy.toml'))
        ctx_mock = MagicMock()
        param_mock = Mock()
        config = read_config(ctx_mock, param_mock, config_path)
        assert ctx_mock.default_map == expected_parsed_config
        assert config == config_path

    def test_read_config_without_param(self):
        expected_parsed_config = {
            'overwrite': False,
            'diff': False,
            'spacecount': 4,
            'transform': [
                'DiscardEmptySections:allow_only_comments=True',
                'ReplaceRunKeywordIf'
            ]
        }
        config_path = str(Path(Path(__file__).parent, 'testdata', 'robotidy.toml'))
        ctx_mock = MagicMock()
        ctx_mock.params = {'src': [config_path]}
        param_mock = Mock()
        config = read_config(ctx_mock, param_mock, value=None)
        assert ctx_mock.default_map == expected_parsed_config
        assert config == config_path

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

    def test_loading_from_stdin(self, monkeypatch):
        input_file = '*** Settings ***\nLibrary  SomeLib\n\n\n' \
                     '*** Variables ***\n\n\n\n' \
                     '*** Keywords ***\nKeyword\n    Keyword1 ${arg}\n'
        expected_output = '*** Settings ***\nLibrary  SomeLib\n\n\n' \
                          '*** Keywords ***\nKeyword\n    Keyword1 ${arg}\n\n'
        monkeypatch.setattr("robotidy.app.Robotidy.load_from_stdin", lambda x: input_file)
        args = '--transform DiscardEmptySections -'.split()
        result = run_tidy(args)
        assert result.output == expected_output
