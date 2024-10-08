from tests.atest import TransformerAcceptanceTest


class TestOrderTags(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "OrderTags"

    def test_order_tags_default(self):
        self.compare(source="tests.robot", expected="default.robot")

    def test_case_insensitive(self):
        self.compare(
            source="tests.robot",
            expected="case_insensitive.robot",
            config=":case_sensitive=False:reverse=False",
        )

    def test_case_sensitive(self):
        self.compare(
            source="tests.robot",
            expected="case_sensitive.robot",
            config=":case_sensitive=True:reverse=False",
        )

    def test_insensitive_reverse(self):
        self.compare(
            source="tests.robot",
            expected="case_insensitive_reverse.robot",
            config=":case_sensitive=False:reverse=True",
        )

    def test_case_sensitive_reverse(self):
        self.compare(
            source="tests.robot",
            expected="case_sensitive_reverse.robot",
            config=":case_sensitive=True:reverse=True",
        )

    def test_default_tags_false(self):
        self.compare(
            source="tests.robot",
            expected="default_tags_false.robot",
            config=":case_sensitive=False:reverse=False:default_tags=False",
        )

    def test_force_tags_false(self):
        self.compare(
            source="tests.robot",
            expected="force_tags_false.robot",
            config=":case_sensitive=False:reverse=False:force_tags=False",
        )

    def test_disablers(self):
        self.compare(source="disablers.robot", not_modified=True)

    def test_test_tags(self):
        self.compare(source="test_tags.robot", target_version=">=6")
