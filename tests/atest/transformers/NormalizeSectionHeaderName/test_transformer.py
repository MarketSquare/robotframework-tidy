from .. import run_tidy_and_compare


class TestNormalizeSectionHeaderName:
    TRANSFORMER_NAME = 'NormalizeSectionHeaderName'

    def test_normalize_names(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source='tests.robot')

    def test_uppercase_names(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source='tests.robot',
            expected='uppercase.robot',
            config=':uppercase=True'
        )

    def test_normalize_names_selected(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source='tests.robot',
            expected='selected.robot',
            config=' --startline 5 --endline 6'
        )
