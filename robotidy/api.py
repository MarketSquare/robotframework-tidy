"""
Methods for transforming Robot Framework ast model programmatically.
"""
from typing import Dict, List, Optional

from robotidy import app, disablers, files, skip, transformers, utils
from robotidy.config import Config, FormattingConfig
from robotidy.transformers import TransformConfig, TransformConfigMap


def get_skip_config(config):
    # TODO: Improve it
    skip_comments = config.get("skip_comments", False)
    skip_documentation = config.get("skip_documentation", False)
    skip_return_values = config.get("skip_return_values", False)
    skip_keyword_call = config.get("skip_keyword_call", [])
    skip_keyword_call_pattern = config.get("skip_keyword_call_pattern", [])
    skip_settings = config.get("skip_settings", False)
    skip_arguments = config.get("skip_arguments", False)
    skip_setup = config.get("skip_setup", False)
    skip_teardown = config.get("skip_teardown", False)
    skip_template = config.get("skip_template", False)
    skip_timeout = config.get("skip_timeout", False)
    skip_return = config.get("skip_return", False)
    skip_tags = config.get("skip_tags", False)
    skip_sections = config.get("skip_sections", "")
    skip_block_comments = config.get("skip_block_comments", False)
    return skip.SkipConfig(
        documentation=skip_documentation,
        return_values=skip_return_values,
        keyword_call=skip_keyword_call,
        keyword_call_pattern=skip_keyword_call_pattern,
        settings=skip_settings,
        arguments=skip_arguments,
        setup=skip_setup,
        teardown=skip_teardown,
        template=skip_template,
        timeout=skip_timeout,
        return_statement=skip_return,
        tags=skip_tags,
        comments=skip_comments,
        block_comments=skip_block_comments,
        sections=skip_sections,
    )


def get_formatting_config(config, kwargs):
    space_count = kwargs.get("spacecount", None) or int(config.get("spacecount", 4))
    indent = kwargs.get("indent", None) or int(config.get("indent", space_count))
    cont_indent = kwargs.get("continuation_indent", None) or int(config.get("continuation_indent", space_count))
    formatting_config = FormattingConfig(
        space_count=space_count,
        indent=indent,
        continuation_indent=cont_indent,
        separator=kwargs.get("separator", None) or config.get("separator", "space"),
        line_sep=config.get("lineseparator", "native"),
        start_line=kwargs.get("startline", None) or int(config["startline"]) if "startline" in config else None,
        end_line=kwargs.get("endline", None) or int(config["endline"]) if "endline" in config else None,
        line_length=kwargs.get("line_length", None) or int(config.get("line_length", 120)),
    )
    return formatting_config


def get_robotidy(src: str, output: Optional[str], **kwargs):
    def convert_transformers_config(
        param_name: str,
        config: Dict,
        force_included: bool = False,
        custom_transformer: bool = False,
        is_config: bool = False,
    ) -> List[TransformConfig]:
        return [
            TransformConfig(
                tr, force_include=force_included, custom_transformer=custom_transformer, is_config=is_config
            )
            for tr in config.get(param_name, ())
        ]

    # TODO Refactor - Config should be read in one place both for API and CLI
    # TODO Remove kwargs usage - other SDKs are not using this feature
    config = files.find_and_read_config((src,))
    config = {k: str(v) if not isinstance(v, (list, dict)) else v for k, v in config.items()}
    transformer_list = convert_transformers_config("transform", config, force_included=True)
    custom_transformers = convert_transformers_config("load-transformers", config, custom_transformer=True)
    configurations = convert_transformers_config("configure", config, is_config=True)
    transformer_config = TransformConfigMap(transformer_list, custom_transformers, configurations)
    formatting_config = get_formatting_config(config, kwargs)
    exclude = config.get("exclude", None)
    extend_exclude = config.get("extend_exclude", None)
    reruns = config.get("reruns", 0)
    config_directory = config.get("config_directory", None)
    exclude = utils.validate_regex(exclude if exclude is not None else files.DEFAULT_EXCLUDES)
    extend_exclude = utils.validate_regex(extend_exclude)
    global_skip = get_skip_config(config)
    language = config.get("language", None)
    configuration = Config(
        transformers_config=transformer_config,
        skip=global_skip,
        src=(),
        exclude=exclude,
        extend_exclude=extend_exclude,
        skip_gitignore=False,
        overwrite=False,
        show_diff=False,
        formatting=formatting_config,
        verbose=False,
        check=False,
        output=output,
        force_order=False,
        target_version=utils.ROBOT_VERSION.major,
        color=False,
        language=language,
        reruns=reruns,
        config_directory=config_directory,
    )
    return app.Robotidy(config=configuration)


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
