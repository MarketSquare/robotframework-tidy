import pytest

from .. import run_tidy_and_compare


class TestRemoveEmptySettings:
    TRANSFORMER_NAME = "RemoveEmptySettings"

    @pytest.mark.parametrize("source", ["empty", "overwritten"])
    @pytest.mark.parametrize("work_mode", ["always", "overwritten_ok"])
    @pytest.mark.parametrize("more_explicit", ["more_explicit", "no_explicit"])
    def test_modes(self, source, work_mode, more_explicit):
        work_mode_config = "" if work_mode == "overwritten_ok" else f":work_mode={work_mode}"
        more_explicit_config = "" if more_explicit == "more_explicit" else ":more_explicit=False"
        run_tidy_and_compare(
            self.TRANSFORMER_NAME,
            source=f"{source}.robot",
            expected=f"{source}_{work_mode}_{more_explicit}.robot",
            config=f"{work_mode_config}{more_explicit_config}",
        )
