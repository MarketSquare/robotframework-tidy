from pathlib import Path

import pytest

from robotidy.exceptions import InvalidParameterValueError

from .. import TransformerAcceptanceTest


class TestGenerateDocumentation(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "GenerateDocumentation"

    def test_transformer(self):
        self.compare(source="test.robot")

    def test_transformer_overwrite(self):
        self.compare(source="test.robot", expected="overwrite.robot", config=":overwrite=True")

    def test_template_with_defaults(self):
        template_path = Path(__file__).parent / "source" / "template_with_defaults.txt"
        args = ["--transform", f"{self.TRANSFORMER_NAME};doc_template={template_path}"]
        source = "test.robot"
        self.run_tidy(args=args, source=source)
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
