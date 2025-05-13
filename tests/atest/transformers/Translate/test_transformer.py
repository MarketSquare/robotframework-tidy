import pytest

from robotidy.utils.misc import ROBOT_VERSION
from tests.atest import TransformerAcceptanceTest


class TestTranslate(TransformerAcceptanceTest):
    TRANSFORMER_NAME = "Translate"

    @pytest.mark.parametrize("source_lang", [["en"], ["pl"], ["pl", "de"]])
    @pytest.mark.parametrize("dest_lang", ["de", "en", "pl"])
    def test_translation(self, source_lang, dest_lang):
        config = ""
        if dest_lang != "en":
            config += f":language={dest_lang}"
        if source_lang != ["en"]:
            config += f" --language {','.join(source_lang)}"
        source_file = "_and_".join(source_lang) + ".robot"
        not_modified = source_lang == [dest_lang]
        self.compare(config=config, source=source_file, expected=f"{dest_lang}.robot", not_modified=not_modified)

    def test_recognize_language_header(self):
        self.compare(config=":language=en", source="pl_language_header.robot", expected="en_with_pl_header.robot")

    def test_bdd(self):
        self.compare(
            config=":translate_bdd=True:language=pl --language pl",
            source="bdd/en_and_pl.robot",
            expected="bdd/pl.robot",
        )
        self.compare(
            config=":translate_bdd=True:language=uk --language pl",
            source="bdd/en_and_pl.robot",
            expected="bdd/uk.robot",
        )

    def test_bdd_alternative(self):
        self.compare(
            config=":translate_bdd=True:language=pl:given_alternative=Zakładając --language pl",
            source="bdd/en_and_pl.robot",
            expected="bdd/pl_alternative.robot",
        )

    def test_bdd_alternative_invalid(self):
        if ROBOT_VERSION.major < 6:
            pytest.skip("Test enabled only for RF 6.0+")
        result = self.run_tidy(
            args=f"--transform {self.TRANSFORMER_NAME}:translate_bdd=True:language=pl:but_alternative=chyba"
            f" --language pl".split(),
            source="bdd/en_and_pl.robot",
            exit_code=1,
        )
        expected_output = (
            f"Error: {self.TRANSFORMER_NAME}: Invalid 'but_alternative' parameter value: 'chyba'. "
            "Provided BDD keyword alternative does not exist in the destination language. Select one of: Ale\n"
        )
        assert expected_output in result.output

    def test_add_language_header(self):
        config = ":language=pl:add_language_header=True"
        self.compare(
            config=config,
            source="add_lang_header/empty.robot",
            expected="add_lang_header/empty.robot",
            not_modified=True,
        )
        self.compare(
            config=config,
            source="add_lang_header/comment_section.robot",
            expected="add_lang_header/comment_section.robot",
        )
        self.compare(
            config=config,
            source="add_lang_header/diff_lang_header.robot",
            expected="add_lang_header/diff_lang_header.robot",
        )
        self.compare(
            config=config,
            source="add_lang_header/no_lang_header.robot",
            expected="add_lang_header/no_lang_header.robot",
        )
        self.compare(
            config=":add_language_header=True",
            source="add_lang_header/en_header.robot",
            expected="add_lang_header/en_header.robot",
        )
