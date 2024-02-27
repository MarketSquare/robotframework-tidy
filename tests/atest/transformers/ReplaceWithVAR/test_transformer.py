from tests.atest import TransformerAcceptanceTest


class TestReplaceWithVAR(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "ReplaceWithVAR"

    def test_transformer(self):
        self.compare(source="test.robot", expected="test.robot")

    def test_explicit_local(self):
        self.compare(source="test.robot", expected="explicit_local.robot", config=":explicit_local=True")

    def test_replace_catenate_disabled(self):
        self.compare(source="test.robot", expected="replace_catenate_false.robot", config=":replace_catenate=False")

    def test_replace_create_dictionary_disabled(self):
        self.compare(
            source="test.robot",
            expected="replace_create_dictionary_false.robot",
            config=":replace_create_dictionary=False",
        )

    def test_replace_create_list_disabled(self):
        self.compare(
            source="test.robot", expected="replace_create_list_false.robot", config=":replace_create_list=False"
        )

    def test_replace_set_variable_if_disabled(self):
        self.compare(
            source="test.robot", expected="replace_set_variable_if_false.robot", config=":replace_set_variable_if=False"
        )

    def test_invalid_inline_if(self):
        self.compare(source="invalid_inline_if.robot", not_modified=True)

    def test_too_long(self):
        self.compare(source="too_long.robot", config=f"-c {self.TRANSFORMER_NAME}:enabled=True", run_all=True)
