import pytest
from robotidy.utils import (
    decorate_diff_with_color,
    split_args_from_name_or_path
)


class TestUtils:
    def test_not_changed_lines_not_colorized(self):
        lines = [
            'this is one line',
            'and another'
        ]
        output = decorate_diff_with_color(lines)
        assert output == '\n'.join(lines)

    def test_diff_lines_colorized(self):
        lines = [
            '+++ color category',
            '--- color category',
            '+ new line',
            '- removed line',
            '@@ line numbers',
            'no diff line',
            'signs + in the - middle @@ +++ ---'
        ]
        expected_lines = [
            '\033[1;37m+++ color category\033[0m',
            '\033[1;37m--- color category\033[0m',
            '\033[32m+ new line\033[0m',
            '\033[31m- removed line\033[0m',
            '\033[36m@@ line numbers\033[0m',
            'no diff line',
            'signs + in the - middle @@ +++ ---'
        ]
        output = decorate_diff_with_color(lines)
        assert output == '\n'.join(expected_lines)

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
