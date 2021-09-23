from .. import run_tidy_and_compare


class TestOrderTags:
    TRANSFORMER_NAME = 'OrderTags'

    def test_order_tags_default(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME, source='tests.robot', expected='default.robot')

    def test_case_insensitive(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME,
                             source='tests.robot',
                             expected='case_insensitive.robot',
                             config=f':case_sensitive=False:reverse=False'
                             )

    def test_case_sensitive(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME,
                             source='tests.robot',
                             expected='case_sensitive.robot',
                             config=f':case_sensitive=True:reverse=False'
                             )

    def test_insensitive_reverse(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME,
                             source='tests.robot',
                             expected='case_insensitive_reverse.robot',
                             config=f':case_sensitive=False:reverse=True'
                             )

    def test_case_sensitive_reverse(self):
        run_tidy_and_compare(self.TRANSFORMER_NAME,
                             source='tests.robot',
                             expected='case_sensitive_reverse.robot',
                             config=f':case_sensitive=True:reverse=True'
                             )