from pathlib import Path

from tests.atest import TransformerAcceptanceTest


def get_relative_path(abs_path: Path) -> Path:
    cwd = Path.cwd()
    return abs_path.relative_to(cwd)


class TestGenerateDocumentation(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "GenerateDocumentation"

    def test_transformer(self):
        self.compare(source="test.robot", target_version=">=5")

    def test_transformer_rf4(self):
        self.compare(source="test.robot", expected="test_rf4.robot", target_version="<=4")

    def test_transformer_overwrite(self):
        self.compare(source="test.robot", expected="overwrite.robot", config=":overwrite=True", target_version=">=5")

    def test_template_with_defaults(self):
        template_path = Path(__file__).parent / "source" / "template_with_defaults.txt"
        args = ["--transform", f"{self.TRANSFORMER_NAME};doc_template={template_path}"]
        source = "test.robot"
        self.run_tidy(args=args, source=source, target_version=">=5")
        self.compare_file(source, "template_with_defaults.robot")

    def test_template_with_defaults_relative_path(self):
        template_path = Path(__file__).parent / "source" / "template_with_defaults.txt"
        rel_template_path = get_relative_path(template_path)
        args = ["--transform", f"{self.TRANSFORMER_NAME}:doc_template={rel_template_path}"]
        source = "test.robot"
        self.run_tidy(args=args, source=source, target_version=">=5")
        self.compare_file(source, "template_with_defaults.robot")

    def test_invalid_template_path(self):
        template_path = "invalid/path.jinja"
        args = [
            "-c",
            f"{self.TRANSFORMER_NAME}:enabled=True",
            "-c",
            f"{self.TRANSFORMER_NAME}:doc_template={template_path}",
        ]
        result = self.run_tidy(
            args=args,
            source="test.robot",
            exit_code=1,
        )
        expected_output = (
            f"Error: {self.TRANSFORMER_NAME}: Invalid 'doc_template' parameter value: '{template_path}'. "
            f"The template path does not exist or cannot be found.\n"
        )
        assert expected_output == result.output

    def test_invalid_template(self):
        template_path = Path(__file__).parent / "source" / "invalid_template.jinja"
        rel_template_path = get_relative_path(template_path)
        args = ["--transform", f"{self.TRANSFORMER_NAME}:doc_template={rel_template_path}"]
        source = "test.robot"
        result = self.run_tidy(args=args, source=source, exit_code=1)
        expected_output = (
            f"Error: {self.TRANSFORMER_NAME}: Invalid 'doc_template' parameter value: 'template content'. "
            f"Failed to load the template: Unexpected end of template. Jinja was looking for the "
            f"following tags: 'endfor' or 'else'. The innermost block that needs to be closed is 'for'.\n"
        )
        assert expected_output == result.output
