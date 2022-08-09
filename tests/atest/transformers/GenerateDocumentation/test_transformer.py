from pathlib import Path

from .. import TransformerAcceptanceTest


class TestGenerateDocumentation(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "GenerateDocumentation"

    def test_transformer(self):
        self.compare(source="test.robot", expected="test.robot")

    def test_template_with_defaults2(self):
        template_path = Path(__file__).parent / "source" / "template_with_defaults.txt"
        args = ["--transform", f"{self.TRANSFORMER_NAME}", "--documentation-template", template_path]
        source = "test.robot"
        self.run_tidy(
            args=args, source=source
        )
        self.compare_file(source, "template_with_defaults.robot")

    def test_template_with_defaults(self):
        template_path = Path(__file__).parent / "source" / "template_with_defaults.txt"
        args = ["--transform", f"{self.TRANSFORMER_NAME};doc_template={template_path}"]
        source = "test.robot"
        self.run_tidy(
            args=args, source=source
        )
        self.compare_file(source, "template_with_defaults.robot")
