from robotidy.utils import decorate_diff_with_color


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
