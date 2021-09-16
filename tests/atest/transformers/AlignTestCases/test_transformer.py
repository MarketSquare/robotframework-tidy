import pytest

from .. import run_tidy_and_compare


class TestAlignTestCases:
    TRANSFORMER_NAME = 'AlignTestCases'

    @pytest.mark.parametrize('source', [
        'test.robot',
        'no_header_col.robot',
        'for_loops.robot',
        'with_settings.robot',
        'templated_for_loops.robot',
        'templated_for_loops_and_without.robot'
    ])
    def test_transformer(self, source):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source=source, expected=source)

    def test_only_with_headers(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source='no_header_col.robot',
            expected='no_header_col_only_headers.robot',
            config=':only_with_headers=True'
        )
