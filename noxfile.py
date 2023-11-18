import nox

DEFAULT_PYTHON_VERSION = "3.11"

UNIT_TEST_PYTHON_VERSIONS = ["3.7", "3.8", "3.9", "3.10", "3.11"]
nox.options.sessions = [
    "unit",
]


def install_dev_deps(session, robot_major_ver):
    session.install("-r", f"tests/rf_versions_matrix/requirements_rf{robot_major_ver}.txt")
    session.install(".[dev]")


def install_doc_deps(session, robot_major_ver):
    session.install("-r", f"tests/rf_versions_matrix/requirements_rf{robot_major_ver}.txt")
    session.install(".[doc]")


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS)
@nox.parametrize("robot_version", list(range(4, 8)))
def unit(session, robot_version):
    install_dev_deps(session, robot_version)
    session.run("pytest", "tests")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def coverage(session):
    install_dev_deps(session, "7")
    session.install("coverage")
    session.run("coverage", "run", "-m", "pytest")
    session.run("coverage", "html")


@nox.session()
def docs(session):
    install_doc_deps(session, "7")
    session.run("sphinx-build", "-b", "html", "docs/source", "docs/_build/")
