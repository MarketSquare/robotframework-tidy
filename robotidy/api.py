"""
Methods for transforming Robot Framework ast model programmatically.
"""
from pathlib import Path
from typing import Optional

from robotidy import app, disablers, files
from robotidy.config import MainConfig, RawConfig


def get_robotidy(src: str, output: Optional[str], ignore_git_dir: bool = False, **kwargs):
    config = RawConfig(**kwargs)
    config_file = files.find_source_config_file(Path(src), ignore_git_dir)
    if config_file:
        config_dict = files.read_pyproject_config(config_file)
        config = config.from_config_file(config_dict, config_file)
    global_config = MainConfig(config)
    global_config.default_loaded.overwrite = False
    global_config.default_loaded.show_diff = False
    global_config.default_loaded.verbose = False
    global_config.default_loaded.check = False
    global_config.default_loaded.force_order = False
    global_config.default_loaded.output = output
    return app.Robotidy(global_config)


def transform_model(model, root_dir: str, output: Optional[str] = None, **kwargs) -> Optional[str]:
    """
    :param model: The model to be transformed.
    :param root_dir: Root directory. Configuration file is searched based
    on this directory or one of its parents.
    :param output: Path where transformed model should be saved
    :param kwargs: Default values for global formatting parameters
    such as ``spacecount``, ``startline`` and ``endline``.
    :return: The transformed model converted to string or None if no transformation took place.
    """
    robotidy_class = get_robotidy(root_dir, output, **kwargs)
    disabler_finder = disablers.RegisterDisablers(
        robotidy_class.config.formatting.start_line, robotidy_class.config.formatting.end_line
    )
    disabler_finder.visit(model)
    if disabler_finder.file_disabled:
        return None
    diff, _, new_model = robotidy_class.transform(model, disabler_finder.disablers)
    if not diff:
        return None
    return new_model.text
