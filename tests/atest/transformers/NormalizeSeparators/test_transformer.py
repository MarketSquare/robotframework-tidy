import pytest

from .. import TransformerAcceptanceTest


class TestNormalizeSeparators(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "NormalizeSeparators"

    def test_normalize_separators(self):
        self.compare(source="test.robot")

    def test_normalize_with_8_spaces(self):
        self.compare(source="test.robot", expected="test_8spaces.robot", config=" --spacecount 8")

    def test_pipes(self):
        self.compare(source="pipes.robot")

    @pytest.mark.parametrize(
        "sections",
        ["", "comments,settings,variables", "comment,keywords", "comments,settings,variable,keywords,testcases"],
    )
    def test_disable_section(self, sections):
        if sections:
            self.compare(
                source="test.robot", expected=sections.replace(",", "_") + ".robot", config=f":sections={sections}"
            )
        else:
            self.compare(source="test.robot", not_modified=True, config=f":sections={sections}")

    def test_configure_invalid_section(self):
        result = self.run_tidy(
            args=f"--transform {self.TRANSFORMER_NAME}:sections=settings,invalid".split(),
            source="test.robot",
            exit_code=1,
        )
        expected_output = (
            f"Error: {self.TRANSFORMER_NAME}: Invalid 'sections' parameter value: 'settings,invalid'. "
            f"Sections to be transformed should be provided in comma separated list with valid section names:\n"
            f"['comments', 'keywords', 'settings', 'testcases', 'variables']\n"
        )
        assert expected_output == result.output

    def test_rf5_syntax(self):
        self.compare(source="rf5_syntax.robot", target_version=5)

    def test_disablers(self):
        self.compare(source="disablers.robot", not_modified=True)

    def test_skip_documentation_default(self):
        self.compare(source="test.robot", config=":skip_documentation=False")

    def test_skip_documentation(self):
        self.compare(source="test.robot", expected="skip_documentation.robot", config=":skip_documentation=True")
