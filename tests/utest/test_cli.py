from unittest.mock import patch

import pytest

from .utils import run_tidy, save_tmp_model


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
