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

    def test_continuation_indent(self):
        self.compare(source="continuation_indent.robot", config=" --continuation-indent 4 --indent 4 --spacecount 2")

    @pytest.mark.parametrize("indent", [2, 4])
    @pytest.mark.parametrize("spaces", [2, 4])
    def test_inline_if(self, spaces, indent):
        not_modified = indent == 4 and spaces == 4
        self.compare(
            source="inline_if.robot",
            expected=f"inline_if_{indent}indent_{spaces}spaces.robot",
            config=f" --spacecount {spaces} --indent {indent}",
            not_modified=not_modified,
            target_version=5,
        )

    def test_skip_keyword_call(self):
        self.compare(
            source="test.robot",
            expected="test_skip_keyword.robot",
            config=":skip_keyword_call_pattern=(?i)should\sbe\sequal",
        )

    def test_file_with_pipes_bug390(self):
        self.compare(source="bug390.robot")
