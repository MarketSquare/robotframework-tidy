from pathlib import Path

from invoke import task
from jinja2 import from jinja2 import Template


@task
def add_transformer(ctx, name, disabled=False):
    root = Path(__file__).parent
    template_dir = Path(root, "utils", "new_transformer_templates")
    class_path = Path(root, "robotidy", "transformers", f"{name}.py")
    docs = Path(root, "docs", "source", "transformers", f"{name}.rst")

    print(f"Creating '{class_path.relative_to(root)}' file with transformer class definition")
    with open(template_dir / "transformer.template") as f:
        class_template = Template(f.read()).render(transformer_name=name, disabled=disabled)
    with open(class_path, "w") as f:
        f.write(class_template)

    print(f"Creating '{docs.relative_to(root)} file with transformer full documentation")
    with open(template_dir / "docs.template") as f:
        docs_template = Template(f.read()).render(transformer_name=name, disabled=disabled)
    with open(docs, "w") as f:
        f.write(docs_template)

    test_dir = Path(root, "tests", "atest", "transformers", name)
    print(f"Creating '{test_dir.relative_to(root)}' directory with test stubs")
    with open(template_dir / "test_transformer.template") as f:
        test_template = Template(f.read()).render(transformer_name=name)
    test_dir.mkdir(exist_ok=True)
    (test_dir / "source").mkdir(exist_ok=True)
    (test_dir / "expected").mkdir(exist_ok=True)
    with open(test_dir / "__init__.py", "w") as f:
        pass
    with open(test_dir / "source" / "test.robot", "w") as f:
        pass
    with open(test_dir / "expected" / "test.robot", "w") as f:
        pass
    with open(test_dir / "test_transformer.py", "w") as f:
        f.write(test_template)
    _add_transformer_to_internal_list(name)


def _add_transformer_to_internal_list(name):
    path = Path(Path(__file__).parent, "robotidy", "transformers", "__init__.py")
    print(
        f"Transformer '{name}' will be placed at the end of transformers list. "
        f"You can change it in {path.relative_to(Path(__file__).parent)} file."
    )
    data = [[], []]
    after_bracket = False
    with open(path) as f:
        for line in f:
            if line == "]\n":
                after_bracket = True
            data[after_bracket].append(line)
    data[0].append(f"    '{name}',\n")
    lines = data[0] + data[1]
    with open(path, "w") as f:
        f.writelines(lines)


@task
def create_release_docs(ctx, version):
    root = Path(__file__).parent
    template_path = root / "utils/release_docs_templates/new_release.template"
    release_docs_path = root / f"docs/releasenotes/{version}.rst"
    print(f"Creating '{release_docs_path}' file with initial release notes.")
    with open(template_path) as fp:
        doc_template = Template(fp.read()).render(version=version)
    with open(release_docs_path, "w") as fp:
        fp.write(doc_template)
