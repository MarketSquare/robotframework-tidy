import nox

DEFAULT_PYTHON_VERSION = "3.9"
UNIT_TEST_PYTHON_VERSIONS = ["3.7", "3.8", "3.9", "3.10"]
nox.options.sessions = [
    "unit",
]


def install_dev_deps(session, robot_major_ver):
    session.install("-r", f"tests/packages/{robot_major_ver}/requirements.txt")
    session.install(".[dev]")


def install_doc_deps(session, robot_major_ver):
    session.install("-r", f"tests/packages/{robot_major_ver}/requirements.txt")
    session.install(".[doc]")


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS)
@nox.parametrize("robot_version", ["stable4", "stable5"])
def unit(session, robot_version):
    install_dev_deps(session, robot_version)
    session.run("pytest", "tests")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def coverage(session):
    install_dev_deps(session, "stable5")
    session.install("coverage")
    session.run("coverage", "run", "-m", "pytest")
    session.run("coverage", "html")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def docs(session):
    install_doc_deps(session, "stable5")
    session.run("sphinx-build", "-b", "html", "docs/source", "docs/_build/")
