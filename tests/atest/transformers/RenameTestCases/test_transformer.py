from .. import run_tidy_and_compare


class TestRenameTestCases:
    TRANSFORMER_NAME = 'RenameTestCases'

    def test_transformer(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source='test.robot', expected='test.robot')
