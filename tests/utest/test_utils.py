import pytest
from robotidy.utils import (
    decorate_diff_with_color,
    split_args_from_name_or_path
)


class TestUtils:
    def test_not_changed_lines_not_colorized(self):
        lines = [
            'this is one line\n',
            'and another\n'
        ]
        output = decorate_diff_with_color(lines)
        assert output == ''.join(lines)

    def test_diff_lines_colorized(self):
        lines = [
            '+++ color category\n',
            '--- color category\n',
            '+ new line\n',
            '- removed line\n',
            '@@ line numbers\n',
            'no diff line\n',
            'signs + in the - middle @@ +++ ---\n'
        ]
        expected_lines = [
            '\033[1m+++ color category\n\033[0m',
            '\033[1m--- color category\n\033[0m',
            '\033[32m+ new line\n\033[0m',
            '\033[31m- removed line\n\033[0m',
            '\033[36m@@ line numbers\n\033[0m',
            'no diff line\n',
            'signs + in the - middle @@ +++ ---\n'
        ]
        output = decorate_diff_with_color(lines)
        assert output == ''.join(expected_lines)

    @pytest.mark.parametrize('name_or_path, expected_name, expected_args', [
        ('DiscardEmptySections', 'DiscardEmptySections', []),
        ('DiscardEmptySections:allow_only_comments=True', 'DiscardEmptySections', ['allow_only_comments=True']),
        ('DiscardEmptySections;allow_only_comments=True', 'DiscardEmptySections', ['allow_only_comments=True']),
        ('DiscardEmptySections;allow_only_comments=True:my_var=1', 'DiscardEmptySections', [
            'allow_only_comments=True:my_var=1']),
        (r'C:\path\to\module\transformer:my_variable=1', r'C:\path\to\module\transformer', ['my_variable=1']),
        (__file__, __file__, [])
    ])
    def test_split_args_from_name_or_path(self, name_or_path, expected_name, expected_args):
        name, args = split_args_from_name_or_path(name_or_path)
        assert name == expected_name
        assert args == expected_args
