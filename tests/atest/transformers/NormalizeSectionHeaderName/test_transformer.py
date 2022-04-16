import pytest

from .. import TransformerAcceptanceTest


class TestNormalizeSectionHeaderName(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "NormalizeSectionHeaderName"

    def test_normalize_names(self):
        self.compare(source="tests.robot")

    def test_uppercase_names(self):
        self.compare(source="tests.robot", expected="uppercase.robot", config=":uppercase=True")

    def test_normalize_names_selected(self):
        self.compare(source="tests.robot", expected="selected.robot", config=" --startline 5 --endline 6")

    @pytest.mark.parametrize("source", ["task.robot", "task2.robot"])
    def test_tasks(self, source):
        self.compare(source=source)

    def test_disablers(self):
        self.compare(source="disablers.robot", not_modified=True)
