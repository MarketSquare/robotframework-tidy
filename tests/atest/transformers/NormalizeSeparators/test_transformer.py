from .. import run_tidy_and_compare


class TestNormalizeSeparators:
    TRANSFORMER_NAME = 'NormalizeSeparators'

    def test_normalize_separators(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source='test.robot')

    def test_normalize_with_8_spaces(self):
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source='test.robot',
            expected='test_8spaces.robot',
            config=' --spacecount 8'
        )

    def test_pipes(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source='pipes.robot')
