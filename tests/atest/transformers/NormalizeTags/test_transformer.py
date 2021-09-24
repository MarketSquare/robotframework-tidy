from .. import run_tidy_and_compare


class TestNormalizeTags:
    TRANSFORMER_NAME = 'NormalizeTags'

    def test_lowercase(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source='tests.robot', expected='lowercase.robot',
                             config=f':case=lowercase')

    def test_uppercase(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source='tests.robot', expected='uppercase.robot',
                             config=f':case=uppercase')

    def test_titlecase(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source='tests.robot', expected='titlecase.robot',
                             config=f':case=titlecase')
